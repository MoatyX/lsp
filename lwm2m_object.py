class Lwm2mObject:
    RESOURCES = []
    OBJ_ID = 0
    OBJ_NAME = 0
    HEADER_GUARD = 0
    RES_COUNT = 0

    def __init__(self, obj_name, obj_id, header_guard, resources):
        self.RESOURCES = resources
        self.OBJ_NAME = obj_name
        self.OBJ_ID = obj_id
        self.HEADER_GUARD = header_guard
        self.RES_COUNT = len(list(self.RESOURCES))
