"""UniOps Continuous PID Controller algorithm"""

import time


class ContinuousPIDController:
    def __init__(self, kp, ki, kd, setpoint=0.0, output_limits=(None, None)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.min_output, self.max_output = output_limits
        self._integral = 0.0
        self._last_error = None
        self._last_time = None

    def reset(self):
        self._integral = 0.0
        self._last_error = None
        self._last_time = None

    def update(self, current_value, current_time=None):
        now = current_time if current_time is not None else time.time()
        if self._last_time is None:
            self._last_time = now
            self._last_error = self.setpoint - current_value
            return 0.0

        dt = now - self._last_time
        if dt <= 0.0:
            dt = 1e-6

        error = self.setpoint - current_value
        p_term = self.kp * error
        self._integral += error * dt
        i_term = self.ki * self._integral
        derivative = (error - self._last_error) / dt
        d_term = self.kd * derivative
        output = p_term + i_term + d_term

        if self.max_output is not None and output > self.max_output:
            if self.ki != 0:
                self._integral -= error * dt
            output = self.max_output
        elif self.min_output is not None and output < self.min_output:
            if self.ki != 0:
                self._integral -= error * dt
            output = self.min_output

        self._last_error = error
        self._last_time = now
        return output
