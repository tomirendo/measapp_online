class PhysicalDeviceObject:
    def __init__(self, dictionary):
        self.name = dictionary.get("name", "Noname")
        self.object = dictionary['object'](dictionary.get("properties",{}))
        self.check_connection()
        self.is_locked = False
        self.owner = None
        print("Done Loading Device : {}".format(self.name))

    def check_connection(self):
        assert self.object.check_connection() == True

    def to_dict(self):
        return {'name' : self.name,
                'inputs' : self.object.list_inputs(),
                'outputs' : self.object.list_outputs(),
                'properties' : list(self.object.get_properties().items())}

