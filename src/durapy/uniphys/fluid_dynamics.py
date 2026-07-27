"""UniPhys Fluid Dynamics Source"""

def reynolds_number(velocity: float, characteristic_length: float, kinematic_viscosity: float) -> float:
    """
    Calculate the Reynolds number for a given flow.

    Parameters
    ----------
    velocity: The velocity of the fluid (m/s).
    characteristic_length: The characteristic length of the flow (m).
    kinematic_viscosity: The kinematic viscosity of the fluid (m^2/s).

    Returns
    -------
    float: The Reynolds number.
    """
    return (velocity * characteristic_length) / kinematic_viscosity
