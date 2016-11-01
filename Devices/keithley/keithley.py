from Device import Device, get_enum_value_by_index, get_index_of_enum, list_values_of_enum_type
from itertools import product
from time import sleep
import pyvisa
from enum import Enum

verbose = False 

class IOType(Enum):
    Voltage = "VOLT"
    Current = "CURR"

def identify_io_type(string):
    if "CURR" or "Current" in source:
        return IOType.Current
    elif "VOLT" in source or "Voltage" in source :
        return IOType.Voltage
    else :
        raise Exception("Cannot interpret Source : {} from keithley".format(source))

class Keithley(Device):
    def __init__(self, properties):
        Device.__init__(self) 
        self.inputs = ["DCV","DCC"]
        self.port = properties['port']
        self.connection = pyvisa.ResourceManager().open_resource(self.port)
        #self.connection = mock_connection() #Mock connection for tests
        self.outputs = ["DCV","DCC"]
        self.properties = self._read_properties()

    def _read_properties(self):
        dictionary = {}
        source = self.connection.query(":SOUR:FUNC?")
        dictionary['Source']  = identify_io_type(source)
        dictionary['Source Range'] = self.connection.query(":SOUR:{}:RANG?".format(dictionary['Source']).value)
        sensor = self.connection.query(":SENS:FUNC?") 
        dictionary['Sensor'] = identify_io_type(sensor)
        dictionary['Sensor Range'] = self.connection.query(":SENS:{}:RANG?".format(dictionary['Source']).value)
        dictionary['Sensor Protocol'] = self.connection.query(":SENS:{}:PROT?".format(dictionary['Source']).value)

    def check_connection(self):
        return self.connection.query("*IDN?").startswith('Stanford_Research_Systems,SR830')

    def list_outputs(self):
        return self.outputs 

    def list_inputs(self):
        return self.inputs 

    def read_input(self, input_name):
        if input_name in self.inputs:
            pass
        raise Exception("Trying to read from a non existing port")

    def write_output(self, output_name, value):
        pass

    def write_raw(self, value):
        if isinstance(value, str):
            value = value.encode()
        elif isinstance(value, bytes):
            self.connection.write_raw(value)
        else :
            raise Exception("Unknown type to write raw (Accepts str or bytes)")

    def read_raw(self):
        return self.connection.read_raw()

    def set_property(self, name, value):
        if name not in property_type_dictionary:
            raise Exception("Unknown property {}".format(name))

        #Convert String to Enum if required
        if value in list_values_of_enum_type(property_type_dictionary[name]):
            value = property_type_dictionary[name](value)

        if value in property_type_dictionary[name]:
            self.properties[name] = value
            self.connection.query("{} {}".format(property_command_dictionary[name], get_index_of_enum(value)))
        else :
            raise Exception("Value isn't of type {}".format(type(property_type_dictionary[name])))


    def get_properties(self):
        self.properties = self._read_properties()
        return self.properties

    def close(self, *exp):
        self.connection.close()


    
