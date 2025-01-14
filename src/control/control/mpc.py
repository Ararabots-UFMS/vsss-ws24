from do_mpc.controller import MPC
from control.model import get_model
from time import time
from math import copysign, pi
from ruckig import Trajectory


class Controller:
    def __init__(
        self, max_velocity, max_angular_vel, n_horizon=2, t_step=0.1, n_robust=0
    ):
        self.n_horizon = n_horizon
        self.t_step = t_step
        self.n_robust = n_robust

        self.path_trajectory = Trajectory(2)
        self.orientation_trajectory = Trajectory(1)

        self.mpc = get_mpc(
            max_velocity,
            max_angular_vel,
            n_horizon=n_horizon,
            t_step=t_step,
            n_robust=n_robust,
            store_full_solution=False,
        )
        self.tvp_template = self.mpc.get_tvp_template()
        self.mpc.set_tvp_fun(self.tvp_func)
        self.mpc.setup()

    def __call__(self, state):
        # if copysign(1, state[2]) != copysign(1, self.orientation_trajectory.at_time(self.orientation_trajectory.duration)[0][0]):
        #     state[2] += 2*pi * copysign(1, self.orientation_trajectory.at_time(self.orientation_trajectory.duration)[0][0])
        
        self.set_initial_guess(state)
        return self.mpc.make_step(state)

    def set_initial_guess(self, state):
        self.mpc.x0 = state
        self.mpc.set_initial_guess()

    def set_trajectory(self, path, orientation) -> None:
        self.path_trajectory = path
        self.orientation_trajectory = orientation

    def reset_history(self):
        self.mpc.reset_history()

    def tvp_func(self, t_now):
        for k in range(self.n_horizon):
            positions, _, _ = self.path_trajectory.at_time(t_now + k * self.t_step)
            orientation, _, _ = self.orientation_trajectory.at_time(
                t_now + k * self.t_step
            )

            self.tvp_template["_tvp", k, "ref_x"] = positions[0]
            self.tvp_template["_tvp", k, "ref_y"] = positions[1]
            self.tvp_template["_tvp", k, "ref_orientation"] = orientation
        return self.tvp_template


def get_mpc(
    max_velocity, max_angular_vel, n_horizon, t_step, n_robust, store_full_solution
):
    model = get_model()
    mpc = MPC(model)

    mpc.set_param(
        n_horizon=n_horizon, t_step=t_step, n_robust=n_robust, store_full_solution=False
    )

    mpc.settings.supress_ipopt_output()

    lterm = (
        (model.x["x"] - model.tvp["ref_x"]) ** 2
        + (model.x["y"] - model.tvp["ref_y"]) ** 2
        + (model.x["orientation"] - model.tvp["ref_orientation"]) ** 2
    )
    mterm = lterm
    mpc.set_objective(lterm=lterm, mterm=mterm)
    mpc.set_rterm(vx=1, vy=1, angular_velocity=1e-2)

    mpc.bounds["lower", "_u", "vx"] = -max_velocity
    mpc.bounds["lower", "_u", "vy"] = -max_velocity
    mpc.bounds["lower", "_u", "angular_velocity"] = -max_angular_vel

    mpc.bounds["upper", "_u", "vx"] = max_velocity
    mpc.bounds["upper", "_u", "vy"] = max_velocity
    mpc.bounds["upper", "_u", "angular_velocity"] = max_angular_vel

    return mpc
