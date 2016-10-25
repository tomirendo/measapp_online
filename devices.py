from devices_properties import devices as _devices
#Converts dictionary to objects
from PhysicalDeviceObject import PhysicalDeviceObject

class devices(list):
    def __init__(self):
        list.__init__(self)

    def __enter__(self):
        for device in _devices:
            try :
                physical_device = PhysicalDeviceObject(device)
                self.append(physical_device)
            except Exception as e:
                 print("Cannot Initiate device {} : {}".format(device.get('name'), e))
        return self
        
    def get_device(self, name):
        for d in self:
            if d.name == name:
                return d

    def __exit__(self, *exp):
        for device in self:
            try:
                device.object.close(*exp)
                print("Closed Device : {}".format(device.name))
            except Exception as e:
                print("Cannot Close Device {} : {}".format(device.name, e))




"""
def devices():
    devices = []
    for device in _devices:
        try :
            physical_device = PhysicalDeviceObject(device)
            devices.append(physical_device)
        except Exception as e:
            print("Cannot Initiate device {} : {}".format(device.get('name'), e))
    global all_devices
    all_devices = list(devices)
    return devices

def close_devices(*exp):
    global all_devices
    for device in _devices:
        try:
            device.object.close(*exp)
            print("Closed Device : {}".format(device.name))
        except Exception as e:
            print("Cannot Close Device {} : {}".format(device.name, e))


"""

