# python3
 
import smbus2 as smbus
import math
import time
from datetime import datetime
 
# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
# Read data from register addr and convert
def read_byte(adr):
    return bus.read_byte_data(address, adr)
 
def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val
 
# Two's complements conversion
def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
# Calculations of rotation value
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)
 
# Create csv file with column names
 
file_name = datetime.now().strftime('%Y-%m-%d %H:%M')+".csv"
f = open(file_name, "w", encoding='utf-8')
f.write("time,data_no.,gyro_x,gyro_y,gyro_z,g_x_scaled,g_y_scaled,g_z_scaled,accel_x,accel_y,accel_z,a_x_scaled,a_y_scaled,a_z_scaled,rotation_x,rotation_y\n")
f.close()
 
#Variables declare
num = 0
st = ""
 
while True:
    try:
        bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
        address = 0x68       # This is the address value read via the i2cdetect command
        # Now wake the 6050 up as it starts in sleep mode
        bus.write_byte_data(address, power_mgmt_1, 0)
        num = num + 1
        print("No." + str(num))
        print("-----------")
        print("gyro data")
        print("---------")
        gyro_xout = read_word_2c(0x43)
        gyro_yout = read_word_2c(0x45)
        gyro_zout = read_word_2c(0x47)
        print("gyro_xout: ", gyro_xout, " scaled: ", round((gyro_xout / 131.0), 4))
        print("gyro_yout: ", gyro_yout, " scaled: ", round((gyro_yout / 131.0), 4))
        print("gyro_zout: ", gyro_zout, " scaled: ", round((gyro_zout / 131.0), 4))
        print("accelerometer data")
        print("------------------")
        accel_xout = read_word_2c(0x3b)
        accel_yout = read_word_2c(0x3d)
        accel_zout = read_word_2c(0x3f)
        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0
        s1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-4]
        print("now_time: ", s1)
        print("accel_xout: ", accel_xout, " scaled: ", round(accel_xout_scaled, 4))
        print("accel_yout: ", accel_yout, " scaled: ", round(accel_yout_scaled, 4))
        print("accel_zout: ", accel_zout, " scaled: ", round(accel_zout_scaled, 4))
        print("x rotation: " , round(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled), 4))
        print("y rotation: " , round(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled), 4))
        print("------------")
        print(accel_xout_scaled + accel_yout_scaled + accel_zout_scaled)
        s2 = str(gyro_xout)
        s3 = str(gyro_yout)
        s4 = str(gyro_zout)
        s5 = str(round((gyro_xout / 131.0),4))
        s6 = str(round((gyro_yout / 131.0),4))
        s7 = str(round((gyro_zout / 131.0),4))
        s8 = str(accel_xout)
        s9 = str(accel_yout)
        s10 = str(accel_zout)
        s11 = str(round((accel_xout / 16384.0),4))
        s12 = str(round((accel_yout / 16384.0),4))
        s13 = str(round((accel_zout / 16384.0),4))
        s14 = str(round(get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled), 4))
        s15 = str(round(get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled), 4))
        # Each data is a string separated by comma
        total = s1 + "," + str(num)+","+s2+","+s3+","+s4+","+s5+","+s6+","+s7+","+s8+","+s9+","+s10+","+s11+","+s12+","+s13+","+s14+","+s15+"\n"
        st = st + total
        # Write to file evey 10s
        if num % 1200 == 0:
            f = open(file_name, "a", encoding='utf-8')
            f.write(st)
            f.close()
            st = ""
        bus.close()
        time.sleep(0.1)
    except Exception:
        continue
