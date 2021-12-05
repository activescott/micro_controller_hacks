from hmc5883l import Compass

I2C_SDA_PIN = 0
I2C_SCL_PIN = 1


comp = Compass(I2C_SDA_PIN, I2C_SCL_PIN)

devices = comp.scan()
print("Devices: {}".format(devices))

#status = comp.status()
#print("status:" + str(status))

#detected = comp.is_device_detected()
#print("detected:" + str(detected))

comp.reset()
