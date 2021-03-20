
## lsusb
...
Bus 001 Device 052: ID 0557:2406 ATEN International Co., Ltd 
Bus 001 Device 051: ID 1a40:0101 Terminus Technology Inc. Hub

## lsusb -d 0557:2406 -v

Bus 001 Device 088: ID 0557:2406 ATEN International Co., Ltd 
Couldn't open device, some information will be missing
Device Descriptor:
  bLength                18
  bDescriptorType         1
  bcdUSB               1.10
  bDeviceClass            0 
  bDeviceSubClass         0 
  bDeviceProtocol         0 
  bMaxPacketSize0         8
  idVendor           0x0557 ATEN International Co., Ltd
  idProduct          0x2406 
  bcdDevice           31.02
  iManufacturer           1 
  iProduct                2 
  iSerial                 0 
  bNumConfigurations      1
  Configuration Descriptor:
    bLength                 9
    bDescriptorType         2
    wTotalLength       0x003b
    bNumInterfaces          2
    bConfigurationValue     1
    iConfiguration          0 
    bmAttributes         0x80
      (Bus Powered)
    MaxPower              200mA
    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        0
      bAlternateSetting       0
      bNumEndpoints           1
      bInterfaceClass         3 Human Interface Device
      bInterfaceSubClass      0 
      bInterfaceProtocol      1 Keyboard
      iInterface              0 
        HID Device Descriptor:
          bLength                 9
          bDescriptorType        33
          bcdHID               1.10
          bCountryCode            0 Not supported
          bNumDescriptors         1
          bDescriptorType        34 Report
          wDescriptorLength      63
         Report Descriptors: 
           ** UNAVAILABLE **
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x81  EP 1 IN
        bmAttributes            3
          Transfer Type            Interrupt
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0008  1x 8 bytes
        bInterval             255
    Interface Descriptor:
      bLength                 9
      bDescriptorType         4
      bInterfaceNumber        1
      bAlternateSetting       0
      bNumEndpoints           1
      bInterfaceClass         3 Human Interface Device
      bInterfaceSubClass      0 
      bInterfaceProtocol      0 
      iInterface              0 
        HID Device Descriptor:
          bLength                 9
          bDescriptorType        33
          bcdHID               1.10
          bCountryCode            0 Not supported
          bNumDescriptors         1
          bDescriptorType        34 Report
          wDescriptorLength      76
         Report Descriptors: 
           ** UNAVAILABLE **
      Endpoint Descriptor:
        bLength                 7
        bDescriptorType         5
        bEndpointAddress     0x82  EP 2 IN
        bmAttributes            3
          Transfer Type            Interrupt
          Synch Type               None
          Usage Type               Data
        wMaxPacketSize     0x0008  1x 8 bytes
        bInterval              50

## dmesg
usb 1-3: new full-speed USB device number 59 using xhci_hcd
usb 1-3: New USB device found, idVendor=0557, idProduct=2406, bcdDevice=31.02
usb 1-3: New USB device strings: Mfr=1, Product=2, SerialNumber=0
usb 1-3: Product: USB 2.0 Peripheral Switch
usb 1-3: Manufacturer: USB 2.0 Peripheral Switch
input: USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch as /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0/0003:0557:2406.004B/input/input61
hid-generic 0003:0557:2406.004B: input,hidraw4: USB HID v1.10 Keyboard [USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch] on usb-0000:00:14.0-3/input0
hid-generic 0003:0557:2406.004C: hidraw5: USB HID v1.10 Device [USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch] on usb-0000:00:14.0-3/input1
usb 1-3: USB disconnect, device number 59
==> Pause of 1s
usb 1-3: new high-speed USB device number 60 using xhci_hcd
usb 1-3: New USB device found, idVendor=1a40, idProduct=0101, bcdDevice= 1.11
usb 1-3: New USB device strings: Mfr=0, Product=1, SerialNumber=0
usb 1-3: Product: USB 2.0 Hub
hub 1-3:1.0: USB hub found
hub 1-3:1.0: 4 ports detected
usb 1-3.2: new full-speed USB device number 61 using xhci_hcd
usb 1-3.2: New USB device found, idVendor=0557, idProduct=2406, bcdDevice=31.02
usb 1-3.2: New USB device strings: Mfr=1, Product=2, SerialNumber=0
usb 1-3.2: Product: USB 2.0 Peripheral Switch
usb 1-3.2: Manufacturer: USB 2.0 Peripheral Switch
input: USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch as /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3.2/1-3.2:1.0/0003:0557:2406.004D/input/input62
hid-generic 0003:0557:2406.004D: input,hidraw4: USB HID v1.10 Keyboard [USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch] on usb-0000:00:14.0-3.2/input0
hid-generic 0003:0557:2406.004E: hidraw5: USB HID v1.10 Device [USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch] on usb-0000:00:14.0-3.2/input1


==>
/dev/hidraw4
/dev/hidraw5
/sys/bus/usb/devices/1-3.2
/sys/bus/usb/devices/1-3.2:1.0
/sys/bus/usb/devices/1-3.2:1.1
/sys/bus/usb/drivers/usbhid/1-3.2:1.0
/sys/bus/usb/drivers/usbhid/1-3.2:1.1
/sys/bus/usb/drivers/usb/1-3.2


## Connected to port 4, plug in
dmesg --follow
[122066.425337] input: USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch as /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3.2/1-3.2:1.0/0003:0557:2406.0069/input/input76
[122066.484269] hid-generic 0003:0557:2406.0069: input,hidraw4: USB HID v1.10 Keyboard [USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch] on usb-0000:00:14.0-3.2/input0
[122066.486578] hid-generic 0003:0557:2406.006A: hidraw5: USB HID v1.10 Device [USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch] on usb-0000:00:14.0-3.2/input1

## Connected to port 3, plug in
[122130.522954] input: USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch as /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3.2/1-3.2:1.0/0003:0557:2406.006D/input/input78
[122130.580721] hid-generic 0003:0557:2406.006D: input,hidraw4: USB HID v1.10 Keyboard [USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch] on usb-0000:00:14.0-3.2/input0
[122130.583244] hid-generic 0003:0557:2406.006E: hidraw5: USB HID v1.10 Device [USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch] on usb-0000:00:14.0-3.2/input1

## Connected to port 4, plug in
[122188.856669] input: USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch as /devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3.2/1-3.2:1.0/0003:0557:2406.0071/input/input80
[122188.917057] hid-generic 0003:0557:2406.0071: input,hidraw4: USB HID v1.10 Keyboard [USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch] on usb-0000:00:14.0-3.2/input0
[122188.919711] hid-generic 0003:0557:2406.0072: hidraw5: USB HID v1.10 Device [USB 2.0 Peripheral Switch USB 2.0 Peripheral Switch] on usb-0000:00:14.0-3.2/input1
