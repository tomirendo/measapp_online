from Device import Device

class ExampleDevice(Device):
    def __init__(self, properties):
        Device.__init__(self) 
        self.connection = None

    def check_connection(self):
        return True 

    def list_inputs(self):
        return ['Port 1', 'Port 2']

    def list_outputs(self):
        return ['ADC 1', 'ADC 2']

    def read_input(self, input_name):
        return 1

    def write_output(self, output_name, value):
        print("Output {} : {}".format(output_name, value))



