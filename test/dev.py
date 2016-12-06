import kociemba
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor

class StepperMotor:

    # Motor hat
    mh = None

    # Current motor
    motor = None

    def __init__(self, addr, step, port, speed):

        # Read I2C address
        self.mh = Adafruit_MotorHAT(addr=addr)

        # Get stepperMotor
        self.motor = self.mh.getStepper(port, step)

        # Set speed
        self.motor.setSpeed(speed)

    # Disable motor at exit
    def TurnOff(self):

        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(5).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(6).run(Adafruit_MotorHAT.RELEASE)

    # Turn stepperMotor
    def Turn(self, number_of_step, clockwise, type):

        # Set direction with bool
        c = Adafruit_MotorHAT.FORWARD if clockwise else Adafruit_MotorHAT.BACKWARD
        t = Adafruit_MotorHAT.SINGLE if type else Adafruit_MotorHAT.DOUBLE

        self.motor.step(number_of_step, c, t)


if __name__ == "__main__":

    STEP = 200
    NBR_STEP = 200
    NBR_STEPx2 = NBR_STEP * 2
    PORT_1_2 = 1
    PORT_3_4 = 2
    SPEED = 30

    up_motor = StepperMotor('0x60', STEP, PORT_1_2, SPEED)
    down_motor = StepperMotor('0x60', STEP, PORT_3_4, SPEED)

    right_motor = StepperMotor('0x61', STEP, PORT_1_2, SPEED)
    left_motor = StepperMotor('0x61', STEP, PORT_3_4, SPEED)

    front_motor = StepperMotor('0x62', STEP, PORT_1_2, SPEED)
    back_motor = StepperMotor('0x62', STEP, PORT_3_4, SPEED)



    instruction_table = {

        "U": up_motor.Turn(NBR_STEP, True, True),
        "R": right_motor.Turn(NBR_STEP, True, True),
        "F": front_motor.Turn(NBR_STEP, True, True),
        "D": down_motor.Turn(NBR_STEP, True, True),
        "L": left_motor.Turn(NBR_STEP, True, True),
        "B": back_motor.Turn(NBR_STEP, True, True),
        "U'": up_motor.Turn(NBR_STEP, False, True),
        "R'": right_motor.Turn(NBR_STEP, False, True),
        "F'": front_motor.Turn(NBR_STEP, False, True),
        "D'": down_motor.Turn(NBR_STEP, False, True),
        "L'": left_motor.Turn(NBR_STEP, False, True),
        "B'": back_motor.Turn(NBR_STEP, False, True),
        "U2": up_motor.Turn(NBR_STEPx2, True, True),
        "R2": right_motor.Turn(NBR_STEPx2, True, True),
        "F2": front_motor.Turn(NBR_STEPx2, True, True),
        "D2": down_motor.Turn(NBR_STEPx2, True, True),
        "L2": left_motor.Turn(NBR_STEPx2, True, True),
        "B2": back_motor.Turn(NBR_STEPx2, True, True)

    }

    list_movement = kociemba.solve('FLBUULFFLFDURRDBUBUUDDFFBRDDBLRDRFLLRLRULFUDRRBDBBBUFL').split()

    for row in list_movement:
        exec(instruction_table.get(row))


