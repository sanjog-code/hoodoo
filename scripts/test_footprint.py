import math

def generate_skate_footprint(N=32):
    """
    Generates N perimeter vertices (x, y) of an authentic skate sneaker last (US Men's 9).
    Angle theta runs from 0 (toe front) counter-clockwise:
    - theta = 0: Toe front (y = +0.130m, x = 0.0)
    - theta = pi/2: Lateral side (x > 0)
    - theta = pi: Heel rear (y = -0.115m, x = 0.0)
    - theta = 3*pi/2: Medial side (x < 0)
    """
    pts = []
    for i in range(N):
        th = i * (2.0 * math.pi / N)
        cos_t = math.cos(th)
        sin_t = math.sin(th)

        # Longitudinal position Y:
        # Front toe at +0.130m, rear heel at -0.115m
        # Length = 245mm
        y = 0.0075 + 0.1225 * cos_t

        # Normalized t from 0 (heel) to 1 (toe)
        t = (y + 0.115) / 0.245
        t = max(0.0, min(1.0, t))

        # Width at station t:
        # Heel: width ~66mm (x ~ 33mm)
        # Waist: medial drops to 24mm, lateral stays at 35mm
        # Forefoot: width ~92mm (lateral ~48mm, medial ~44mm)
        # Toe bumper: broad rounded curve (radius ~32mm)
        if t < 0.25:
            # Rounded heel cup
            f = t / 0.25
            r_h = math.sqrt(max(0.1, 1.0 - ((1.0 - f) ** 2)))
            w_lat = 0.033 * (0.65 + 0.35 * r_h)
            w_med = 0.032 * (0.65 + 0.35 * r_h)
        elif t < 0.55:
            # Waist / Arch
            f = (t - 0.25) / 0.30
            w_lat = 0.033 + 0.003 * math.sin(f * math.pi)
            w_med = 0.032 - 0.008 * math.sin(f * math.pi)  # Medial arch hollow
        elif t < 0.82:
            # Forefoot / Ball of foot
            f = (t - 0.55) / 0.27
            w_lat = 0.036 + 0.012 * math.sin(f * math.pi * 0.95)
            w_med = 0.024 + 0.020 * math.sin(f * math.pi * 0.95)
        else:
            # Broad skate toe box
            f = (t - 0.82) / 0.18
            # Rounded dome curve
            r_t = math.sqrt(max(0.1, 1.0 - (f ** 1.6)))
            w_lat = 0.047 * (0.55 + 0.45 * r_t)
            w_med = 0.043 * (0.55 + 0.45 * r_t)

        x = w_lat * sin_t if sin_t >= 0 else w_med * sin_t
        pts.append((x, y, t))
    return pts

if __name__ == "__main__":
    footprint = generate_skate_footprint(32)
    print("Footprint generated: 32 vertices")
    for i, (x, y, t) in enumerate(footprint):
        print(f"[{i:02d}] x={x*1000:6.1f}mm, y={y*1000:6.1f}mm, t={t:.2f}")
