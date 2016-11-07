from devices.Device import Device, get_enum_value_by_index, get_index_of_enum, list_values_of_enum_type
from itertools import product
from time import sleep
import pyvisa
from devices.device_controller.GPIB_controller import GPIBDeviceConnection
from enum import Enum

verbose = False


class IOType(Enum):
    Voltage = "VOLT"
    Current = "CURR"

class SensorRangeVolt(Enum):
    range_1000V = '1000 V'
    range_100V = '100V'
    range_10V = '10V'
    range_1V = '1V' 
    range_100mV = '100mV'

class SensorRangeCurrent(Enum):
    range_3A = '3A'
    range_1A = '1A'
    range_100mA = '100mA'
    range_10mA = '10mA' 

def convert_range_to_float(range):
    if 'm' in range:
        return float(range.replace("A","").replace("m","").replace("V",""))*.001
    else:
        return float(range.replace("A","").replace("V",""))


def identify_io_type(string):
    if "CURR" in string or "Current" in string:
        return IOType.Current
    elif "VOLT" in string or "Voltage" in string :
        return IOType.Voltage
    else :
        raise Exception("Cannot interpret Source : {} from keithley".format(source))
def identify_sensor_range_volt(string):
    volt_dict = {
        101000 : SensorRangeVolt.range_1000V,
        10000 : SensorRangeVolt.range_100V ,
        1000 :  SensorRangeVolt.range_10V ,
        100 : SensorRangeVolt.range_1V ,
        10 : SensorRangeVolt.range_100mV,
    }
    return volt_dict[int(float(string)*100)]

def identify_sensor_range_curr(string):
    curr_dict = {
        300 : SensorRangeCurrent.range_3A,
        100 : SensorRangeCurrent.range_1A,
        10 :  SensorRangeCurrent.range_100mA,
        1 : SensorRangeCurrent.range_10mA,
    }
    return curr_dict[int(float(string)*100)]

property_command_dictionary = {
    'Sense' : ":SENSE:FUNC",
    'Sense Range Voltage' : ':SENS:VOLT:RANG',
    'Sense Range Current' : ':SENS:CURR:RANG',
}
class DMM(Device):
    def __init__(self, properties):
        Device.__init__(self) 
        self.inputs = ["DCV/DCC"]
        self.outputs = []
        self.port = properties['port']
        #self.connection = pyvisa.ResourceManager().open_resource(self.port)
        #self.connection = mock_connection() #Mock connection for tests
        self.connection = GPIBDeviceConnection(self.port)


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
        source = self.query(":SENS:FUNC?")
        dictionary['Sense']  = identify_io_type(source)
        self.connection.write(":SENS:{}:RANG:AUTO OFF".format(dictionary['Sense'].value))
        sense_range_volt = self.query(":SENS:VOLT:RANG?")
        dictionary['Sense Range Voltage'] = identify_sensor_range_volt(sense_range_volt)
        sense_range_curr = self.query(":SENS:CURR:RANG?")
        dictionary['Sense Range Current'] = identify_sensor_range_curr(sense_range_curr)

        return dictionary 


    def check_connection(self):
        return self.connection.query("*IDN?").startswith('KEITHLEY INSTRUMENTS INC.,MODEL 2000')

    def list_outputs(self):
        return self.outputs 

    def list_inputs(self):
        return self.inputs 

    def read_input(self, input_name):
        lower_case_inputs = [i.lower() for i in self.inputs]
        
        if input_name.lower() in lower_case_inputs:
            return float(self.query(":DATA:FRES?"))
        raise Exception("Trying to read from a non existing input : {}".format(input_name))

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
        if name not in property_command_dictionary:
            raise Exception("Unknown property {}".format(name))

        command_to_write = None

        if name == 'Sense':
            if value in IOType:
                value = value.value
            command_to_write = ":SENS:FUNC \"{}\"".format(value)
        elif name == 'Sense Range Voltage':
            if value in SensorRangeVolt:
                value = value.value
            command_to_write = "SENS:VOLT:RANG {}".format(convert_range_to_float(value))
        elif name == 'Sense Range Current':
            if value in SensorRangeCurrent:
                value = value.value
            command_to_write = "SENS:CURR:RANG {}".format(convert_range_to_float(value))
            
        if verbose:
            print("Updating Property : {}:{} with command '{}'".format(name, value, command_to_write))

        if command_to_write is not None:
            self.connection.write(command_to_write)

        #reupdate properties
        self.get_properties()

    def get_properties(self):
        self.properties = self._read_properties()
        return self.properties

    def close(self, *exp):
        self.connection.close()
        if verbose:
            print("Close Connection to Keithley")


    """
        Not Required
    """
    @property
    def current_value(self):
        return self.read_input("DCV/DCC")

    def set_DCV(self):
        self.set_property("Sense", IOType.Voltage)

    def set_DCI(self):
        self.set_property("Sense", IOType.Current)

    #def set_range_by_max_value()


    
