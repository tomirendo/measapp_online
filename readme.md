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

Alternativly:
	
	with devices() as devs:
		#Do Stuff

