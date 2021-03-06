![inverters image](https://energypower.gr/wp-content/uploads/2015/12/inverter-axpert-mks-5-kva.jpg)
================

This is a Hassio addon to monitor [voltronic axpert inverters](http://www.voltronicpower.com/oCart2/index.php?route=product/product&product_id=123) through USB and publish the data as JSON to an MQTT broker. It publishes the data to 2 topics:
- 'power/axpert' for the parallel data (some of these values seem to be only for the connected inverter even though they are returned by the parallel data command)
- 'power/axpert{sn}' for the data from the connected inverter (configurable, {sn} is replaced with the serial number of the inverter)

You can then configure the sensors in Home Assistant like this:
```
sensors:
  - platform: mqtt
    name: "Power"
    state_topic: "power/axpert"
    unit_of_measurement: 'W'
    value_template: "{{ value_json.TotalAcOutputActivePower }}"
    expire_after: 60
```

The values published on 'power/axpert' are:
- SerialNumber # of the first inverter in the parallel setup
- TotalAcOutputActivePower
- TotalAcOutputApparentPower
- TotalAcOutputPercentage
- BatteryChargingCurrent
- BatteryDischargeCurrent
- TotalChargingCurrent
- GridVoltage
- GridFrequency
- OutputVoltage
- OutputFrequency
- OutputAparentPower
- OutputActivePower
- LoadPercentage
- BatteryVoltage
- BatteryCapacity
- PvInputVoltage
- OutputMode
- ChargerSourcePriority
- MaxChargeCurrent
- MaxChargerRange
- MaxAcChargerCurrent
- PvInputCurrentForBattery
- Gridmode
- Solarmode

The values published on 'power/axpert{sn}' are:
- BusVoltage
- InverterHeatsinkTemperature
- BatteryVoltageFromScc
- PvInputCurrent
- PvInputVoltage
- PvInputPower
- BatteryChargingCurrent
- BatteryDischargeCurrent
- DeviceStatus

I have 3 inverters in parallel and a raspberry connected to 1 of them with a USB cable . Linux doesn't seem to recognize it as a USB to Serial device and it only shows up as `/dev/hidraw0`.

A description of the serial communication protocol can be found [here](file:///home/freon/Downloads/HS_MS_MSX-Communication%20Protocol-NEW.pdf)


### Rules for the HIDRAW device


Devices from Voltronic are shipped with 4 possible hardware interfaces: RS232, USB, Bluetooth & RS485

All the interfaces share the same underlying communication protocol


The Axpert is an HIDRAW device.  It requires the following rule to set up in order to give the active user to access the device:

`echo 'ATTRS{idVendor}=="0665", ATTRS{idProduct}=="5161", SUBSYSTEMS=="usb", ACTION=="add", MODE="0666", GROUP="root", SYMLINK+="hidVoltronic"' > /etc/udev/rules.d/35-voltronic.rules`

This command requires root access.  On a raspberry pi use the command:

`sudo su`

and then echo the contents to the udev rule file.

### Simultaneous communication across multiple interfaces

During testing it was found that simultaneous communication across USB & RS232 for example would result in device lockup. The device keeps operating, but the device will no longer respond to input or produce output.

As such it is advised to pick an interface and use it exclusively.

An example of this is trying to communicate simultaneously to a Pylontech battery and an Axpert inverter.  Lockup will occur and then neither device will respond.

### Protocol

This section is heavily borrowed from 

https://github.com/jvandervyver/libvoltronic

## Communication protocol
The communication protocol consists of the following format:

**Overall the protocol has the following format:**

`{bytes}{CRC16}{end of input character}`
- **bytes** the actual bytes being sent to the device, generally speaking this is the *"command"*
- **CRC16** common CRC protocol with many implementations online
- **end of input character** character signaling the end of input

### Reserved characters
These characters are reserved
- `\r` (*0x0d*) End of input character
- `(` (*0x28*) Seems to indicate start of input
- `\n` (*0x0a*) No material importance but still reserved

### Bytes
The bytes being sent to the device appear to be simply ASCII in the form of a command

Multiple documents exist listing possible commands
 - [Axpert](https://s3-eu-west-1.amazonaws.com/osor62gd45llv5fcg47yijafsz6dcrjn/HS_MS_MSX_RS232_Protocol_20140822_after_current_upgrade.pdf)
 - [Infini Solar](https://s3-eu-west-1.amazonaws.com/osor62gd45llv5fcg47yijafsz6dcrjn/Infini_RS232_Protocol.pdf)

### CRC
The CRC is used is the [CRC16 XMODEM](https://pycrc.org/models.html#xmodem) variation

**Background**

Multiple methods exist to [generate CRC](https://en.wikipedia.org/wiki/Computation_of_cyclic_redundancy_checks).

CRC16 as the name implies contains 16 bits or 2 bytes of data.
It is commonly written as hexadecimal for readability reason, ie> `0x17AD`

Two hexadecimal character represent a single byte so given the example above.
`0x` part simply indicates hexadecimal
`0x17` is the first byte
`0xAD` is the second byte

**Exception**

The **Reserved characters** are not allowed in the CRC.
It appears the device simply expects them to be incremented by 1

So `0x28` becomes `0x29`, `0x0d` becomes `0x0e`, etc.

### End of input character
The `\r` character signals to the device end of input

Regardless of what the device received up to that point `\r` signals to the device end of current input

Once this character is received all input up to that point is taken as the *command* to the device

