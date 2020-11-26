class Lwm2mResource:
    RES_DATA_TYPE = 0
    RES_NAME = 0
    RES_ID = 0
    RES_INST_TYPE = 0
    RES_OP = 0
    DESCRIPTION = 0

    def __init__(self, res_id, res_name, res_op, res_inst_type, res_data_type, description):
        self.RES_DATA_TYPE = res_data_type
        self.RES_NAME = res_name
        self.RES_ID = res_id
        self.RES_INST_TYPE = res_inst_type
        self.RES_OP = res_op
        self.DESCRIPTION = description
