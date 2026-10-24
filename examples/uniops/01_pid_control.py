"""DuraPy Examples - UniOps (robotics/controls)"""

from durapy.uniops import (
    ContinuousPIDController,
    forward_kinematics,
    inverse_kinematics,
)

# PID controller
pid = ContinuousPIDController(kp=1.0, ki=0.1, kd=0.01, setpoint=100)
print("PID controller initialized, setpoint=100")
# Simulate a step
for t in [0.1, 0.2, 0.3, 0.4, 0.5]:
    out = pid.update(measured_value=50 + t * 80, dt=0.1)
    print(f"t={t:.1f}: measurement={50 + t * 80:.1f}, output={out:.3f}")

print(
    "\nUniOps modules loaded:",
    dir(forward_kinematics)[:5],
    "...",
    dir(inverse_kinematics)[:5],
)
