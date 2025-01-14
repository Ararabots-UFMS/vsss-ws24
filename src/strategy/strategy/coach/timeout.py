from strategy.blackboard import Blackboard

from strategy.behaviour import LeafNode, Sequence, Selector
from strategy.behaviour import TaskStatus
from strategy.robots.timeout.attacker import AttackerAction

class CheckState(LeafNode):
    def __init__(self, name, _desired_states):
        self.name = name
        self.blackboard = Blackboard()
        self.desired_states = _desired_states

    def run(self):
        if self.blackboard.referee.command in self.desired_states:
            return TaskStatus.SUCCESS, None

        return TaskStatus.FAILURE, None

class _TimeoutAction(LeafNode):
    def __init__(self, name):
        super().__init__(name)
        self.blackboard = Blackboard()
        self.commands = {}

    def run(self):
        for robot in self.blackboard.ally_robots:
            self.commands[robot] = AttackerAction()

        return TaskStatus.SUCCESS, self.commands
    
class _Timeout(Sequence):
    def __init__(self, name):
        super().__init__(name, [])
        
        """ List with possible inputs to this state """
        commands = ["TIMEOUT_BLUE", "TIMEOUT_YELLOW"]
        check_timeout = CheckState("CheckTimeout", commands)
        
        timeout_action = _TimeoutAction("TimeoutAction")

        self.add_children([check_timeout, timeout_action])
        
    def run(self):
        """Access the second element in tuple"""
        return super().run()

if __name__ == "__main__":
    timeout = _Timeout("Timeout")
    print(timeout.run()[1])