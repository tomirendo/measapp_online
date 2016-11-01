from Devices.example_device import ExampleDevice
from Devices.duck.duck import Duck
from Devices.Lockin.lockin import Lockin

devices = [
        {
        "name" : "Example Device 1", 
        "object" : ExampleDevice,
        "properties" : {
            "buad" : 1,
            "communication_port" : "1",
            } 
        },
        {
        "name" : "Lockin 1", 
        "object" : Lockin,
        "properties" : {
            "port" : "GPIB0::8::INSTR",
            } 
        },
        {  
        "name" : "Duck",
        "object" : Duck,
        "properties":{
            "port" : "/dev/tty.usbmodem1421",
            "has_adc" : True,
            "frequency" : 17,
            "points" : 80,
            "ramp_time" : 1
        },
        },
        
        
    ]
