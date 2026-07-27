"""UniCon Continuous PID Controller algorithm"""

import time


class ContinuousPIDController:
    """A Continuous PID Controller algorithm"""

    def __init__(
        self, kp: float = 0, ki: float = 0, kd: float = 0, setpoint: int = 0
    ) -> None:
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint

        self.integral = 0
        self.prev_error = 0
        self.prev_time = time.time()

    def update(self, measured_value: float) -> float:
        now = time.time()
        dt = now - self.prev_time

        error = self.setpoint - measured_value

        p = self.kp * error

        self.integral += error * dt
        i = self.ki * self.integral

        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        d = self.kd * derivative

        self.prev_error = error
        self.prev_time = now

        return p + i + d
