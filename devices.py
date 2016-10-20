from example_device import ExampleDevice

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
        }
    ]

#Converts dictionary to objects
from PhysicalDeviceObject import PhysicalDeviceObject
devices = [PhysicalDeviceObject(i) for i in devices]