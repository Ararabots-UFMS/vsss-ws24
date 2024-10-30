from movement.path.path_profiles import MovementProfiles, DirectionProfiles
from strategy.blackboard import Blackboard


"""This file should have a properly class to use the Movement classes, look the example below"""

class NormalMovement():
    """This class should be a strategy skill to move a robot to a especific point"""
    def __init__(self):
        super().__init__()
        self.blackboard = Blackboard()

    # theta is radians and position(x,y) is millimeter

    def moveToCenter(self):   

        """Moviment to point when the robot is not goalkeeper"""
        return {"obstacles" : self.blackboard.enemy_robots,
                "path_profile" : MovementProfiles.Normal,
                "orientation_profile": DirectionProfiles.Aim,
                "sync" : False,
                "path_kwargs" : {"goal_state" : (90,0)},
                "orientation_kwargs" : {"theta" : 0}}
    
    def centerLineGoal(self):
        
        """"Moviment to the center of our goal"""

        return {"obstacles" : [],
                "path_profile" : MovementProfiles.Normal,
                "orientation_profile": DirectionProfiles.Aim,
                "sync" : False,
                "path_kwargs" : {"goal_state" : (2160,0)},
                "orientation_kwargs" : {"theta" : 0}}
    
    def outsideCenterCircle(self):
        """"Moviment to the center of our goal"""

        return {"obstacles" : [],
                "path_profile" : MovementProfiles.Normal,
                "orientation_profile": DirectionProfiles.Aim,
                "sync" : False,
                "path_kwargs" : {"goal_state" : (600,0)},
                "orientation_kwargs" : {"theta" : 0}}
      
        
    def moveToPenaltyKicker(self):

        """Moviment to central area, acording with the Penalty requirements"""

        #TODO: create a function to direct the robot to point (+-750,0)
        # Penalty mark: at the goal to goal mark (y = 0) 3m away from the goal (x = -750 or x = +750)
        if self.blackboard.gui._is_field_side_left: # point (-750,0) turned to right
            return {"obstacles" : [],
                "path_profile" : MovementProfiles.Normal,
                "orientation_profile": DirectionProfiles.Aim,
                "sync" : False,
                "path_kwargs" : {"goal_state" : (660,0)},
                "orientation_kwargs" : {"theta" : 0}}
        else: # point(750,0), turned to left
            return {"obstacles" : [],
                "path_profile" : MovementProfiles.Normal,
                "orientation_profile": DirectionProfiles.Aim,
                "sync" : False,
                "path_kwargs" : {"goal_state" : (-660,0)},
                "orientation_kwargs" : {"theta" : 3.14}}
    
    def moveToPenaltyDefender(self):
        if self.blackboard.gui._is_field_side_left: # point (-750,0) turned to right
            return {"obstacles" : [],
                "path_profile" : MovementProfiles.Normal,
                "orientation_profile": DirectionProfiles.Aim,
                "sync" : False,
                "path_kwargs" : {"goal_state" : (-250,0)},
                "orientation_kwargs" : {"theta" : 0}}
        else: # point(750,0), turned to left
            return {"obstacles" : [],
                "path_profile" : MovementProfiles.Normal,
                "orientation_profile": DirectionProfiles.Aim,
                "sync" : False,
                "path_kwargs" : {"goal_state" : (250,0)},
                "orientation_kwargs" : {"theta" : 3.14}}
    
    def moveToFreeKick(self):
        #TODO adjust properly free-kick
        if self.blackboard.gui._is_field_side_left: # point (-750,0) turned to right
            return {"obstacles" : [],
                "path_profile" : MovementProfiles.Normal,
                "orientation_profile": DirectionProfiles.Aim,
                "sync" : False,
                "path_kwargs" : {"goal_state" : (-90,0)},
                "orientation_kwargs" : {"theta" : 0}}
        else: # point(750,0), turned to left
            return {"obstacles" : [],
                "path_profile" : MovementProfiles.Normal,
                "orientation_profile": DirectionProfiles.Aim,
                "sync" : False,
                "path_kwargs" : {"goal_state" : (-660,0)},
                "orientation_kwargs" : {"theta" : 3.14}}

            


class StraightMovement():
    """This class have types of movements using StraightProfile"""
    def __init__(self):
        super().__init__()
        self.blackboard = Blackboard()

    def run(self):

        """Moviment to point when the robot is not goalkeeper"""

        return {"obstacles" : self.blackboard.enemy_robots,
                "path_profile" : MovementProfiles.Straight,
                "orientation_profile": DirectionProfiles.Aim,
                "sync" : False,
                "orientation_kwargs" : {"theta" : 0}}
        
        
class GetInAngleStrategy():
    """This class have types of movements using StraightProfile"""
        
    pass

class BreakStrategy():
    """"This class have the BreakProfile movement"""
    def __init__(self):
        super().__init__()
        self.blackboard = Blackboard()

    def _break(self):
        return {"obstacles" : self.blackboard.enemy_robots,
                "path_profile" : MovementProfiles.Break,
                "orientation_profile": DirectionProfiles.Aim,
                "sync" : False,
                "path_kwargs" : None,
                "orientation_kwargs" : {}}
        