from Device import Device
from Devices.duck.myserial import Duck as DuckConnection
from itertools import product

class mock_connection:
    def __init__(self, *args):
        pass
    def run(self, *args,**kwargs):
        print("Mock Connection",args)
        return "READY"
    def __enter__(self):
        pass
    def __exit__(self, *exp):
        pass

class Duck(Device):
    def __init__(self, properties):
        Device.__init__(self) 
        print(properties)
        self.port = properties['port']
        self.has_adc = properties['has_adc']
        self.frequency = properties['frequency']
        self.points = properties['points']
        self.ramp_time = properties['ramp_time']
        self.connection = mock_connection(self.port, 115200) 
        #self.connection = DuckConnection(self.port, 115200)
        self.connection.__enter__()
        self.outputs = [" ".join([i,j]) for i,j in product(['Port 0','Port 1', 'Port 2','Port 3'], ['AC','DC'])]
        if self.has_adc:
            self.inputs = ['ADC 0','ADC 1', 'ADC 2','ADC 3']
        else :
            self.inputs = []
        self.properties = ['Frequency (Hz)','Points On Graph','Ramp Time (V/S)']
        self._update_sine_function()

    def _update_sine_function(self):
        self.connection.run("SINE,{},{},{}".format(self.frequency, self.points, self.ramp_time), verbose=True)

    def check_connection(self):
        return "READY" == self.connection.run("*RDY?")

    def list_outputs(self):
        return self.outputs 

    def list_inputs(self):
        return self.inputs 

    def read_input(self, input_name):
        if has_adc and input_name in self.inputs:
            return self.connection.run("GET_ADC,{}".format(self.inputs.find(input_name)))
        raise Exception("Trying to read from non existing port")

    def write_output(self, output_name, value):
        port = self.outputs.find(output_name)//2
        if "AC" in output_name : 
            self.connection.run("AC {}:{}".format(float(value), port), read=False)
        elif "DC" in output_name:
            self.connection.run("DC {}:{}".format(float(value), port), read=False)
        else :
            raise Exception("Unknown Output")

    def write_raw(self, value):
        self.connection.run(value, read=False)

    def read_raw(self):
        return self.connection.serial_device.readline().decode()

    def set_property(self, name, value):
        begin_data = self.frequency, self.points, self.ramp_time 
        if name in self.properties:
            if name == self.properties[0]: 
                self.frequency = float(value)
            elif name == self.properties[1]:
                self.points = int(value)
            elif name == self.properties[2]: 
                self.ramp_time = float(value)

            if begin_data != (self.frequency, self.points, self.ramp_time):
                self._update_sine_function()
        else :
            raise Exception("Unknown Property to set")

    def get_properties(self):
        return dict(zip(self.properties, [self.frequency, self.points, self.ramp_time]))

    def close(self, *exp):
        self.connection.__exit__(*exp)

