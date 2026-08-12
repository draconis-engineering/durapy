"""`UniPhys` electromagnetics source"""

from ..shared.color_system import color_text
from ..shared.constants import INF, PLANCK, C
from ..shared.numval_types import Quantity
from ..shared.units import ELECTRONVOLT, JOULE, METER

# Ultraviolet Spectrum Wavelengths
UV_SPEC_WAVLEN: dict[tuple[float, float], str] = {
    (10, 13.5): f"{color_text('EUV', 'Violet')}",
    (13.5, 100): f"{color_text('DUV', 'Violet')}",
    (100, 280): f"{color_text('UVC', 'Violet')}",
    (280, 315): f"{color_text('UVB', 'Violet')}",
    (315, 390): f"{color_text('UVA', 'Violet')}",
}

# Visible Spectrum Wavelengths
VSBL_SPEC_WAVLEN: dict[tuple[float, float], str] = {
    (390, 450): f"{color_text('Violet', 'violet')}",
    (450, 495): f"{color_text('Blue', 'blue')}",
    (495, 570): f"{color_text('Green', 'green')}",
    (570, 590): f"{color_text('Yellow', 'yellow')}",
    (590, 620): f"{color_text('Orange', 'orange')}",
    (620, 750): f"{color_text('Red', 'red')}",
}

# Electromagnetic Spectrum Wavelengths
EM_SPEC_WAVLEN = {
    (0, 0.01): "Gamma-ray",
    (0.01, 10): "X-Ray",
    (10, 400): UV_SPEC_WAVLEN,
    (400, 700): VSBL_SPEC_WAVLEN,
    (700, 1e6): "Infrared Light",
    (1e7, 1e10): "Micro Wave",
    (1e10, INF.value): "Radio Wave",
}


def spectrum_label(
    λ: float,
    spectrum_map: dict[tuple[float, float], str | dict[tuple[float, float], str]],
) -> str:
    """Return the spectrum label (e.g. `Radio Wave` or `X-Ray`) by checking recursively for wavelength `λ` in `spectrum_map`."""
    for (low, high), value in spectrum_map.items():
        if low <= λ < high:
            if isinstance(value, dict):
                return spectrum_label(λ, dict(value))

            return value
    raise ValueError(f"Wavelength {λ!r} is out of range for this spectrum map")


def λ(Hz: float) -> Quantity:
    """Return wavelength `λ` from `Hertz`."""
    return Quantity(C / Hz * 1e9, METER)  # 1e9 to convert from nm to m


def Hz(λ: float) -> Quantity:
    """Return `Hertz` from wavelength `λ`."""
    return Quantity(C / λ * 1e9, METER)


def ems(λ: float) -> tuple[str, float, str]:
    """Get the part of the electromagnetic spectrum the wavelength `λ` sits in, as well as the hertz."""
    label = spectrum_label(λ, EM_SPEC_WAVLEN)
    hz = float(Hz(λ))

    return label, hz, f"{label} - {hz} Hz"


def photon_energy_λ(λ: float) -> Quantity:
    """Calculate the energy of a photon in joules with wavelength `λ`."""
    return Quantity(PLANCK * Hz(λ), JOULE)


def photon_energy_hz(Hz: float) -> Quantity:
    """Calculate the energy of a photon in joules with frequency `Hz`."""
    return Quantity(PLANCK * Hz, JOULE)


def photon_energy_ev_λ(λ: float) -> Quantity:
    """Calculate the energy of a photon with wavelength `λ` in electron volts."""
    return Quantity(photon_energy_λ(λ) / 1.60218e-19, ELECTRONVOLT)


def photon_energy_ev_hz(Hz: float) -> Quantity:
    """Calculate the energy of a photon with frequency `Hz` in electron volts."""
    return Quantity(photon_energy_hz(Hz) / 1.60218e-19, ELECTRONVOLT)
