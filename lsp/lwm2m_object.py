import xml.etree.ElementTree as ET

import lsp.util
from lsp.lwm2m_resource import Lwm2mResource


class Lwm2mObject:

    def __init__(self, xml_path: str):
        self.xml_path = xml_path
        self.RESOURCES = []

        self.MULTI_INSTANCE = None
        self.RES_COUNT = None
        self.HEADER_GUARD = None
        self.OBJ_DESC = None
        self.OBJ_INST = None
        self.OBJ_NAME = None
        self.OBJ_ID = None

    def parse(self):
        tree = ET.parse(self.xml_path)
        if tree is None:
            print(f"failed to parse {self.xml_path}")
            return

        root = tree.getroot()[0]  # LWM2M(actual root) -> OBJECT(use this as the "root")
        self.OBJ_ID = root.find("ObjectID").text
        self.OBJ_NAME = str(root.find("Name").text).replace(' ', '_').replace('-', '_').replace('/', '_').replace('.', '_')
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
