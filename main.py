import xml.etree.ElementTree as ET
import zephyr_mapping_utilities as zephyr_mapper
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


def generate_lwm2m_object(templates_dir: str, template_name: str, xml_path: str, output_dir_path=None) -> Lwm2mObject:
    # TODO: first do xml Schema Validation
    LWM2M_OBJ = Lwm2mObject(xml_path)
    LWM2M_OBJ.parse()

    # import the template
    template_loader = FileSystemLoader(templates_dir)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(template_name)

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

        cpp_header_file_path = path / f"{Lwm2mObject.OBJ_NAME}_id{Lwm2mObject.OBJ_ID}.h"
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

    # check if we should output to file, or to console
    if output_dir_path is None:
        print(output)
    else:
        # make sure the directory exits
        path = Path(output_dir_path).absolute()
        if not Path.exists(path):
            path.mkdir(parents=True, exist_ok=True)
            pass

        c_file_path = path / f"{lwm2m_obj.OBJ_NAME}_id{lwm2m_obj.OBJ_ID}.c"
        zephyr_c_source = open(c_file_path, "w")
        zephyr_c_source.writelines(output)
        zephyr_c_source.close()
        pass

    print(f"generated Zephyr Source Definition {lwm2m_obj.OBJ_NAME}")
    return


def generate_zephyr_lwm2m_kconfig():
    # TODO.....
    pass


if __name__ == '__main__':
    # generate_lwm2m_object(TEMPLATES_DIR, "lwm2m_object_template.txt", "./xml/3347.xml",
    #                       LWM2M_OBJECTS_OUTPUT_PATH + "lwm2m_objects/")
    lwm2m_object = generate_lwm2m_object(TEMPLATES_DIR, "lwm2m_object_template.txt", "./xml/3347.xml")
    generate_zephyr_source_obj(TEMPLATES_DIR, "lwm2m_obj_zephyr_source.txt", lwm2m_object)
    pass
