import xml.etree.ElementTree as ET
import zephyr_mapping_utilities as zephyr_mapper


class Lwm2mResource:

    # essential resource data
    RES_DATA_TYPE: str
    RES_DATA_TYPE_RAW: str
    RES_NAME: str
    RES_ID: str
    RES_INST_TYPE: str
    RES_OP: str
    DESCRIPTION: str
    MANDATORY: bool

    # Metadata, helps produce good code
    RES_TYPE: str
    ZEPHYR_RES_DATA_TYPE: str

    xml_res: ET.Element

    def __init__(self, xml_res: ET.Element):
        self.xml_res = xml_res
        pass

    def parse(self):
        self.RES_ID = self.xml_res.attrib["ID"]
        self.RES_NAME = self.xml_res.find("Name").text.replace(' ', '_').lower()
        self.RES_DATA_TYPE_RAW = self.xml_res.find("Type").text
        self.RES_OP = self.xml_res.find("Operations").text.replace(' ', '_')
        self.RES_DATA_TYPE = zephyr_mapper.map_to_cpp_data_type(self.RES_DATA_TYPE_RAW, self.RES_OP)
        self.ZEPHYR_RES_DATA_TYPE = zephyr_mapper.map_to_zephyr_type_def(self.RES_DATA_TYPE_RAW)
        res_inst_type_raw = self.xml_res.find("MultipleInstances").text.replace(' ', '_')
        self.RES_INST_TYPE = zephyr_mapper.map_resource_instance_type(self.RES_DATA_TYPE, res_inst_type_raw)
        self.DESCRIPTION = self.xml_res.find("Description").text
        self.MANDATORY = False if self.xml_res.find("Mandatory").text == "Optional" else True
        pass
