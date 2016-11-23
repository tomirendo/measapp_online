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



## Structure

### Accessing a device

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


### Standard Functionality 

Every single device implements a set of standard functions. These standard functions should enable all the device functionality, but are a bit tedious to actually use. The standard functions enable a standard access for external objects to the devices library. 

    def __init__(self, properties):

The device.check_connection() method checks the identity of the connected device, and returns True if the device is properly connected.

    def check_connection(self)

The device.list_inputs() method returns a list of stringing representing all the inputs of the device. You can access their current value using the device.read_input(input_name) method.

    def list_inputs(self):

device.list_outputs() returns a list of strings representing all of the available outputs of the device.

    def list_outputs(self):

device.read_input() reads the current value of a given input by name. You can find all the available inputs using the device.list_inputs() function.

    def read_input(self, input_name):

device.write_output(output_name, value) sets the value of an output. You can find all the available outpus using the device.list_outputs() methods.

    def write_output(self, output_name, value):

Write raw string to a device.

    def write_raw(self, value):

Read raw string for a device

    def read_raw(self):

Set a value to a property. Properties can either by a number, a string or an Enum. 

    def set_property(self, name, value):

Returns a dictionary representing the properties of the device.

    def get_properties(self):

Close connection to a device.

    def close(self, *exp):

