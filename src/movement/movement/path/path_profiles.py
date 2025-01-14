from ruckig import InputParameter, Result, Ruckig, Trajectory, ControlInterface, Synchronization
from math import sin, cos, pi
from random import uniform

from abc import ABC, abstractmethod

from typing import List, Optional, Tuple

# TODO Separate movement profiles and Aim Profile.
# TODO Change 3d trajectorys to 2d trajectorys and 1d orientation trajectory.

class PathProfile(ABC):
    ''' Profiles are the used in the Path generator, it defines how a path will be generated '''
    @abstractmethod
    def generate(self):
        pass

class OrientationProfile(ABC):
    ''' Profiles are the used in the Path generator, it defines how a path will be generated '''
    @abstractmethod
    def generate(self):
        pass

# --- Path Profiles ---

class StraightProfile(PathProfile):
    ''' Return a straight line between two states ignoring the position plane and orientation'''
    def generate(inp: InputParameter, theta: float):
        inp.control_interface = ControlInterface.Velocity

        bottleneck_vel = inp.max_velocity[0] if inp.max_velocity[0] < inp.max_velocity[1] else inp.max_velocity[1]

        inp.target_velocity = [bottleneck_vel * cos(theta), bottleneck_vel * sin(theta)]
        inp.target_acceleration = [0.0, 0.0]

        return None

class NormalProfile(PathProfile):
    ''' Return a bang-bang rest to rest trajectory from initial state to final state given acceleration constrainsts '''
    def generate(inp: InputParameter, goal_state: Tuple[float, float]):
        inp.control_interface = ControlInterface.Position
        
        inp.target_position = [goal_state[0], goal_state[1]]
       
        return None

class GetInAngleProfile(PathProfile):
    ''' Return a bang-bang trajectory from initial state to final state arriving with a velocity in a angle'''
    def generate(inp: InputParameter, goal_state: Tuple[float, float], theta: float):
        inp.control_interface = ControlInterface.Position 
        inp.target_velocity = [0, 0]

        # Using 10% of the total velocity.
        bottleneck_vel = inp.max_velocity[0] if inp.max_velocity[0] < inp.max_velocity[1] else inp.max_velocity[1]
        arriving_velocity = bottleneck_vel
        
        inp.target_position = [goal_state[0], goal_state[1]]
        inp.target_velocity = [arriving_velocity * cos(theta) , arriving_velocity * sin(theta)]
        
        return None

class BreakProfile(PathProfile):
    ''' Return a maximum breaking path, in this case, a acceleration in the oposite direction of the movement '''
    def generate(inp: InputParameter):
        # Goal state will not be used, sincronization will be turned off and each Dof will reach a stop independently.
        inp.control_interface = ControlInterface.Velocity
        inp.synchronization = Synchronization.No

        inp.target_velocity = [0.0, 0.0]
        inp.target_acceleration = [0.0, 0.0]

        return None

# --- Orientation Profiles ---

class ONormalProfile(OrientationProfile):
    ''' Return a path to the velocity direction'''
    def generate(inp: InputParameter, current_state: Tuple[List[float]]):
        pass

class OBreakProfile(OrientationProfile):
    ''' Return a maximum breaking path, in this case, a acceleration in the oposite direction of the movement '''
    def generate(inp: InputParameter):
        # Goal state will not be used, sincronization will be turned off and each Dof will reach a stop independently.
        inp.control_interface = ControlInterface.Velocity
        inp.synchronization = Synchronization.No

        inp.target_velocity = [0.0]
        inp.target_acceleration = [0.0]

        return None

class AimProfile(OrientationProfile):
    ''' Return a rotation movement profile to angle while being stationary'''
    def generate(inp: InputParameter, theta: float):
        inp.control_interface = ControlInterface.Position
        
        inp.target_position = [theta]
        inp.target_velocity = [0]

        return None

class SpinProfile(OrientationProfile):
    ''' Return a spin movement profile while being stationary'''
    def generate(inp: InputParameter, clockwise: bool):
        inp.control_interface = ControlInterface.Velocity
        inp.synchronization = Synchronization.No

        direction = 1 if clockwise else -1

        inp.target_velocity = [inp.max_velocity[0] * direction]
        inp.target_acceleration = [0.0]

        return None

# --- Bypass Profiles ---

class BypassProfile(PathProfile):
    ''' Should not be used in strategy, in case of collision, it's a alternative deviation path '''
    def generate(inp: InputParameter, min_duration: float):
        inp.control_interface = ControlInterface.Velocity

        random_angle = uniform(0, 3.14)

        inp.target_velocity = [inp.max_velocity[0] * cos(random_angle), inp.max_velocity[1] * sin(random_angle)]
        inp.target_acceleration = [0, 0]
        inp.minimum_duration = min_duration

        return None

# --------------------------------------
class MovementProfiles():
    Straight   = StraightProfile
    Normal     = NormalProfile
    GetInAngle = GetInAngleProfile
    Break      = BreakProfile
    Bypass     = BypassProfile

class DirectionProfiles():
    Normal = ONormalProfile
    Break = OBreakProfile
    Aim  = AimProfile
    Spin = SpinProfile