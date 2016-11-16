from devices.Devices.example_device import ExampleDevice
from devices.Devices.duck.duck import Duck
from devices.Devices.Lockin.lockin import Lockin
from devices.Devices.keithley.keithley import Keithley
from devices.Devices.dmm.dmm import DMM

devices = [
        #{
        #"name" : "Lockin 1", 
        #"object" : Lockin,
        #"properties" : {
        #    "port" : "GPIB0::8::INSTR",
        #    } 
        #},
        #{
        #"name" : "DMM 1", 
        #"object" : DMM,
        #"properties" : {
        #    "port" : "GPIB0::26::INSTR",
        #    } 
        #},
        #{
        #"name" : "Keithley", 
        #"object" : Keithley,
        #"properties" : {
        #    "port" : "GPIB0::27::INSTR",
        #    } 
        #},
        {
        "name" : "Keithley", 
        "object" : Keithley,
        "properties" : {
            "port" : "GPIB0::27::INSTR",
            } 
        },
        {
        "name" : "DMM", 
        "object" : DMM,
        "properties" : {
            "port" : "GPIB0::16::INSTR",
            } 
        },
        #{  
        #"name" : "Duck",
        #"object" : Duck,
        #"properties":{
        #    "port" : "COM6",
        #    "has_adc" : True,
        #    "frequency" : 17,
        #    "points" : 80,
        #    "ramp_time" : .1
        #    },
        #},
]
