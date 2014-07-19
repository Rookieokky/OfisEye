# Imports
import webiopi
import math 
from RPIO import PWM

# Retrieve GPIO lib
GPIO = webiopi.GPIO

# -------------------------------------------------- #
# Constants definition                               #
# -------------------------------------------------- #

# Left motor GPIOs
L1=9  # H-Bridge 1
L2=10 # H-Bridge 2
LS=11 # H-Bridge 1,2EN

# Right motor GPIOs
R1=23 # H-Bridge 3
R2=24 # H-Bridge 4
RS=25 # H-Bridge 3,4EN

servo = PWM.Servo()
SERVOY  = 8
SERVOX  = 18
global angle_y
global angle_x
angle_y = 1500
angle_x = 1500


# -------------------------------------------------- #
# Convenient PWM Function                            #
# -------------------------------------------------- #

# Set the speed of two motors
def set_speed(speed):
    GPIO.pulseRatio(LS, speed)
    GPIO.pulseRatio(RS, speed)

# -------------------------------------------------- #
# Left Motor Functions                               #
# -------------------------------------------------- #

def left_stop():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.LOW)

def left_forward():
    GPIO.output(L1, GPIO.HIGH)
    GPIO.output(L2, GPIO.LOW)

def left_backward():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.HIGH)

# -------------------------------------------------- #
# Right Motor Functions                              #
# -------------------------------------------------- #
def right_stop():
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.LOW)

def right_forward():
    GPIO.output(R1, GPIO.HIGH)
    GPIO.output(R2, GPIO.LOW)

def right_backward():
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.HIGH)

# -------------------------------------------------- #
# servo Y control                                    #
# -------------------------------------------------- #
def servo_y_aum():
	global angle_y
	angle_y += 50
	if angle_y > 2000:
		angle_y = 2000
	servo.set_servo(SERVOY, angle_y)

def servo_y_dim():
	global angle_y
	angle_y -= 50
	if angle_y < 1000:
		angle_y = 1000
	servo.set_servo(SERVOY, angle_y)


# -------------------------------------------------- #
# servo X control                                    #
# -------------------------------------------------- #
def servo_x_aum():
	global angle_x
	angle_x += 50
	if angle_x > 2000:
		angle_x = 2000
	servo.set_servo(SERVOX, angle_x)

def servo_x_dim():
	global angle_x
	angle_x -= 50
	if angle_x < 1000:
		angle_x = 1000
	servo.set_servo(SERVOX, angle_x)
	
# -------------------------------------------------- #
# Macro definition part                              #
# -------------------------------------------------- #

def go_forward():
    left_forward()
    right_forward()

def go_backward():
    left_backward()
    right_backward()

def turn_left():
    left_backward()
    right_forward()

def turn_right():
    left_forward()
    right_backward()

def stop():
    left_stop()
    right_stop()

def servo_center():
	global angle_y
	angle_y = 1500
	global angle_x
	angle_x = 1500
	servo.set_servo(SERVOY, angle_y)
	servo.set_servo(SERVOX, angle_x)
   
# -------------------------------------------------- #
# Initialization part                                #
# -------------------------------------------------- #

# Setup GPIOs
GPIO.setFunction(LS, GPIO.PWM)
GPIO.setFunction(L1, GPIO.OUT)
GPIO.setFunction(L2, GPIO.OUT)

GPIO.setFunction(RS, GPIO.PWM)
GPIO.setFunction(R1, GPIO.OUT)
GPIO.setFunction(R2, GPIO.OUT)

servo.set_servo(SERVOY, angle_y)
servo.set_servo(SERVOX, angle_x)

set_speed(1)
stop()

# -------------------------------------------------- #
# Main server part                                   #
# -------------------------------------------------- #


# Instantiate the server on the port 8000, it starts immediately in its own thread
server = webiopi.Server(port=8000, login="webiopi", password="raspberry")

# Register the macros so you can call it with Javascript and/or REST API

server.addMacro(go_forward)
server.addMacro(go_backward)
server.addMacro(turn_left)
server.addMacro(turn_right)
server.addMacro(stop)
server.addMacro(servo_y_aum)
server.addMacro(servo_y_dim)
server.addMacro(servo_x_aum)
server.addMacro(servo_x_dim)
server.addMacro(servo_center)
# -------------------------------------------------- #
# Loop execution part                                #
# -------------------------------------------------- #

# Run our loop until CTRL-C is pressed or SIGTERM received
webiopi.runLoop()

# -------------------------------------------------- #
# Termination part                                   #
# -------------------------------------------------- #

# Stop the server
server.stop()

# Reset GPIO functions
GPIO.setFunction(LS, GPIO.IN)
GPIO.setFunction(L1, GPIO.IN)
GPIO.setFunction(L2, GPIO.IN)

GPIO.setFunction(RS, GPIO.IN)
GPIO.setFunction(R1, GPIO.IN)
GPIO.setFunction(R2, GPIO.IN)

servo.stop_servo(SERVOY)
servo.stop_servo(SERVOX)

#GPIO.setFunction(SERVOX, GPIO.IN)
#GPIO.setFunction(SERVOY, GPIO.IN)
