from jinja2 import Template, Environment, FileSystemLoader
import xml.etree.ElementTree as ET

TEMPLATES_DIR = "./"
LWM2M_OBJECTS_TEMPLATE = "lwm2m_objects_template.txt"
LWM2M_OBJECTS_OUTPUT_PATH = "./generated/"

if __name__ == '__main__':
    tree = ET.parse("xml/test.xml")
    for node in tree.iter():
        print(node.tag)
