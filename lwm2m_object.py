class Lwm2mObject:

    RESOURCES = []

    OBJ_ID: str
    OBJ_NAME: str
    HEADER_GUARD: str

    RES_COUNT = 0

    def __init__(self, obj_name, obj_id, header_guard, resources):
        self.RESOURCES = resources
        self.OBJ_NAME = obj_name
        self.OBJ_ID = obj_id
        self.HEADER_GUARD = header_guard
        self.RES_COUNT = len(list(self.RESOURCES))
        pass
