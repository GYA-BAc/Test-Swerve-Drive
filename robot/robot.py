import wpilib
import wpilib.drive
import ctre
from magicbot import MagicRobot
from networktables import NetworkTables, NetworkTable


from components.swerve_module import SwerveModule
from components.swerve_drive import SwerveDrive


# Download and install stuff on the RoboRIO after imaging
'''
py -3 -m robotpy_installer download-python
py -3 -m robotpy_installer install-python
py -3 -m robotpy_installer download robotpy
py -3 -m robotpy_installer install robotpy
py -3 -m robotpy_installer download robotpy[ctre]
py -3 -m robotpy_installer install robotpy[ctre]
py -3 -m robotpy_installer download robotpy[rev]
py -3 -m robotpy_installer install robotpy[rev]
py -3 -m robotpy_installer download pynetworktables
py -3 -m robotpy_installer install pynetworktables
py -3 -m pip install -U robotpy[ctre]
py -3 -m pip install robotpy[ctre]
'''

# Push code to RoboRIO (only after imaging)
'''
python robot/robot.py deploy --skip-tests
py robot/robot.py deploy --skip-tests --no-version-check
'''




class SpartaBot(MagicRobot):

    drivetrain: SwerveDrive

    def createObjects(self):
        '''Create motors and stuff here'''

        NetworkTables.initialize(server='roborio-5045-frc.local')
        self.sd: NetworkTable = NetworkTables.getTable('SmartDashboard')

        self.drive_controller: wpilib.XboxController = wpilib.XboxController(0)

        # drivetrain motors
        self.frontLeftModule_driveMotor: ctre.WPI_TalonSRX = ctre.WPI_TalonSRX(1)
        self.frontRightModule_driveMotor: ctre.WPI_TalonSRX = ctre.WPI_TalonSRX(3)
        self.rearLeftModule_driveMotor: ctre.WPI_TalonSRX = ctre.WPI_TalonSRX(7)
        self.rearRightModule_driveMotor: ctre.WPI_TalonSRX = ctre.WPI_TalonSRX(6)

        self.frontLeftModule_rotateMotor: ctre.WPI_TalonSRX = ctre.WPI_TalonSRX(2)
        self.frontRightModule_rotateMotor: ctre.WPI_TalonSRX = ctre.WPI_TalonSRX(4)
        self.rearLeftModule_rotateMotor: ctre.WPI_TalonSRX = ctre.WPI_TalonSRX(8)
        self.rearRightModule_rotateMotor: ctre.WPI_TalonSRX = ctre.WPI_TalonSRX(5)

        # encoders
        self.frontLeftModule_encoder = self.frontLeftModule_rotateMotor
        self.frontRightModule_encoder = self.frontRightModule_rotateMotor
        self.rearLeftModule_encoder = self.rearLeftModule_driveMotor
        self.rearRightModule_encoder = self.rearRightModule_driveMotor

        # swerve modules defined here --
        # since magicrobot only allows 1 layer of variable injection 
        #   (ie, drivetrain cannot be injected with swerve_module if swerve_module needs motors to be injected first)
        self.frontLeftModule: SwerveModule = SwerveModule(self.frontLeftModule_driveMotor, self.frontLeftModule_rotateMotor, self.frontLeftModule_encoder)
        self.frontRightModule: SwerveModule = SwerveModule(self.frontRightModule_driveMotor, self.frontRightModule_rotateMotor, self.frontRightModule_encoder)
        self.rearLeftModule: SwerveModule = SwerveModule(self.rearLeftModule_driveMotor, self.rearLeftModule_rotateMotor, self.rearLeftModule_encoder)
        self.rearRightModule: SwerveModule = SwerveModule(self.rearRightModule_driveMotor, self.rearRightModule_rotateMotor, self.rearRightModule_encoder)



    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        self.sd.putValue("Mode", "Disabled")

    def teleopInit(self):
        self.drivetrain.flush()

        self.sd.putValue("Mode", "Teleop")

        print(f"{self.frontLeftModule.encoder_zero=} {self.frontRightModule.encoder_zero=} {self.rearLeftModule.encoder_zero=} {self.rearRightModule.encoder_zero=}")

    def teleopPeriodic(self):
        '''NOTE: all components' execute() methods will be called automatically'''

        #NOTE: currently no rotation capabilities

        self.drivetrain.set_velocity_vector([
            self.drive_controller.getLeftX(),
            self.drive_controller.getLeftY(),
        ])


        # log swerve module values
        self.sd.putValue("FL encoder", self.frontLeftModule.encoder.getSelectedSensorPosition())
        self.sd.putValue("FR encoder", self.frontRightModule.encoder.getSelectedSensorPosition())
        self.sd.putValue("RL encoder", self.rearLeftModule.encoder.getSelectedSensorPosition())
        self.sd.putValue("RR encoder", self.rearRightModule.encoder.getSelectedSensorPosition())

        self.sd.putValue("FL speed", self.frontLeftModule.requested_speed)
        self.sd.putValue("FR speed", self.frontRightModule.requested_speed)
        self.sd.putValue("RL speed", self.rearLeftModule.requested_speed)
        self.sd.putValue("RR speed", self.rearRightModule.requested_speed)


if __name__ == '__main__':
    wpilib.run(SpartaBot)
