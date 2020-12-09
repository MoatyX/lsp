class Lwm2mResource:
    RES_DATA_TYPE: str
    RES_NAME: str
    RES_ID: str
    RES_INST_TYPE: str
    RES_OP: str
    DESCRIPTION: str
    MANDATORY: bool

    # special field, because zephyr uses macros to represent data types internally
    ZEPHYR_RES_DATA_TYPE: str

    def __init__(self, res_id, res_name, res_op, res_inst_type, res_data_type, description, mandatory=False):
        self.RES_DATA_TYPE = res_data_type
        self.RES_NAME = res_name
        self.RES_ID = res_id
        self.RES_INST_TYPE = res_inst_type
        self.RES_OP = res_op
        self.DESCRIPTION = description
        self.MANDATORY = mandatory
        pass

    def set_zephyr_res_data_type(self, val: str):
        self.ZEPHYR_RES_DATA_TYPE = val
        pass
