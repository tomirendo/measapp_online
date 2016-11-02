from devices_properties import devices as _devices
devices_instance = None

class devices(dict):
    def __init__(self):
        global devices_instance
        if devices_instance is not None:
            devices_instance.close()

        devices_instance = self


        dict.__init__(self)
        for device in _devices:
            try :
                a_device = device['object'](device.get("properties",{}))
                self[device['name']] = a_device
            except Exception as e:
                 print("Cannot Initiate device {} : {}".format(device.get('name'), e))



    def __enter__(self):
        return self
        
    def get_device(self, name):
        return self[name]

    def __exit__(self, *exp):
        for name, device in self.items():
            try:
                device.close(*exp)
                print("Closed Device : {}".format(name))
            except Exception as e:
                print("Cannot Close Device {} : {}".format(name, e))

    def open(self):
        self.__enter__()
    def close(self):
        self.__exit__(None)
