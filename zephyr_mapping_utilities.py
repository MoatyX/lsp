"""functions that helps mapping standard-defined LwM2M Resource types, to a equivalent Programming language Data type"""

res_types = {
    "Boolean": ("bool", "BOOL"),
    "Integer": ("uint64_t", "U64"),
    "StringR": ("char*", "STRING"),
    "StringRW": ("char", "STRING"),
    "String": ("char*", "STRING"),      # the first tuple part should be unused
    "Float": ("float", "FLOAT32")
}


def map_to_cpp_data_type(res_data_type: str, res_op: str) -> str:
    """
    map a lwm2m resource to a primitive data type using its Resource ID.

    :param res_op: the string
    :param res_data_type: the string data type from the xml
    """
    # string optimization for c++
    if res_data_type == "String":
        res_data_type += res_op
        pass

    output = res_types[res_data_type]
    return output[0]


def map_to_zephyr_type_def(res_data_type: str) -> str:
    output = res_types[res_data_type]
    return output[1]


def map_resource_instance_type(data_type: str, default_instance_definition: str) -> str:
    """
    in the C++ Client, instances can be SINGLE instanced, MULTIPLE Instanced or PTR.
        SINGLE or MULTIPLE are both LwM2M standards and thus can be extracted from a standard
        xml Document and passed to as the `default_instance_definition`.
        The PTR Instance Type is determined by the `data_type` argument.
    :param data_type: the data type string returned by the function `map_data_type()`
    :param default_instance_definition: the default string value of the MultipleInstances tag from a standard xml doc
    :return: the C++ defined instance type string
    :rtype: str
    """

    # for execute and pointer (i.e char*) data types, use the C++ defined PTR Instance Type
    if data_type == "EXEC" or "*" in data_type:
        return "PTR"

    return default_instance_definition


def obj_instance_is_multiple(obj_multiple_instances: str) -> bool:
    """
    maps the xml value of an Object's "MultipleInstances" to a boolean, that represents if the object can be instanced.
    this is useful to optimize memory usage of the generated code
    :param obj_multiple_instances:
    :return:
    """
    if obj_multiple_instances == "Multiple":
        return True
    else:
        return False
