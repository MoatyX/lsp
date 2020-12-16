import xml.etree.ElementTree as ET
import zephyr_mapping_utilities as mapper


class Lwm2mResource:

    # essential resource data
    RES_CPP_DATA_TYPE: str
    RES_XML_DATA_TYPE: str
    RES_NAME: str
    RES_ID: str
    RES_INST_TYPE: str
    RES_OP: str
    DESCRIPTION: str
    MANDATORY: bool
    IS_MULTIPLE: bool
    RANGE_BEGIN: int
    RANGE_END: int
    RANGE: int

    # Metadata, helps produce good code
    RES_TYPE: str
    ZEPHYR_RES_DATA_TYPE: str

    xml_res: ET.Element

    def __init__(self, xml_res: ET.Element):
        self.xml_res = xml_res
        pass

    def parse(self):
        self.RES_ID = self.xml_res.attrib["ID"]
        self.RES_NAME = self.xml_res.find("Name").text.replace(' ', '_').replace('-', '_').replace('/', '_').lower()
        self.RES_XML_DATA_TYPE = self.xml_res.find("Type").text
        self.RES_OP = self.xml_res.find("Operations").text
        res_xml_is_multi = self.xml_res.find("MultipleInstances").text

        self.IS_MULTIPLE = mapper.obj_is_multiple(res_xml_is_multi)
        if self.IS_MULTIPLE:
            range_enum = self.xml_res.find("RangeEnumeration").text
            range_array = range_enum.partition("-")
            self.RANGE_BEGIN = int(range_array[0])
            self.RANGE_END = int(range_array[2])
            self.RANGE = abs(self.RANGE_END - self.RANGE_BEGIN)
        pass

        self.RES_CPP_DATA_TYPE = mapper.map_to_cpp_data_type(self.RES_XML_DATA_TYPE, self.RES_OP, self.IS_MULTIPLE)
        self.RES_INST_TYPE = mapper.map_resource_instance_type(self.RES_CPP_DATA_TYPE, res_xml_is_multi)
        self.ZEPHYR_RES_DATA_TYPE = mapper.map_to_zephyr_type_def(self.RES_XML_DATA_TYPE)
        self.DESCRIPTION = self.xml_res.find("Description").text
        res_xml_mandatory = self.xml_res.find("Mandatory").text
        self.MANDATORY = mapper.obj_is_mandatory(res_xml_mandatory)
        pass
