### Installing Devices
Install using these commands:

	cd PYTHON_DIR/Lib/site-packages
	git clone https://github.com/tomirendo/measapp_online
	mv measapp_online devices

And you are done!

Running the web server:
	
	python -m devices.application


Opening up devices:
	
	from devices import devices
	devs = devices()
	devs.open()

Closing devices:

	devs.close()

Alternativly:
	
	with devices() as devs:
		#Do Stuff



### Structure

#### Accessing a device

The devs object is an ordered dictionary of device objects. For example you my run:

	>> devs
	devices([('Lockin 2', <devices.Devices.Lockin.lockin.Lockin at 0x485bbb0>),
		('Keithley',
		<devices.Devices.keithley.keithley.Keithley at 0x3978030>),
		('DMM', <devices.Devices.dmm.dmm.DMM at 0x4bd45f0>),
		('Duck (with display)',
		<devices.Devices.duck.duck.Duck at 0x4bd4610>)])

In this case you can access the lockin by typing devs['Lockin 2']. 
Since this is an ordered dictionary you can quickly assign all of the devices to a variable:

	lockin, keithley, dmm, duck = devs

From this point on I would write "dmm.property" assuming the variable "dmm" contains a dmm object from the devs dictionary.


#### Standard Functionality 

Every single device implements a set of standard functions. These standard functions should enable all the device functionality, but are a bit tedious to actually use. The standard functions enable a standard access for external objects to the devices library. 

    def __init__(self, properties):
        Device.__init__(self) 
        self.connection = None

The device.check_connection() method checks the identity of the connected device, and returns True if the device is properly connected.

    def check_connection(self)

The device.list_inputs() method returns a list of stringing representing all the inputs of the device. You can access their current value using the device.read_input(input_name) method.

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