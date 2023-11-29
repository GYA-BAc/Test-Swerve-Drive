from networktables import NetworkTable
from components.swerve_module import SwerveModule

from tools.utils import *

class SwerveDrive:
    """NOTE: ensure wheels are aligned forward when first turned on"""

    sd: NetworkTable

    frontLeftModule: SwerveModule
    frontRightModule: SwerveModule
    rearLeftModule: SwerveModule
    rearRightModule: SwerveModule

    def setup(self):
        self.velocity_vector = [
            0, # fwd (positive) / bwd
            0  # right(positive) / left
        ]

        self.rotation_speed = 0 # clockwise (positive) / ccw

    def flush(self):
        """reset all modules to make them face forward"""
        self.frontLeftModule.flush()
        self.frontRightModule.flush()
        self.rearLeftModule.flush()
        self.rearRightModule.flush()

    def set_velocity_vector(self, new: list[float, float]):
        self.velocity_vector = new

    # def set_rotation_speed(self, new: float):
    #     self.rotation_speed = limit(new)

    def physics_process(self):
        """NOTE: currently cannot do rotations (only does strafe)"""
        
        # break down velocity vector into speed and angle
        angle = vector_to_degrees(self.velocity_vector)
        speed = get_vector_length(self.velocity_vector)

        self.frontLeftModule.set_direction(angle)
        self.frontRightModule.set_direction(angle)
        self.rearLeftModule.set_direction(angle)
        self.rearRightModule.set_direction(angle)

        self.frontLeftModule.set_speed(speed)
        self.frontRightModule.set_speed(speed)
        self.rearLeftModule.set_speed(speed)
        self.rearRightModule.set_speed(speed)

    def execute(self):
        
        self.sd.putValue("Velocity Vector", f"{self.velocity_vector[0]} {self.velocity_vector[1]}")

        self.physics_process()

        # manually call module's execute method
        self.frontLeftModule.execute()
        self.frontRightModule.execute()
        self.rearLeftModule.execute()
        self.rearRightModule.execute()