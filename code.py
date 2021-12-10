import board
import busio
import digitalio
import analogio
import time
from analogio import AnalogIn
from adafruit_wiznet5k.adafruit_wiznet5k import *
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
import adafruit_requests as requests
import adafruit_wiznet5k.adafruit_wiznet5k_wsgiserver as server
from adafruit_wsgi.wsgi_app import WSGIApp

import pwmio


# Define a list of tones/music notes to play.
TONE_FREQq = [
            330,
             
			440,
             
			494,
             
			523,
             
			440,
			440,
			 
			
			330,
             
			440,
             
			494,
             
			523,
             
			440,
			440,
			 
			
			330,
             
			440,
             
			494,
             
			523,
            523,
             
            
            494,
             
			440,
             
            523,
             
			494,
             
			440,
			659,
			659,
			 
			
			659,
             
			587,
             
			659,
             
			698,
            698,
			698,
			 
			
			698,
             
			659,
             
			587,
             
			698,
             
			659,
			659,
			 
			
			659,
             
			587,
             
			523,
             
			493,
             
			659,
             
			493,
             
			523,
             
			440,
			440] #// Bella ciao
              
              
TONE_FREQ = [ 
            330,
            330,
            111,
            330,
            494,
            111,
            440,
            494,
            111,
            392,
            111,
            440,
            111,
            523,
            111,
            494,
            494,
            494,
            
            330,
            111,
            330,
            330,
            111,
            494,
            111,
            440,
            111,
            494,
            111,
            392,
            440,
            111,
            392,
            111,
            370,
            370,
            370,
            
            330,
            111,
            370,
            294,
            111,
            330,
            111,
            370,
            294,
            111,
            330,
            111,
            392,
            111,
            330,
            330,
            330,


            330,
            370,
            111,
            294,
            111,
            330,
            111,
            370,
            111,
            294,
            111,
            392,
            111,
            370,
            111,
            330]

##SPI0
SPI0_SCK = board.GP18
SPI0_TX = board.GP19
SPI0_RX = board.GP16
SPI0_CSn = board.GP17

##reset
W5x00_RSTn = board.GP20
## ADC
potentiometer = AnalogIn(board.GP28)


buzzer = pwmio.PWMOut(board.GP3, variable_frequency=True)
buzzer.duty_cycle = 0
print("Wiznet5k WebServer Test(DHCP)")

# Setup your network configuration below
# random MAC, later should change this value on your vendor ID
MY_MAC = (0x00, 0x01, 0x02, 0x03, 0x04, 0x05)
IP_ADDRESS = (192, 168, 1, 19)
SUBNET_MASK = (255, 255, 255, 0)
GATEWAY_ADDRESS = (192, 168, 1, 1)
DNS_SERVER = (8, 8, 8, 8)

led = digitalio.DigitalInOut(board.GP25)  #GP25
led.direction = digitalio.Direction.OUTPUT

ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
ethernetRst.direction = digitalio.Direction.OUTPUT

# For Adafruit Ethernet FeatherWing
cs = digitalio.DigitalInOut(SPI0_CSn)

# cs = digitalio.DigitalInOut(board.D5)
spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)

# Reset W5500 first
ethernetRst.value = False
time.sleep(1)
ethernetRst.value = True

# Initialize ethernet interface without DHCP
# eth = WIZNET5K(spi_bus, cs, is_dhcp=False, mac=MY_MAC, debug=False)
# Initialize ethernet interface with DHCP
eth = WIZNET5K(spi_bus, cs, is_dhcp=False, mac=MY_MAC, debug=False)

# Set network configuration
eth.ifconfig = (IP_ADDRESS, SUBNET_MASK, GATEWAY_ADDRESS, DNS_SERVER)

print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))

# Initialize a requests object with a socket and ethernet interface
requests.set_socket(socket, eth)

# Here we create our application, registering the
# following functions to be called on specific HTTP GET requests routes
web_app = WSGIApp()

html_string = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RaspberryPi Pico Web server - WIZnet W5100S/W5500</title>
</head>
<body>
<div align="center">
<H1>RaspberryPi Pico Web server & WIZnet Ethernet HAT</H1>
<h2>Network Information</h2>
<p>
Chip Version is $CHIPNAME<br>
My IP address is $IPADDRESS<br>
</p>
<h2>MUSIC PLAYER Via Buzzer in PICO</h2>
<p>
<label for="led_on"></label><a href="/led_on" id="led_on">  press for Play Music DDLJ </a><br>
</p>
<p>
<label for="led_off"></label><a href="/led_off" id="led_off"> press for Play Music Bella Ciao </a><br>
</p>
</div>
</body>
</html>
'''

#type(potentiometer.value)
#def get_voltage(pin):
#return (pin.value * 3.3) / 66536

#print((converted_num,))
#convertwd_num = "% s" % potentiometer.value
convertwd_num = "% s" % ((potentiometer.value * 3.3) / 66536)
print((convertwd_num,))
html_string = html_string.replace("$CHIPNAME",eth.chip)
html_string = html_string.replace("$IPADDRESS",eth.pretty_ip(eth.ip_address))
#HTTP Request handlers
@web_app.route("/led_on")
def led_on(request):  # pylint: disable=unused-argument
    print("Playing music 1 on!")
    led.value = True
    

    buzzer.frequency = TONE_FREQ[0]
    buzzer.duty_cycle = 2**15 
    converted_num = "% s" % ((potentiometer.value * 3.3) / 66536)
    for i in range(len(TONE_FREQ)):
        if(TONE_FREQ[i] == 111):
            buzzer.duty_cycle = 0
            buzzer.frequency = TONE_FREQ[i]
           # time.sleep(0.5)
        else:
            buzzer.duty_cycle = 2**15
            buzzer.frequency = TONE_FREQ[i]
            time.sleep(0.5)
            
             # Half second delay.
    # Then play tones going from end to start of list.
    buzzer.duty_cycle = 0   
    return ("100 OK", [], "Music 1 Ended")
	
@web_app.route("/led_off")
def led_off(request):  # pylint: disable=unused-argument
	print("Playing music 2!")
	led.value = False
        buzzer.duty_cycle = 2**15
        for i in range(len(TONE_FREQq)):
            if(TONE_FREQq[i] == 111):
                buzzer.duty_cycle = 0
                buzzer.frequency = TONE_FREQq[i]
           # time.sleep(0.5)
            else:
                buzzer.duty_cycle = 2**15
                buzzer.frequency = TONE_FREQq[i]
                time.sleep(0.5)
            
             # Half second delay.
    # Then play tones going from end to start of list.
        buzzer.duty_cycle = 0   
        
        return ("100 OK", [], "Music 2 Ended")

@web_app.route("/")
def root(request):  # pylint: disable=unused-argument
    print("Root WSGI handler")
    converted_num = "% s" % ((potentiometer.value * 3.3) / 66536)
    
    # return ("200 OK", [], ["Root document"])
    return ("100 OK", [], [html_string])

# Here we setup our server, passing in our web_app as the application
server.set_interface(eth)
print(eth.chip)
wsgiServer = server.WSGIServer(80, application=web_app)

print("Open this IP in your browser: ", eth.pretty_ip(eth.ip_address))

# Start the server
wsgiServer.start()

while True:
    type(potentiometer.value)
    # Our main loop where we have the server poll for incoming requests
    wsgiServer.update_poll()
    # Maintain DHCP lease
    eth.maintain_dhcp_lease()
    # Could do any other background tasks here, like reading sensors
