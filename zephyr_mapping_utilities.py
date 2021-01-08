"""functions that helps mapping standard-defined LwM2M Resource types, to a equivalent Programming language Data type"""

# a dictionary that maps XML Resource Types to equivalent C++ (first part of the tuple) or Zephyr C type (2nd part)
# https://www.openmobilealliance.org/release/LightweightM2M/V1_1-20180710-A/HTML-Version/OMA-TS-LightweightM2M_Core-V1_1-20180710-A.html
# Appendix C. Data Types (Normative)
res_types = {
    "Boolean": ("bool", "BOOL"),
    "Integer": ("int64_t", "S64"),
    "String": ("char*", "STRING"),
    "Float": ("float", "FLOAT32"),
    "Time": ("char", "STRING"),
    "EXEC": ("executable", ""),
    "Objlnk": ("void*", "OBJLNK"),
    "Opaque": ("void*", "OPAQUE"),
    "Corelnk": ("char*", "STRING"),
    "Unsigned Integer": ("uint64_t", "U64")
}


def map_to_cpp_data_type(res_data_type: str, res_op: str, is_multiple: bool) -> str:
    """
    map a lwm2m resource to a primitive data type using its Resource ID.

    :param is_multiple:
    :param res_op: the string
    :param res_data_type: the string data type from the xml
    """
    # some adjustments to the input, to avoid filling the dictionary with redundant values
    if res_op == "E":
        res_data_type = "EXEC"  # executable
        pass

    try:
        out_tuple = res_types[res_data_type]
        output = out_tuple[0]
        if is_multiple:
            corrected_output = f"multi_inst_resource<{output}>"
            output = corrected_output
            pass

        return output
    except:
        raise Exception(f"{res_data_type} not supported")
        pass
    pass


def map_to_zephyr_type_def(res_data_type: str) -> str:
    if not res_data_type:
        return ""

    output = res_types[res_data_type]
    return output[1]


def map_resource_instance_type(data_type: str, default_instance_definition: str) -> str:
    """
    in the C++ Client, instances can be SINGLE instanced, MULTIPLE Instanced or PTR.
        SINGLE or MULTIPLE are both LwM2M standards and thus can be extracted from a standard
        xml Document and passed to as the `default_instance_definition`.
        The PTR Instance Type is only available inside our custom C++ lwm2m client,
        it helps optimize read-only strings and pointers to executables. it's determined by the `data_type` argument.
    :param data_type: the data type string returned by the function `map_to_cpp_data_type()`
    :param default_instance_definition: the default string value of the MultipleInstances tag from a standard xml doc
    :return: the C++ defined instance type string
    :rtype: str
    """

    # for executables and pointer (i.e char*) data types, use the C++ defined PTR Instance Type.
    if data_type == "executable" or "*" in data_type:
        return "PTR"

    return default_instance_definition


def obj_is_multiple(obj_multiple_instances: str) -> bool:
    """
    maps the xml value of an Object's "MultipleInstances" to a boolean, that represents if the object can be instanced.
    this is useful to optimize memory usage of the generated code
    :param obj_multiple_instances:
    :return:
    """
    return True if obj_multiple_instances.upper() == "Multiple".upper() else False


def obj_is_mandatory(xml_mandatory: str) -> bool:
    """
    maps the xml value "Mandatory" to a boolean
    :param xml_mandatory:
    :return:
    """
    return False if xml_mandatory.upper() == "Optional".upper() else True
