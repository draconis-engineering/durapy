"""UniOps Continuous PID Controller algorithm"""

import time


class ContinuousPIDController:
    def __init__(
        self,
        setpoint: float = 0.0,
        output_limits: tuple[float | None, float | None] = (None, None),
        *,
        kp: float,
        ki: float,
        kd: float,
    ):
        """A Continuous PID controller."""
        self.kp: float = kp
        self.ki: float = ki
        self.kd: float = kd
        self.setpoint: float = setpoint
        self.min_output, self.max_output = output_limits

        self._integral: float = 0.0
        self._last_value: float | None = None
        self._last_time: float | None = None

    def reset(self) -> None:
        """Reset the integral, last error and last time."""

        self._integral = 0.0
        self._last_value = None
        self._last_time = None

    def update(
        self, *, current_value: float, current_time: float | None = None
    ) -> float:
        """Update the controller with new values and the current time."""

        now = current_time if current_time is not None else time.time()

        # First pass initialization ------------------
        if self._last_time is None or self._last_value is None:
            self._last_time = now
            self._last_value = current_value
            return 0.0  # Returns 0.0 on the first tick, but saves state for tick #2

        dt = now - self._last_time

        if dt <= 0.0:
            dt = 1e-6

        error = self.setpoint - current_value

        # Proportional term --------------------------
        p_term = self.kp * error

        # Derivative term (Prevents derivative kick by tracking process value)
        d_value = current_value - self._last_value
        d_term = -self.kd * (d_value / dt)

        # Integral term ------------------------------
        integral_step = error * dt
        self._integral += integral_step
        i_term = self.ki * self._integral

        # Total Raw Output ---------------------------
        output = p_term + i_term + d_term

        # Clamping & Anti-Windup Logic ---------------
        # Roll back the integral step to prevent windup
        if self.max_output is not None and output > self.max_output:
            self._integral -= integral_step
            output = self.max_output
        elif self.min_output is not None and output < self.min_output:
            self._integral -= integral_step
            output = self.min_output

        # State updates for next loop iteration ------
        self._last_value = current_value
        self._last_time = now

        return output
