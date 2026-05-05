# src/features/solar_logic.py

import numpy as np

# ---------------------------
#  BASIC SOLAR YIELD
# ---------------------------

def calculate_yield(ghi, area=1.5, efficiency=0.20):
    """
    Convert irradiance (W/m²) → energy output (kWh)
    """
    return (ghi * area * efficiency) / 1000


# ---------------------------
#  CLOUD IMPACT
# ---------------------------

def cloud_efficiency_loss(cloud_cover):
    """
    Non-linear cloud loss (0 → 1)
    """
    return np.clip((cloud_cover / 100) ** 1.2, 0, 1)


# ---------------------------
#  TEMPERATURE IMPACT
# ---------------------------

def temperature_efficiency(temp):
    """
    Solar panels lose efficiency above 25°C
    Typical loss ≈ 0.4% per °C
    """
    loss = (temp - 25) * 0.004
    return np.clip(1 - loss, 0.75, 1.05)


# ---------------------------
#  FINAL ADJUSTED OUTPUT
# ---------------------------

def adjusted_yield(
    ghi,
    cloud_cover,
    temp=25,
    area=1.5,
    efficiency=0.20
):
    """
    Real-world solar output (kWh)
    Includes cloud + temperature effects
    """

    cloud_loss = cloud_efficiency_loss(cloud_cover)
    temp_factor = temperature_efficiency(temp)

    effective_eff = efficiency * (1 - cloud_loss) * temp_factor

    return (ghi * area * effective_eff) / 1000


# ---------------------------
#  DEVICE-BASED OUTPUT
# ---------------------------

def device_output(ghi, device_config, cloud_cover=0, temp=25):
    """
    Calculate output based on device profile
    """

    return adjusted_yield(
        ghi=ghi,
        cloud_cover=cloud_cover,
        temp=temp,
        area=device_config["area"],
        efficiency=device_config["efficiency"]
    )


# ---------------------------
#  SOLAR QUALITY CLASSIFIER
# ---------------------------

def classify_irradiance(ghi):
    """
    Categorize sunlight quality
    """

    if ghi >= 800:
        return "PEAK ⚡"
    elif ghi >= 600:
        return "GOOD ☀️"
    elif ghi >= 400:
        return "MODERATE 🌤️"
    else:
        return "LOW ❌"


# ---------------------------
#  SOLAR WINDOW CHECK
# ---------------------------

def is_good_solar_window(ghi, threshold=600):
    """
    Check if current timestep is usable
    """
    return ghi >= threshold


