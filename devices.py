from devices_properties import devices as _devices

#Converts dictionary to objects
from PhysicalDeviceObject import PhysicalDeviceObject
devices = []
for device in _devices:
    try :
        physical_device = PhysicalDeviceObject(device)
        devices.append(physical_device)
    except Exception as e:
        print("Cannot Initiate device {} : {}".format(device.get('name'), e))


def close_devices(*exp):
    for device in devices:
        try:
            device.object.close(*exp)
            print("Closed Device : {}".format(device.name))
        except Exception as e:
            print("Cannot Close Device {} : {}".format(device.name, e))



