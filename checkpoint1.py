import time
import board
import busio
import adafruit_bmp280
from dual_max14870_rpi import motors, MAX_SPEED
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

#BMP280 Setup
def bmp_initialize():
    i2c = busio.I2C(board.SCL, board.SDA)
    return adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    
log_file = open("/home/aykay/workspace_ait500/bmp_log.txt", "w")
log_file.write("Timestamp,Temperature(C),Altitude(m)\n")

# 1.7s is my current calculation for covering 30cm
def move_forward(duration=1.7, speed=100):
    motors.setSpeeds(speed, speed)
    time.sleep(duration)
    motors.forceStop()

def move_backward(duration=1.7, speed=100):
    motors.setSpeeds(-speed, -speed)
    time.sleep(duration)
    motors.forceStop()

# speed needs to be a bit higher (105) to turn at 90 deg
def turn_left(duration=0.68, speed=105):
    motors.setSpeeds(speed, -speed)
    time.sleep(duration)
    motors.forceStop()

def turn_right(duration=0.68, speed=105):
    motors.setSpeeds(-speed, speed)
    time.sleep(duration)
    motors.forceStop()

# picamera setup
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
encoder = H264Encoder(10000000)
output = FfmpegOutput('/home/aykay/workspace_ait500/checkpoint1_video.mp4')
picam2.start_recording(encoder, output)

bmp280 = bmp_initialize()

# Capture Movement and Sensor Data 
start_time = time.time()
print("Starting 2-minute run...\n")

while time.time() - start_time < 120:
    print(f"Temperature: {bmp280.temperature:.2f} °C | Altitude: {bmp280.altitude:.2f} m")
    log_file.write(f"{time.time()},{bmp280.temperature:.2f},{bmp280.altitude:.2f}\n") # log file for bmp output, just for blackboard submission 
   
    # run each movement pattern for 30cm equivalent
    move_forward()
    move_backward()
    turn_left()
    move_forward()
    turn_right()
    move_forward()
    turn_left()
    move_backward()
    turn_right()
    move_backward()

    time.sleep(1)

print("Finished 2-minute movement test.")
motors.forceStop()
picam2.stop_recording()

