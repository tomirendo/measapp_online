from Devices.example_device import ExampleDevice
from Devices.duck.duck import Duck
from Devices.Lockin.lockin import Lockin
from Devices.keithley.keithley import Keithley
from Devices.dmm.dmm import DMM

devices = [
        {
        "name" : "Lockin 1", 
        "object" : Lockin,
        "properties" : {
            "port" : "GPIB0::8::INSTR",
            } 
        },
        {
        "name" : "DMM 1", 
        "object" : DMM,
        "properties" : {
            "port" : "GPIB0::26::INSTR",
            } 
        },
        {  
        "name" : "Duck(MAC)",
        "object" : Duck,
        "properties":{
            "port" : "/dev/tty.usbmodem1421",
            "has_adc" : True,
            "frequency" : 17,
            "points" : 80,
            "ramp_time" : 1
            },
        },
        {  
        "name" : "Duck",
        "object" : Duck,
        "properties":{
            "port" : "COM6",
            "has_adc" : True,
            "frequency" : 17,
            "points" : 80,
            "ramp_time" : .1
            },
        },
]
