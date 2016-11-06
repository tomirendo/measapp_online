from devices.Device import Device, get_enum_value_by_index, get_index_of_enum, list_values_of_enum_type
from itertools import product
from time import sleep
import pyvisa
from enum import Enum

verbose = False

class IOType(Enum):
    Voltage = "VOLT"
    Current = "CURR"

class OutputState(Enum):
    On = "On"
    Off = "Off"

def identify_io_type(string):
    if "CURR" in string or "Current" in string:
        return IOType.Current
    elif "VOLT" in string or "Voltage" in string :
        return IOType.Voltage
    else :
        raise Exception("Cannot interpret Source : {} from keithley".format(source))

def identify_output_state(text):
    if "1" in text:
        return OutputState.On
    elif "0" in text:
        return OutputState.Off
    raise Exception("Cannot identify output state {}".format(text))

property_command_dictionary = {
    'Source' : ":SOUR:FUNC ",
    'Source Range' : None,
    'Sensor' : ":CONF:",
    'Sensor Range' : None,
    'Sensor Protocol' : None,
    "Output" : None,
}

set_output_command = ":OUTP {}"
set_dcv_command = ":SOUR:VOLT:LEV {}"
set_dcc_command = ":SOUR:CURR:LEV {}"
class Keithley(Device):
    def __init__(self, properties):
        Device.__init__(self) 
        self.inputs = ["DCV","DCC"]
        self.outputs = ["DCV","DCC"]
        self.port = properties['port']
        self.connection = pyvisa.ResourceManager().open_resource(self.port)
        #self.connection = mock_connection() #Mock connection for tests

        try :
            self._reset()
            self.properties = self._read_properties()
        except Exception as e:
            self.connection.close()
            raise(e)


    def _reset(self):
        self.connection.write("*RST")

    def query(self, *args):
        if verbose:
            print("Query : {}".format(args))
        try :
            res = self.connection.query(*args)
        except Exception as e:
            print("Cannot query {}".format(args))
            raise e

        if verbose:
            print("Query Result : {}".format(res))
        return res

    def _read_properties(self):
        dictionary = {}
        source = self.query(":SOUR:FUNC?")
        dictionary['Source']  = identify_io_type(source)
        dictionary['Source Range'] = self.query(":SOUR:{}:RANG?".format(dictionary['Source'].value))
        sensor = self.query(":SENS:FUNC?") 
        dictionary['Sensor'] = identify_io_type(sensor)
        dictionary['Sensor Range'] = self.query(":SENS:{}:RANG?".format(dictionary['Source'].value))
        dictionary['Sensor Protocol'] = self.query(":SENS:{}:PROT?".format(dictionary['Source'].value))
        dictionary['Output'] = identify_output_state(self.query(":OUTP?"))
        return dictionary 


    def _init_sense(self, input_name):           
        if input_name.upper() == 'DCV':
            if self.properties['Sensor'] != IOType.Voltage:
                self.set_property('Sensor', IOType.Voltage)
        elif input_name.upper() == 'DCC':
            if self.properties['Sensor'] != IOType.Current:
                self.set_property('Sensor', IOType.Current)

    def _is_output_on(self):
        return identify_output_state(self.query(":OUTP?")) == OutputState.On

    def _output_on(self):
        if not self._is_output_on():
            self.set_property("Output", OutputState.On)

    def check_connection(self):
        return self.connection.query("*IDN?").startswith('KEITHLEY INSTRUMENTS INC')

    def list_outputs(self):
        return self.outputs 

    def list_inputs(self):
        return self.inputs 

    def read_input(self, input_name):
        lower_case_inputs = [i.lower() for i in self.inputs]
        
        if input_name.lower() in lower_case_inputs:
            self._init_sense(input_name)
            self._output_on()

            data = self.query(":READ?").split(',')
            if input_name.upper() == 'DCV':
                return float(data[0])
            elif input_name.upper() == 'DCC':
                return float(data[1])
        raise Exception("Trying to read from a non existing input : {}".format(input_name))

    def write_output(self, output_name, value):
        
        lower_case_outputs = [i.lower() for i in self.outputs]
        if output_name.lower() in lower_case_outputs:
            if output_name.upper() == 'DCV':
                self.connection.write(set_dcv_command.format(value))
            elif output_name.upper() == 'DCC':
                self.connection.write(set_dcc_command.format(value))
            else :
                raise Exception("Cannot find output {}".format(output_name))
        else :
            raise Exception("Cannot find output {}".format(output_name))
        self._output_on()

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
        if name not in property_command_dictionary:
            raise Exception("Unknown property {}".format(name))


        command_to_write = None

        if name in ['Source', 'Sensor']:
            if value in IOType:
                value = value.value
            command_to_write = "{}{}".format(property_command_dictionary[name], value)

        if name == "Output":
            if value in OutputState:
                value = value.value
            value = value.upper()
            command_to_write = ":OUTP {}".format(value)

        if verbose:
            print("Updating Property : {}:{} with command '{}'".format(name, value, command_to_write))

        if command_to_write is not None:
            self.connection.write(command_to_write)




    def get_properties(self):
        self.properties = self._read_properties()
        return self.properties

    def close(self, *exp):
        self.connection.close()
        if verbose:
            print("Close Connection to Keithley")


    
