from jinja2 import Template, Environment, FileSystemLoader
from datetime import date
import xml.etree.ElementTree as ET
from lwm2m_resource import Lwm2mResource

TEMPLATES_DIR = "./templates"
LWM2M_OBJECTS_TEMPLATE_FILE = "lwm2m_object_template.txt"
LWM2M_OBJECTS_OUTPUT_PATH = "./generated/"

# metadata
GEN_DATE = date.today().strftime("%m/%Y")


def generate_lwm2m_object(xml_path):
    # TODO: first do XML Schema Validation
    tree = ET.parse(xml_path)
    if tree is None:
        print("failed to parse")
        return
    root = tree.getroot()[0]  # LWM2M(actual root) -> OBJECT(use this as the "root")

    obj_name = str(root.find("Name").text).replace(' ', '_').lower()
    OBJ_ID = root.find("ObjectID").text
    HEADER_GUARD = "NX_GENERATED_" + obj_name.upper() + "_ID_" + OBJ_ID + "_H_"

    resources_raw = root.find("Resources")
    RES_COUNT = len(list(resources_raw))
    RESOURCES = []
    for res in list(resources_raw):
        res_id = res.attrib["ID"]
        res_name = res.find("Name").text.replace(' ', '_').lower()
        res_op = res.find("Operations").text.replace(' ', '_')
        res_inst_type = res.find("MultipleInstances").text.replace(' ', '_').upper()  # TODO: adjust to fit the C++ enum
        res_data_type_raw = res.find("Type").text.replace(' ', '_')  # TODO: convert this to a C++ data type
        description = res.find("Description").text

        res_item = Lwm2mResource(res_id, res_name, res_op, res_inst_type, res_data_type_raw, description)
        RESOURCES.append(res_item)

    # import the template
    template_loader = FileSystemLoader(TEMPLATES_DIR)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template("lwm2m_object_template.txt")
    output = template.render(GEN_DATE=GEN_DATE, OBJ_ID=OBJ_ID, HEADER_GUARD=HEADER_GUARD, RES_COUNT=RES_COUNT, RESOURCES=RESOURCES)
    print(output)   # TODO: instead of printing, write out a file


if __name__ == '__main__':
    generate_lwm2m_object("./xml/3347.xml")
