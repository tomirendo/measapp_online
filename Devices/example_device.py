from Device import Device

class ExampleDevice(Device):
    def __init__(self, properties):
        Device.__init__(self) 
        self.connection = None

    def check_connection(self):
        return True 

    def list_inputs(self):
        return ['ADC 1', 'ADC 2']

    def list_outputs(self):
        return ['Port 1', 'Port 2']

    def read_input(self, input_name):
        return 1

    def write_output(self, output_name, value):
        print("Output {} : {}".format(output_name, value))

    def write_raw(self, value):
        print("Raw Output {}".format(value))

    def read_raw(self):
        print("Read Raw")
        return "Read Raw\n" 

    def set_property(self, name, value):
        pass

    def get_properties(self):
        return dict()

    def close(self, *exp):
        print("Closed")




