from strategy.blackboard import Blackboard
from strategy.skill.route import BreakStrategy

"""Contains all HaltActions the robot must do (in order or not) during the match"""

class GoalKeeperAction():
    def __init__(self):
        self.name = "HatlAction"
        self.blackboard = Blackboard()
        #self.movement = MoveToPoint(self.name)

    def __call__(self):
        self.movemet = BreakStrategy() 
        return self.movemet._break() # TODO remove this method
        #return self.movement.moveToPenalty()

    def run(self):
        self.movemet = BreakStrategy() 
        return self.movemet._break() # TODO remove this method
        