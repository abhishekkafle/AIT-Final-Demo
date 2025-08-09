import time
import board
import busio
import adafruit_bmp280
from dual_max14870_rpi import motors, MAX_SPEED
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

def bmp_initialize():
    i2c = busio.I2C(board.SCL, board.SDA)
    return adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# movements functions 

# def move_forward(duration=10, speed=100):
#     motors.setSpeeds(speed, speed)
#     time.sleep(duration)
#     motors.forceStop()

# def move_backward(duration=10, speed=100):
#     motors.setSpeeds(-speed, -speed)
#     time.sleep(duration)
#     motors.forceStop()

def turn_left(duration=0.68, speed=105):
    motors.setSpeeds(speed, -speed)
    time.sleep(duration)
    motors.forceStop()

def turn_right(duration=0.68, speed=105):
    motors.setSpeeds(-speed, speed)
    time.sleep(duration)
    motors.forceStop()

def stop(duration=1):
    motors.forceStop()
    time.sleep(duration)

# cam and format setup
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
encoder = H264Encoder(10000000)
output = FfmpegOutput('/home/aykay/workspace_ait500/checkpoint2_video.mp4')
picam2.start_recording(encoder, output)

bmp280 = bmp_initialize()

log_file = open("/home/aykay/workspace_ait500/bmp_checkpoint2_log.txt", "w")
log_file.write("Temp(C), Action\n")

start_time = time.time()
print("Checkpoint 2: Maze Navigation with Temperature Sensor\n")

while time.time() - start_time < 20:
    temp = bmp280.temperature
    altitude = bmp280.altitude
    timestamp = time.time()
    STOP_TEMP = 25
    LEFT_TEMP = 27
    RIGHT_TEMP = 28

    if LEFT_TEMP < temp < RIGHT_TEMP:
        action = "Move Forward"
        #move_forward()
        motors.setSpeeds(100, 100)
    elif temp < STOP_TEMP:
        action = "Stop"
        motors.forceStop()
    elif temp < LEFT_TEMP:
        action = "Turn Left"
        turn_left()
        motors.setSpeeds(100, 100)  # resume forward
    elif temp > RIGHT_TEMP: 
        action = "Turn Right"
        turn_right()
        motors.setSpeeds(100, 100)  # resume forward

    print(f"Temp: {temp:.2f}°C | Action: {action}")
    log_file.write(f"{temp:.2f}, {action}\n")

    time.sleep(1)

log_file.close()
motors.forceStop()
picam2.stop_recording()
print("Completed")
