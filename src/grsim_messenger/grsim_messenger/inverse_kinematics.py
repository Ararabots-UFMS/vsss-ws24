import numpy as np
from math import pi, sin, cos


def apply_inverse_kinematics(vx, vy, theta):
    velocity = np.matrix([vx, vy, theta]).T

    wheel_radius = 0.027
    robot_radius = 0.09

    wheel_angles = [pi * 5 / 6, pi * 5 / 4, pi * 7 / 4, pi / 6]

    jacobian = np.matrix(
        [
            [
                cos(wheel_angles[0]),
                sin(wheel_angles[0]),
                robot_radius,
            ],
            [
                cos(wheel_angles[1]),
                sin(wheel_angles[1]),
                robot_radius,
            ],
            [
                cos(wheel_angles[2]),
                sin(wheel_angles[2]),
                robot_radius,
            ],
            [
                cos(wheel_angles[3]),
                sin(wheel_angles[3]),
                robot_radius,
            ],
        ]
    )

    wheels_v = ((1 / wheel_radius) * (jacobian * velocity)).T.tolist()

    return wheels_v[0]


if __name__ == "__main__":
    print(apply_inverse_kinematics(3.0, 3.0, 0.0))
