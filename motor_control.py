from gpiozero import LED, Device
from gpiozero.pins.mock import MockFactory
from time import sleep

# Set the pin factory to the mock factory (for simulation on non-Raspberry Pi environments)
Device.pin_factory = MockFactory()

# Simulated GPIO pin mapping for thrusters using MockFactory
stern_port_thruster = LED(3)      # Stern Port Thruster on GPIO 3
stern_starboard_thruster = LED(5) # Stern Starboard Thruster on GPIO 5
bow_port_thruster = LED(6)        # Bow Port Thruster on GPIO 6
bow_starboard_thruster = LED(9)   # Bow Starboard Thruster on GPIO 9
heave_thruster = LED(11)          # Heave Thruster on GPIO 11

# Function to initialize thrusters (simulate ESC initialization)
def initialize_thrusters():
    print("Initializing all thrusters with minimum pulse...")
    stern_port_thruster.off()
    stern_starboard_thruster.off()
    bow_port_thruster.off()
    bow_starboard_thruster.off()
    heave_thruster.off()
    sleep(2)
    print("Thrusters initialized.")

# Thruster control functions
def start_heave():
    print("Starting heave thruster...")
    heave_thruster.on()
    sleep(2)
    print("Heave thruster active.")

def start_stern_thrusters():
    print("Activating stern thrusters...")
    stern_port_thruster.on()
    stern_starboard_thruster.on()
    sleep(2)
    print("Stern thrusters active.")

def start_bow_thrusters():
    print("Activating bow thrusters...")
    bow_port_thruster.on()
    bow_starboard_thruster.on()
    sleep(2)
    print("Bow thrusters active.")

def stop_bow_thrusters():
    print("Stopping bow thrusters...")
    bow_port_thruster.off()
    bow_starboard_thruster.off()
    sleep(2)
    print("Bow thrusters stopped.")

def slow_down_heave_thruster():
    print("Slowing down heave thruster...")
    heave_thruster.off()
    sleep(2)
    print("Heave thruster slowed down.")

def slow_down_stern_thrusters():
    print("Slowing down stern thrusters...")
    stern_port_thruster.off()
    stern_starboard_thruster.off()
    sleep(5)
    print("Stern thrusters slowed down.")
