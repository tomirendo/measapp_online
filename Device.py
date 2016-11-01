class Device:
    pass

def get_index_of_enum(value):
    return list(type(value).__members__.values()).index(value)

def get_enum_value_by_index(type, index):
    return list(type.__members__.values())[index]
    
def list_values_of_enum(enum_value):
    return [i.value for i in list(type(enum_value).__members__.values())]

def list_values_of_enum_type(enum_type):
    return [i.value for i in list(enum_type.__members__.values())]


    
