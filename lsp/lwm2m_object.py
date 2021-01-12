import xml.etree.ElementTree as ET

import lsp.util
from lsp import zephyr_mapping_utilities as zephyr_mapper
from lsp.lwm2m_resource import Lwm2mResource


class Lwm2mObject:
    xml_path: str
    RESOURCES = []
    OBJ_ID: str
    OBJ_NAME: str
    OBJ_INST: str
    OBJ_DESC: str
    HEADER_GUARD: str

    RES_COUNT = 0
    MULTI_INSTANCE = False

    def __init__(self, xml_path: str):
        self.xml_path = xml_path
        pass

    def parse(self):
        tree = ET.parse(self.xml_path)
        if tree is None:
            print(f"failed to parse {self.xml_path}")
            return

        root = tree.getroot()[0]  # LWM2M(actual root) -> OBJECT(use this as the "root")
        self.OBJ_ID = root.find("ObjectID").text
        self.OBJ_NAME = str(root.find("Name").text).replace(' ', '_').replace('-', '_').replace('/', '_')
        self.OBJ_DESC = root.find("Description1").text
        self.HEADER_GUARD = "NX_GENERATED_" + self.OBJ_NAME.upper() + "_ID_" + self.OBJ_ID + "_H_"
        self.OBJ_INST = root.find("MultipleInstances").text
        self.MULTI_INSTANCE = lsp.util.obj_is_multiple(self.OBJ_INST)

        resources_raw = root.find("Resources")
        for res_raw in resources_raw:
            res = Lwm2mResource(res_raw)
            res.parse()
            self.RESOURCES.append(res)
            pass
        self.RES_COUNT = len(self.RESOURCES)
        pass
