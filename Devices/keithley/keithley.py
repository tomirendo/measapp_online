from devices.Device import Device, get_enum_value_by_index, get_index_of_enum, list_values_of_enum_type
from itertools import product
from time import sleep
import pyvisa
from enum import Enum
from numpy import log10, ceil

verbose = False

class IOType(Enum):
    Voltage = "VOLT"
    Current = "CURR"

class OutputState(Enum):
    On = "On"
    Off = "Off"

class VoltageRange(Enum):
    range_210V = "210 V"
    range_21V = "21 V"
    range_2100mv = "2.1 V"
    range_210mv = "210 mV"

def convert_voltage_range(range):
    index = get_index_of_enum(VoltageRange(range))
    result =  210 * (10**-index)
    return result

class CurrentRange(Enum):
    range_1_05A = "1.05 A"
    range_105mA = "105 mA"
    range_10_5mA = "10.5 mA"
    range_1_05mA = "1.05 mA"
    range_105_micro_A = "105 μA"
    range_10_5_micro_A = "10.5 μA"
    range_1_05_micro_A = "1.05 μA"

def convert_current_range(range):
    index = get_index_of_enum(CurrentRange(range))
    return 1.05 * (10**-index)

def convert_range(value, type):
    if type == IOType.Current:
        index = int(-ceil(log10(float(value)/1.05)))
        return get_enum_value_by_index(CurrentRange, index)
    elif type == IOType.Voltage:
        index = int(-ceil(log10(float(value)/210)))
        return get_enum_value_by_index(VoltageRange, index)
    raise Exception("Cannot Identify range {} of type {}".format(value, type))

def identify_io_type(string):
    if "CURR" in string or "Current" in string:
        return IOType.Current
    elif "VOLT" in string or "Voltage" in string :
        return IOType.Voltage
    else :
        raise Exception("Cannot interpret Source : {} from Keithley".format(source))

def identify_output_state(text):
    if "1" in text:
        return OutputState.On
    elif "0" in text:
        return OutputState.Off
    raise Exception("Cannot identify output state {}".format(text))

property_command_dictionary = {
    'Source' : ":SOUR:FUNC ",
    'Source Voltage Range' : ':SOUR:VOLT:RANG ',
    'Source Current Range' : ':SOUR:CURR:RANG ',
    'Sensor' : ":CONF:",
    'Sensor Voltage Range' : ':SENS:VOLT:RANG ',
    'Sensor Protection Voltage' : None,
    'Sensor Protection Current' : None,
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
            self.properties = self._read_properties()
        except Exception as e:
            self.connection.close()
            raise(e)

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
        dictionary['Source Voltage Range'] = convert_range(self.query(":SOUR:VOLT:RANG?"), IOType.Voltage)
        dictionary['Source Current Range'] = convert_range(self.query(":SOUR:CURR:RANG?"), IOType.Current)
        sensor = self.query(":SENS:FUNC?") 
        dictionary['Sensor'] = identify_io_type(sensor)
        dictionary['Sensor Voltage Range'] = convert_range(self.query(":SENS:VOLT:RANG?"), IOType.Voltage)
        dictionary['Output'] = identify_output_state(self.query(":OUTP?"))
        dictionary['Sensor Protection Voltage'] = float(self.query("SENS:VOLT:PROT?"))
        dictionary['Sensor Protection Current'] = float(self.query("SENS:CURR:PROT?"))
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
            if input_name.upper() == 'DCV':
                return float(self.query(":READ?").split(',')[0])
            elif input_name.upper() == 'DCC':
                return float(self.query(":READ?").split(',')[1])
        else : 
            raise Exception("Trying to read from a non existing input : {}".format(input_name))

    def write_output(self, output_name, value):
        lower_case_outputs = [i.lower() for i in self.outputs]
        

        if output_name.lower() in lower_case_outputs:
            if output_name.upper() == 'DCV':
                if self.properties['Source'] == IOType.Voltage:
                    self.connection.write(set_dcv_command.format(value))
                else :
                    raise Exception("Cannot write DCV - Source not in Voltage mode")

            elif output_name.upper() == 'DCC':
                if self.properties['Source'] == IOType.Current:
                    self.connection.write(set_dcc_command.format(value))
                else :
                    raise Exception("Cannot write DCC - Source not in Current mode")
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

    def set_property(self, name, value, reload_properties = True):
        if name not in property_command_dictionary:
            raise Exception("Unknown property {}".format(name))

        if name in ['Source', 'Sensor']:
            if value in IOType:
                value = value.value
            command_to_write = "{}{}".format(property_command_dictionary[name], value)
        elif name == "Output":
            if value in OutputState:
                value = value.value
            value = value.upper()
            command_to_write = ":OUTP {}".format(value)

        elif name == 'Sensor Protection Voltage':
            command_to_write = "SENS:VOLT:PROT {}".format(value)

        elif name == 'Sensor Protection Current':
            command_to_write = "SENS:CURR:PROT {}".format(value)

        elif 'Voltage' in name:
            command_to_write = "{}{}".format(property_command_dictionary[name], convert_voltage_range(value))
        elif 'Current' in name:
            command_to_write = "{}{}".format(property_command_dictionary[name], convert_current_range(value))

        if verbose:
            print("Updating Property : {}:{} with command '{}'".format(name, value, command_to_write))

        if command_to_write is not None:
            self.connection.write(command_to_write)
            if reload_properties:
                self.get_properties()
        """
            'Source' : ":SOUR:FUNC ",
            'Source Voltage Range' : ':SOUR:VOLT:RANG ',
            'Source Current Range' : ':SOUR:CURR:RANG ',
            'Sensor' : ":CONF:",
            'Sensor Voltage Range' : ':SENS:VOLT:RANG ',
            'Sensor Current Range' : ':SENS:CURR:RANG ',
            'Sensor Protocol' : None,
            "Output" : None,
        """
    def get_properties(self):
        self.properties = self._read_properties()
        return self.properties

    def close(self, *exp):
        self.connection.close()
        if verbose:
            print("Close Connection to Keithley")



    """ Not Required """
    def set_properties(self, properties_dictionary):
        """
        Overriding set_properties of the standart Device object described in Device.py 
        by overwriting this I can controll the order of updating properties
        """
        ordered_properties = ['Sensor Protection Current','Sensor Protection Voltage' ,
        'Source' ,'Source Voltage Range', 'Source Current Range','Sensor' ,
        'Sensor Voltage Range',"Output" ]
        for key in ordered_properties:
            print("Updating ",format(key))
            self.set_property(key, properties_dictionary[key], reload_properties=True)

        self.get_properties()


    def set_output_voltage(self):
        self.set_property("Source",IOType.Voltage)

    def set_output_current(self):
        self.set_property("Source",IOType.Current)

    def set_input_voltage(self):
        self.set_property("Sensor",IOType.Voltage)

    def set_input_current(self):
        self.set_property("Sensor",IOType.Current)

    def set_current(self, value):
        self.write_output("DCC", value)

    def set_voltage(self, value):
        self.write_output("DCV", value)

    def read_voltage(self):
        return self.read_input("DCV")

    def read_current(self):
        return self.read_input("DCC")
 
    def read(self):
        if self.properties['Sensor'] == IOType.Current:
            return self.read_current()
        elif self.properties['Sensor'] == IOType.Voltage:
            return self.read_voltage()


    
