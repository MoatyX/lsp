class Lwm2mObject:

    RESOURCES = []

    OBJ_ID: str
    OBJ_NAME: str
    HEADER_GUARD: str

    RES_COUNT = 0
    MULTI_INSTANCE = False

    def __init__(self, obj_name: str, obj_id: str, header_guard: str, resources, multi_instance: bool):
        self.RESOURCES = resources
        self.OBJ_NAME = obj_name
        self.OBJ_ID = obj_id
        self.HEADER_GUARD = header_guard
        self.RES_COUNT = len(list(self.RESOURCES))
        self.MULTI_INSTANCE = multi_instance
        pass
