from Device import list_values_of_enum
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
                'properties' : properties_to_json(self.object.get_properties())}


from enum import Enum

def properties_to_json(properties_dict):
    result = []
    for key, value in properties_dict.items():
        if isinstance(value , Enum):
            result.append({'name' : key, 'value': value.value, 'type' : list_values_of_enum(value)})
        else :
            result.append({'name' : key, 'value' : value, 'type' : 'number'})
    return result

