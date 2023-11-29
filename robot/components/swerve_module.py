import ctre
from wpimath.controller import PIDController

from tools.utils import limit

DIRECTION_ENCODER_SIZE = 4096

ROTATION_ACCEPTABLE_ERROR = 10 #~1 degree


class SwerveModule:
    """NOTE: NOT a magic component, variable injection will not work here; manually instantiate"""

    def __init__(self, drive_controller: ctre.WPI_TalonSRX, rotate_controller: ctre.WPI_TalonSRX, encoder_controller: ctre.WPI_TalonSRX):

        self.drive_motor: ctre.WPI_TalonSRX = drive_controller
        self.rotate_motor: ctre.WPI_TalonSRX = rotate_controller
        self.encoder: ctre.WPI_TalonSRX = encoder_controller

        #self.direction_PID = PIDController(0.00001, 0.0001, 0.0001)

        # NOTE: assumes that when bot is started, all wheels are facing forward
        # TODO: hardcode encoder zero values
        self.encoder_zero = self.encoder.getSelectedSensorPosition()

        self.requested_ticks = self.encoder_zero
        self.requested_speed = 0

        # between 1 and -1, used when setting new direction where new is more than 90* from old
        #   in that case, simply invert forward direction, resulting in always less than 90* rotation
        self.speed_inverted = 1 

    @staticmethod
    def ticks_to_degrees(ticks):
        deg = (ticks % DIRECTION_ENCODER_SIZE)/DIRECTION_ENCODER_SIZE
        deg *= 360
        return deg

    @staticmethod
    def degree_to_ticks(degree):
        return round((degree / 360) * DIRECTION_ENCODER_SIZE)
    
    def flush(self):
        '''Function will be called to reset motors to starting position'''
        self.requested_ticks = self.encoder_zero
        self.requested_speed = 0
        # self.pid_controller.reset()


    def set_direction(self, new_angle):
        """::new_angle (in encoder ticks)\n
        Will calculate shortest path to new direction
        """
        angle_distance = (new_angle%360) - self.ticks_to_degrees(self.requested_ticks)

        if (abs(angle_distance) > 90):
            # invert speed
            self.speed_inverted *= -1
            # account for speed inversion
            angle_distance = (angle_distance+180)%360
        
        # convert angle to ticks
        tick_distance = self.degree_to_ticks(angle_distance)

        # set new direction
        if (tick_distance != 0):
            self.requested_ticks = self.encoder_zero + tick_distance

    def set_speed(self, new_speed):
        self.requested_speed = new_speed

    def execute(self):
        """NOTE: this method will need to be manually called (as this components is not a magic component)"""

        #error = self.direction_PID.calculate(self.encoder.getSelectedSensorPosition(), self.requested_ticks)
        error = self.requested_ticks - self.encoder.getSelectedSensorPosition()

        if (abs(error) <= ROTATION_ACCEPTABLE_ERROR):
            # if "close enough" to desired direction
            self.rotate_motor.set(0)

        else:
            # use rational function to convert ticks to motor output
            rotation_speed = limit(error/DIRECTION_ENCODER_SIZE)
            # to make more gradual, use a multiple of DIRECTION_ENCODER_SIZE for the denominator

            self.rotate_motor.set(rotation_speed)

        self.drive_motor.set(self.requested_speed)

