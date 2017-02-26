from devices.Devices.example_device import ExampleDevice
from devices.Devices.duck.duck import Duck
from devices.Devices.Lockin.lockin import Lockin
from devices.Devices.keithley.keithley import Keithley
from devices.Devices.dmm.dmm import DMM

devices = [
        {
        "name" : "Lockin 1", 
        "object" : Lockin,
        "properties" : {
            "port" : "GPIB0::8::INSTR",
        }
        },
        {
        "name" : "DMM 26", 
        "object" : DMM,
        "properties" : {
            "port" : "GPIB0::26::INSTR",
            } 
        },
        {
        "name" : "DMM 16", 
        "object" : DMM,
        "properties" : {
            "port" : "GPIB0::16::INSTR",
            } 
        },
        # {
        # "name" : "Keithley", 
        # "object" : Keithley,
        # "properties" : {
        #     "port" : "GPIB0::27::INSTR",
        #     } 
        # },
        # { "name" : "Example Device",
        #   "object" : ExampleDevice,
        #   "properties" : {
        #   }
        # },
        {
        "name" : "Lockin 2", 
        "object" : Lockin,
        "properties" : {
            "port" : "GPIB0::8::INSTR",
            } 
        },
        # {
        # "name" : "Keithley 27", 
        # "object" : Keithley,
        # "properties" : {
        #     "port" : "GPIB0::27::INSTR",
        #     } 
        # },
        # {
        # "name" : "Keithley 24", 
        # "object" : Keithley,
        # "properties" : {
        #     "port" : "GPIB0::27::INSTR",
        #     } 
        # },
        {  
        "name" : "DAC (with ADC)",
        "object" : Duck,
        "properties":{
            "port" : "COM6",
            "has_adc" : True,
            "frequency" : 17,
            "points" : 80,
            "ramp_time" : .1
            },
        },
        {  
        "name" : "DAC (with display)",
        "object" : Duck,
        "properties":{
            "port" : "COM9",
            "has_adc" : False,
            "frequency" : 17,
            "points" : 80,
            "ramp_time" : .1
            },
        },
]
