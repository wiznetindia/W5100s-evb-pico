# W5100s-evb-pico
Wiznet's W5100s-EVB-PICO and Peizo Buzzer will paying the musical notes of selected song via PWM controlling in Web Server

W5100S-EVB-Pico pinout is directly connected to the GPIO of RP2040 as shown in the picture above. It has the same pinout as the Raspberry Pi Pico board. However, GPIO16, GPIO17, GPIO18, GPIO19, GPIO20, GPIO21 are connected to W5100S inside the board. These pins enable SPI communication with W5100S to use Ethernet function. If you are using the Ethernet function, these pins cannot be used for any other purpose.

For getting started with W5100s-EVB-PICO board refer the link 
https://github.com/Wiznet/RP2040-HAT-CircuitPython/blob/master/Ethernet%20Example%20Getting%20Started%20%5BCircuitpython%5D.md

Connections

Connecting the Buzzer one End to GND(Ground) pin of EVB and one end to GPIO3(pin number 5) of EVB.
