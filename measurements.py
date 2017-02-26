import numpy 
import os
import csv
from time import sleep
import matplotlib.pyplot as plt

class Output:
    def __init__(self, dictionary, device_finder = lambda x:x):
        self.begin_value = dictionary['begin_value']
        self.end_value = dictionary['end_value']
        self.output = dictionary['output']
        self.device = device_finder(dictionary['name'])
        self.steps = int(dictionary['steps'])

    def set(self, value):
        self.device.object.write_output(self.output, value)

    def to_dict(self):
        return {"begin_value" : self.begin_value,
                "end_value" : self.end_value,
                "output" : self.output,
                "device" : self.device.name,
                "steps" : self.steps}


class Input:
    def __init__(self, dictionary, device_finder = lambda x:x):
        self.input = dictionary['input']
        self.device = device_finder(dictionary['name'])

    def get(self):
        return self.device.object.read_input(self.input)

    def to_dict(self):
        return {"input" : self.input,
                "device": self.device.name}

class Measurement:
    def __init__(self, dictionary, device_finder=lambda x:x, path="."):
        self.name = dictionary['name']
        self.step_time = float(dictionary['step_time'])
        self.inputs = [Input(i, device_finder) for i in dictionary['measurements']]
        self.outputs = [Output(i, device_finder) for i in dictionary['outputs']]
        self.running = False
        self.results = []
        self.range = []
        self.path = path
        for output in self.outputs:
            if output.device.is_locked and output.device.owner != id(self):
                raise Exception("Cannot use output device {}. Device is used by another measurement".format(output.device.name))
            output.device.owner = id(self)
            output.device.is_locked = True

    def end_measurement(self):
        for output in self.outputs:
            if id(self) == output.device.owner :
                output.device.is_locked = False

    def save_measurement(self, exception = False):
        if exception: 
            filename = self.name + ".error.csv"
        else :
            filename = self.name + ".csv"

        full_path = os.path.join(self.path, filename)

        with open(full_path, "w") as f:
            writer = csv.writer(f)
            writer.writerows(self.results)

    def run(self):
        try : 
            self.running = True
            if len(self.outputs) != 1:
                raise Exception("Not ready yet")
            output = self.outputs[0]
            self.range = numpy.linspace(float(output.begin_value), float(output.end_value), int(output.steps))
            self.results = [(None,) * (1+len(self.inputs))]*output.steps
            for index, value in enumerate(self.range):
                if self.running: #self.running value can change while this is running to stop the measurement
                    output.set(value)
                    sleep(self.step_time)
                    self.results[index] = [value] + [i.get() for i in self.inputs]
                    self.save_measurement()
                    print(self.results[index])
            self.running = False
            self.end_measurement()

        except Exception as e:
            self.save_measurement(exception = True)
            print("Stoped measurement : {}\nBecause of an Error:{}\n".format(self.name, e))

    def to_dict(self):
        return {"running" : self.running,
                "outputs" : [i.to_dict() for i in self.outputs],
                "inputs" : [i.to_dict() for i in self.inputs],
                "results" : self.results,
                "step_time" : self.step_time,
                "name" : self.name,
                "range" : list(self.range)
                }

    def to_graph(self, input_index, to_differentiate = False):
        X, *Ys = zip(*self.results)
        plt.plot(X, Ys[input_index])
        file_name = "temp_{}_{}.png".format(id(self), input_index)
        plt.savefig(file_name)
        plt.clf()
        return os.path.abspath(file_name)
