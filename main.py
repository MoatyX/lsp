import xml.etree.ElementTree as ET
import zephyr_type_mapper as zephyr_mapper
from datetime import date
from jinja2 import Environment, FileSystemLoader
from lwm2m_object import Lwm2mObject
from lwm2m_resource import Lwm2mResource
from pathlib import Path

TEMPLATES_DIR = "./templates"
LWM2M_OBJECTS_TEMPLATE_FILE = "lwm2m_object_template.txt"
LWM2M_OBJECTS_OUTPUT_PATH = "./generated/"

# metadata
GEN_DATE = date.today().strftime("%m/%Y")


def generate_lwm2m_object(templates_dir, template_name, xml_path, output_dir_path=None) -> Lwm2mObject:
    # TODO: first do XML Schema Validation
    tree = ET.parse(xml_path)
    if tree is None:
        print(f"failed to parse {xml_path}")
        return None
    root = tree.getroot()[0]  # LWM2M(actual root) -> OBJECT(use this as the "root")

    obj_name = str(root.find("Name").text).replace(' ', '_')
    OBJ_ID = root.find("ObjectID").text
    HEADER_GUARD = "NX_GENERATED_" + obj_name.upper() + "_ID_" + OBJ_ID + "_H_"

    resources_raw = root.find("Resources")
    RESOURCES = []
    for res in list(resources_raw):
        res_id = res.attrib["ID"]
        res_name = res.find("Name").text.replace(' ', '_').lower()
        res_op = res.find("Operations").text.replace(' ', '_')
        res_cpp_data_type = zephyr_mapper.map_to_cpp_data_type(res_id)
        res_zephyr_data_type = zephyr_mapper.map_to_zephyr_type_def(res_id)
        res_inst_type_raw = res.find("MultipleInstances").text.replace(' ', '_')
        res_inst_type = zephyr_mapper.map_resource_instance_type(res_cpp_data_type, res_inst_type_raw)
        description = res.find("Description").text
        mandatory = False if res.find("Mandatory").text == "Optional" else True

        res_item = Lwm2mResource(res_id, res_name, res_op, res_inst_type, res_cpp_data_type, description, mandatory)
        res_item.set_zephyr_res_data_type(res_zephyr_data_type)
        RESOURCES.append(res_item)

    # import the template
    template_loader = FileSystemLoader(templates_dir)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(template_name)

    LWM2M_OBJ = Lwm2mObject(obj_name, OBJ_ID, HEADER_GUARD, RESOURCES)
    output = template.render(GEN_DATE=GEN_DATE, LWM2M_OBJ=LWM2M_OBJ)

    # check if we should output to file, or to console
    if output_dir_path is None:
        print(output)
    else:
        # make sure the directory exits
        path = Path(output_dir_path).absolute()
        if not Path.exists(path):
            path.mkdir(parents=True, exist_ok=True)
            pass

        cpp_header_file_path = path/f"{obj_name}_id{OBJ_ID}.h"
        cpp_header = open(cpp_header_file_path, "w")
        cpp_header.writelines(output)
        cpp_header.close()
        pass

    print(f"finished parsing {xml_path}")
    return LWM2M_OBJ


def generate_zephyr_source_obj(templates_dir, template_name, lwm2m_obj: Lwm2mObject, output_dir_path=None):
    # import the template
    template_loader = FileSystemLoader(templates_dir)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(template_name)
    output = template.render(GEN_DATE=GEN_DATE, LWM2M_OBJ=lwm2m_obj)
    print(output)
    return


if __name__ == '__main__':
    # generate_lwm2m_object(TEMPLATES_DIR, "lwm2m_object_template.txt", "./xml/3347.xml",
    #                       LWM2M_OBJECTS_OUTPUT_PATH + "lwm2m_objects/")
    lwm2m_object = generate_lwm2m_object(TEMPLATES_DIR, "lwm2m_object_template.txt", "./xml/3347.xml")
    generate_zephyr_source_obj(TEMPLATES_DIR, "lwm2m_obj_zephyr_source.txt", lwm2m_object)
    pass
