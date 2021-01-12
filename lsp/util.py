def split_array(input_array, num_subarray=1):
    """
    splits an array into a number of subarrays
    :param input_array:
    :param num_subarray: the number of target sub arrays. this must be in the range of [1, len(input_array)]
    :return:
    """
    list_array = []
    base_subarray_len = int(len(input_array) / num_subarray)
    index = 0
    for i in range(num_subarray):
        sub_array = []
        rest = (len(input_array) - index) % base_subarray_len
        subarray_count = base_subarray_len + rest
        for j in range(subarray_count):
            sub_array.append(input_array[index])
            index = index + 1
            pass
        list_array.append(sub_array)
        pass
    return list_array


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