
import math
from strategy.behaviour import LeafNode, Selector, TaskStatus
from strategy.blackboard import Blackboard
from strategy.coach.running.Defense_play import DefensivePlay
from strategy.skill.route import BreakStrategy, GetInAngleStrategy, NormalMovement

class DefensePosition(LeafNode):
    def __init__(self, name, point):
        super().__init__(name)
        self.blackboard = Blackboard()
        self.movement = NormalMovement()
        self.point = point
        

    def run(self):
        if self.blackboard.gui.is_field_side_left:
            theta = 0
        else:
            theta = math.pi
        print(f"indo para o ponto : {self.point}")
        return TaskStatus.SUCCESS, self.movement.move_to_position_with_orientation(self.point[0], self.point[1], theta)
    

class CheckBallDistance(LeafNode):
    def __init__(self, name):
        super().__init__(name)
        self.blackboard = Blackboard()
        self.movement = BreakStrategy()
        self.ball_position_x = self.blackboard.balls[0].position_x
        self.ball_position_y = self.blackboard.balls[0].position_y
        self.position_x = self.blackboard.ally_robots[0].position_x
        self.position_y = self.blackboard.ally_robots[0].position_y
        self.radius = 142

    def run(self):

        distance = math.sqrt((self.position_x - self.ball_position_x) ** 2 + (self.position_y - self.ball_position_y) ** 2)

        if distance > self.radius:
            print(f"Estou longe da bola : {distance}")
            return TaskStatus.FAILURE, None
        else:
            print(f"Estou perto da bola {distance}")
            return TaskStatus.SUCCESS, self.movement._break()
        


class OurActionDefender(Selector):
    def __init__(self, name, points):
        super().__init__(name, [])
        self.blackboard = Blackboard()
        self.point = points
        is_near_ball = CheckBallDistance("CheckBallDistance")
        defensive_mode = DefensePosition("DefensivePosition", self.point)
        self.add_children([defensive_mode])
    
    def __call__(self):
        return super().run()[1]
        

