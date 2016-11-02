from Device import Device, get_enum_value_by_index, get_index_of_enum, list_values_of_enum_type
from itertools import product
from time import sleep
import pyvisa
from enum import Enum
from collections import OrderedDict

verbose = False 

class mock_connection:
    def query(self, *args):
        print("Query : {} ".format(args))       
        if args[0] == '*IDN?':
            return "Stanford_Research_Systems,SR830"
        elif args[0].split(" ")[0].strip() in property_command_dictionary.values():
            return '1'
        else :
            return "0,1,2,3,4"
    def close(self):
        print("Close")


class Input(Enum):
    A = "A"
    I = "I"
    A_MINUS_B = "A-B"

class Sensitivity(Enum):
    nV_2_fA = '2 nV/fA'
    nV_5_fA = '5 nV/fA'
    nV_10_fA = '10  nV/fA'
    nV_20_fA = '20 nV/fA'
    nV_50_fA = '50 nV/fA'
    nV_100_fA = '100  nV/fA'
    nV_200_fA = '200 nV/fA'
    nV_500_fA ='500 nV/fA'
    V_1_pA = '1 μV/pA'
    V_2_pA = '2 μV/pA'
    V_5_pA = '5 μV/pA'
    V_10_pA = '10 μV/pA'
    V_20_pA = '20 μV/pA'
    V_50_pA = '50 μV/pA'
    V_100_pA = '100 μV/pA'
    V_200_pA = '200 μV/pA'
    V_500_pA = '500 μV/pA'
    mV_1_nA = '1 mV/nA'
    mV_2_nA = '2 mV/nA'
    mV_5_nA = '5 mV/nA'
    mV_10_nA = '10 mV/nA'
    mV_20_nA = '20 mV/nA'
    mV_50_nA = '50 mV/nA'
    mV_100_nA = '100 mV/nA'
    mV_200_nA = '200 mV/nA'
    mV_500_nA = '500 mV/nA'
    V_1_A = '1 V/?A'

class TimeConstant(Enum):
    micro_sec_10 ='10 μs'
    micro_sec_30 ='30 μs'
    micro_sec_100 = '100 μs'
    micro_sec_300 = '300 μs'
    mili_sec_1 = '1 ms'
    mili_sec_3 = '3 ms'
    mili_sec_10 = '10 ms'
    mili_sec_30 = '30 ms'
    mili_sec_100 ='100 ms'
    mili_sec_300 = '300 ms'
    sec_1 = '1 s'
    sec_3 = '3 s'
    sec_10 = '10 s'
    sec_30 = '30 s'
    sec_100 = '100 s'
    sec_300 = '300 s'
    kilo_sec_1 = '1 ks'
    kilo_sec_3 = '3 ks'
    kilo_sec_10 = '10 ks'
    kilo_sec_30 = '30 ks'

class Slope(Enum):
    slope_6_dB_oct = '6 dB/oct'
    slope_12_dB_oct = '12 dB/oct'
    slope_18_dB_oct = '18 dB/oct'
    slope_24_dB_oct = '24 dB/oct'

class Coupling(Enum):
    AC = "AC"
    DC = "DC"

class Ground(Enum):
    float = "Float"
    ground = "Ground"

class Filter(Enum):
    none = "None"
    line = "Line"
    line2x = "2X Line"
    line1_plus_2_x = "(1+2)X Line"

class Reserve(Enum):
    high_reserve = "High Reserve"
    normal = "Normal"
    low_noise = "Low Noise"

property_type_dictionary = { "Input" : Input,
                            "Sensitivity" : Sensitivity,
                            "Time Constant" : TimeConstant,
                            "Slope" : Slope,
                            "Coupling" : Coupling,
                            "Ground" : Ground,
                            "Filter" : Filter,
                            "Reserve" : Reserve}

property_command_dictionary = { "Input" : "ISRC",
                            "Sensitivity" : "SENS",
                            "Time Constant" : "OFLT",
                            "Slope" : "OFSL",
                            "Coupling" : "ICPL",
                            "Ground" : "IGND",
                            "Filter" : "ILIN",
                            "Reserve" : "RMOD"}


class Lockin(Device):
    def __init__(self, properties):
        Device.__init__(self) 
        self.inputs = ["x","y","r","phase"]
        self.port = properties['port']
        self.connection = pyvisa.ResourceManager().open_resource(self.port)
        #self.connection = mock_connection() #Mock connection for tests
        self.outputs = []
        self.properties = self._read_properties()

    def _read_properties(self):
        dictionary = OrderedDict()
        for property, command in property_command_dictionary.items():
            data = self.connection.query(command +" ?")
            index = int(data)
            value = get_enum_value_by_index(property_type_dictionary[property], index)
            dictionary[property] = value
        return dictionary


    def check_connection(self):
        return self.connection.query("*IDN?").startswith('Stanford_Research_Systems,SR830')

    def list_outputs(self):
        return self.outputs 

    def list_inputs(self):
        return self.inputs 

    def read_input(self, input_name):
        if input_name in self.inputs:
            input_index = self.inputs.index(input_name)
            result = self.connection.query("SNAP?1,2,3,4").replace("\n","").split(",")
            return float(result[input_index])
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
            text_to_write = "{} {}".format(property_command_dictionary[name], get_index_of_enum(value))
            print(text_to_write)
            self.connection.write(text_to_write)
        else :
            raise Exception("Value isn't of type {}".format(type(property_type_dictionary[name])))


    def get_properties(self):
        self.properties = self._read_properties()
        return self.properties

    def close(self, *exp):
        self.connection.close()

    """
    This part is not required

    """
    @property
    def x(self):
        return self.read_input("x")        

    @property
    def y(self):
        return self.read_input("y")
    
    @property
    def r(self):
        return self.read_input("r")

    @property
    def phase(self):
        return self.read_input("phase")

    @property
    def nx(self):
        return self.read_input("nx")
    
