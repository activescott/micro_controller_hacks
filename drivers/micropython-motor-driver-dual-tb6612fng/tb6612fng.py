import machine

SPEED_MAX = 2**16 - 1
SPEED_MIN = 0

class Motor:
  """
  Provides methods to control a single motor in the TB6612FNG dual motor driver.
  """
  def __init__(self, in1_pin, in2_pin, pwm_pin):
    """
    Initializes a motor.

    - `pinIn1`: Pin ID identifying the pin for one of the two inputs that determines the direction of the motor. This will be AI1 or AI2 for motor A and BI1 or BI2 for motor B.
    - `pinIn2`: Pin ID identifying the pin for one of the two inputs that determines the direction of the motor. This will be AI1 or AI2 for motor A and BI1 or BI2 for motor B.
    - `pinPWM`: PWM input that controls the speed.
    """
    self.pinIn1 = machine.Pin(in1_pin, machine.Pin.OUT, machine.Pin.PULL_DOWN)
    self.pinIn2 = machine.Pin(in2_pin, machine.Pin.OUT, machine.Pin.PULL_DOWN)
    self.pinPWM = machine.PWM(machine.Pin(pwm_pin))
    # Datasheet says max is 100 kHz
    KHZ = 1000
    self.pinPWM.freq(100 * KHZ)

  # How the pins control a a motor from Toshiba's PDF datsheet
  # In1 In2	PWM Out1	Out2	Mode
  # H   H   H/L L     L     Short brake
  # L   H   H   L     H     CCW
  # L   H   L   L     L     Short brake
  # H   L   H   H     L     CW
  # H   L   L   L     L     Short brake
  # L   L   H   OFF   OFF   Stop

  def stop(self):
    """Stops the motor."""
    self.pinIn1.low()
    self.pinIn2.low()
  
  def clockwise(self, speed):
    """
    Turns the motor clockwise at the specified speed.
    Speed must be in the range 0 to 65535 inclusive.
    """
    self.pinIn1.high()
    self.pinIn2.low()
    self.pinPWM.duty_u16(speed)

  def counter_clockwise(self, speed):
    """
    Turns the motor counter clockwise at the specified speed.
    Speed must be in the range 0 to 65535 inclusive.
    """
    self.pinIn1.low()
    self.pinIn2.high()
    self.pinPWM.duty_u16(speed)


class Motors:
  """
  Provides methods to control the dual TB6612FNG motor controller.
  """
  def __init__(self, left_motor, right_motor, stby_pin):
    """
    Initializes a new motor controller

    - `left_motor`: A an initialized `Motor` object representing one of the two motors on the board.
    - `right_motor`: A an initialized `Motor` object representing one of the two motors on the board.
    - `stby_pin`: The pin ID for the STBY pin.
    """
    self.left = left_motor
    self.right = right_motor
    
    self.stby = machine.Pin(stby_pin, machine.Pin.OUT)
    # LOW = standby
    self.stby.high()
  
  def standby(self):
    self.stby.low()
  
  def disable(self):
    self.standby()
  
  def enable(self):
    self.stby.high()
  
  def forward(self, speed=SPEED_MAX):
    self.left.counter_clockwise(speed)
    self.right.clockwise(speed)
  
  def reverse(self, speed=SPEED_MAX):
    self.left.clockwise(speed)
    self.right.counter_clockwise(speed)

  def spin_left(self, speed=SPEED_MAX):
    self.left.stop()
    self.right.clockwise(speed)

  def spin_right(self, speed=SPEED_MAX):
    self.right.stop()
    self.left.counter_clockwise(speed)
  
  def stop(self):
    self.left.stop()
    self.right.stop()
