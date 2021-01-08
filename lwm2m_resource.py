import xml.etree.ElementTree as ET
import zephyr_mapping_utilities as mapper
import re


class Lwm2mResource:
    # constants
    DEFAULT_MULTIPLE_COUNT = 7  # special case for the resources that don't define max instance count. we will assume the resource can have max this count of instances
    DEFAULT_RES_OP = "RW"       # some lwm2m objects leave the "Operations" tag empty for some reason

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

        if self.RES_OP is None: self.RES_OP = self.DEFAULT_RES_OP
        res_xml_is_multi = self.xml_res.find("MultipleInstances").text

        self.IS_MULTIPLE = mapper.obj_is_multiple(res_xml_is_multi)
        if self.IS_MULTIPLE:
            range_enum = self.xml_res.find("RangeEnumeration").text
            if range_enum: range_enum = range_enum.strip()
            if not range_enum:
                self.RANGE_BEGIN = 0
                self.RANGE_END = self.DEFAULT_MULTIPLE_COUNT
                pass
            else:
                range_array = re.findall("\d+", range_enum)
                if len(range_array) == 0:
                    raise Exception(f"failed to decode {self.RES_NAME}'s RangeEnumeration")
                if len(range_array) == 1: range_array.insert(0, 0)
                self.RANGE_BEGIN = int(range_array[0])
                self.RANGE_END = int(range_array[len(range_array) - 1])
                pass
            self.RANGE = abs(self.RANGE_END - self.RANGE_BEGIN)
        pass

        try:
            self.RES_CPP_DATA_TYPE = mapper.map_to_cpp_data_type(self.RES_XML_DATA_TYPE, self.RES_OP, self.IS_MULTIPLE)
            self.RES_INST_TYPE = mapper.map_resource_instance_type(self.RES_CPP_DATA_TYPE, res_xml_is_multi)
            self.ZEPHYR_RES_DATA_TYPE = mapper.map_to_zephyr_type_def(self.RES_XML_DATA_TYPE)
        except:
            raise Exception("failed to decode C++/zephyr data type from XML input")
            pass

        self.DESCRIPTION = self.xml_res.find("Description").text
        res_xml_mandatory = self.xml_res.find("Mandatory").text
        self.MANDATORY = mapper.obj_is_mandatory(res_xml_mandatory)
        pass
