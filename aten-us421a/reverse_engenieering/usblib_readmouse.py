# https://www.orangecoat.com/how-to/read-and-decode-data-from-your-mouse-using-this-pyusb-hack

#!/usr/bin/python
import time
import sys
import usb.core
import usb.util
# decimal vendor and product values
dev = usb.core.find(idVendor=0x0557, idProduct=0x2406)
# dev = usb.core.find(idVendor=0x046d, idProduct=0xc077) # Logitech Mouse
# or, uncomment the next line to search instead by the hexidecimal equivalent
#dev = usb.core.find(idVendor=0x45e, idProduct=0x77d)
# first endpoint
interface = 0
endpoint = dev[0][(0,0)][0]
# endpoint = dev[0][(0,0)][1]  # OUT
# endpoint = dev[0][(1,0)][0]
# if the OS kernel already claimed the device, which is most likely true
# thanks to http://stackoverflow.com/questions/8218683/pyusb-cannot-set-configuration
if dev.is_kernel_driver_active(interface) is True:
  # tell the kernel to detach
  print('dev.detach_kernel_driver')
  dev.detach_kernel_driver(interface)
  # claim the device
  usb.util.claim_interface(dev, interface)
collected = 0
attempts = 10
while collected < attempts :
    time.sleep(0.1)
    try:
        collected += 1
        data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        print(data)
    except usb.core.USBError as e:
        print(f'Error {e}')
        data = None
        if e.args == ('Operation timed out',):
            continue
# release the device
usb.util.release_interface(dev, interface)
# reattach the device to the OS kernel
print('dev.attach_kernel_driver')
dev.attach_kernel_driver(interface)
