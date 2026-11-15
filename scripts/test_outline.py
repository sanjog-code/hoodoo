import math

def get_sneaker_perimeter_point(u, scale_x=1.0, scale_y=1.0):
    """
    Returns (x, y) along the perimeter of an authentic skate low sneaker last.
    u ranges from 0 to 2*pi.
    u = 0 is rear heel center (y = -0.125).
    u = pi is front toe center (y = +0.145).
    u in (0, pi) is lateral side (positive X).
    u in (pi, 2*pi) is medial side (negative X).
    """
    # Parameterize normalized length along shoe: t in [0, 1]
    # Heel at t=0, Toe at t=1
    cos_u = math.cos(u)
    sin_u = math.sin(u)
    
    # y position along foot
    # Map cos(u) from [1, -1] to [-0.125, +0.145]
    # Heel is at u=0 (cos=1 -> y=-0.125)
    # Toe is at u=pi (cos=-1 -> y=+0.145)
    y = 0.010 - 0.135 * cos_u
    t = (y + 0.125) / 0.270
    t = max(0.0, min(1.0, t))
    
    # Width calculation based on t (heel to toe)
    if t < 0.20:
        # Heel: smooth parabolic arc, max half-width ~36mm
        w = 0.036 * math.sqrt(max(0.01, 1.0 - ((0.20 - t) / 0.20) ** 2))
    elif t < 0.50:
        # Waist / Arch: tapers to ~33mm on medial side, ~37mm on lateral side
        f = (t - 0.20) / 0.30
        w_lat = 0.036 + 0.002 * math.sin(f * math.pi)
        w_med = 0.036 - 0.006 * math.sin(f * math.pi) # medial arch cutout
        w = w_lat if sin_u >= 0 else w_med
    elif t < 0.82:
        # Ball of foot: flares out to ~46mm lateral, ~42mm medial
        f = (t - 0.50) / 0.32
        w_lat = 0.038 + 0.009 * math.sin(f * math.pi * 0.9)
        w_med = 0.030 + 0.012 * math.sin(f * math.pi * 0.9)
        w = w_lat if sin_u >= 0 else w_med
    else:
        # Toe dome: rounded broad skate box
        f = (t - 0.82) / 0.18
        w = 0.046 * math.sqrt(max(0.01, 1.0 - f ** 1.8))
        
    x = (w if sin_u >= 0 else -w) * math.sin(abs(u if u <= math.pi else (2*math.pi - u)))
    # Ensure smooth transition across midline at u=0 and u=pi
    blend = abs(sin_u)
    x = x * (blend ** 0.5)
    
    return x * scale_x, y * scale_y
