from Devices.example_device import ExampleDevice
from Devices.duck.duck import Duck
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
        "name" : "Example Device 2", 
        "object" : ExampleDevice,
        "properties" : {
            "buad" : 1,
            "communication_port" : "2",
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
