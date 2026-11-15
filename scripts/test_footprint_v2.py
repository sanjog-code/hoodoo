import math

def get_skate_perimeter_points(n_heel=8, n_waist=6, n_ball=8, n_toe=10):
    """
    Constructs an authentic skate last perimeter loop (like Nike SB Dunk Low)
    by defining key anatomical arcs and connecting them with smooth splines.
    Total vertices around the perimeter = 2 * (n_heel + n_waist + n_ball) + n_toe = ~40 vertices.
    """
    pts = []
    
    # 1. Heel Cup: Semicircular arc from lateral heel to medial heel
    # Centered at (0, -0.090), radius 0.030, y from -0.090 to -0.120
    heel_pts = []
    for i in range(10):
        # Angle from -pi/2 (lateral side, x>0) down to -pi (rear) to -3pi/2 (medial side, x<0)
        ang = -math.pi/2 - (i / 9.0) * math.pi
        hx = 0.030 * math.cos(ang)
        hy = -0.090 + 0.030 * math.sin(ang)
        heel_pts.append((hx, hy))
        
    # 2. Medial Side (from heel to waist arch to ball of foot)
    # y goes from -0.090 up to +0.055
    medial_pts = [
        (-0.030, -0.070),
        (-0.027, -0.045),
        (-0.024, -0.020),  # Inset arch
        (-0.026,  0.005),
        (-0.034,  0.030),  # Flaring out to ball
        (-0.044,  0.055),  # Ball of foot (widest medial point)
        (-0.042,  0.080),
        (-0.036,  0.102),
    ]
    
    # 3. Toe Bumper Arc: Broad rounded skate curve (radius ~28mm)
    # Centered at (0.002, 0.102), curving around from medial to lateral
    toe_pts = []
    for i in range(11):
        # Angle from -math.pi (medial) up to 0 (lateral)
        ang = math.pi - (i / 10.0) * math.pi
        # Slightly biased towards big toe (asymmetric medial side)
        rx = 0.038 if ang > math.pi/2 else 0.042
        ry = 0.028
        tx = rx * math.cos(ang) + 0.002
        ty = 0.102 + ry * math.sin(ang)
        toe_pts.append((tx, ty))
        
    # 4. Lateral Side (from toe back to lateral heel)
    lateral_pts = [
        ( 0.044,  0.080),
        ( 0.048,  0.055),  # Ball of foot (widest lateral point)
        ( 0.044,  0.030),
        ( 0.038,  0.005),
        ( 0.035, -0.020),
        ( 0.033, -0.045),
        ( 0.031, -0.070),
    ]
    
    # Combine counter-clockwise around perimeter:
    # Toe arc (from medial to lateral) -> Lateral side (forward to rear) -> Heel arc (lateral to medial) -> Medial side (rear to forward)
    # Start at front-most toe point:
    return toe_pts, lateral_pts, heel_pts, medial_pts

if __name__ == "__main__":
    toe, lat, heel, med = get_skate_perimeter_points()
    print(f"Toe points: {len(toe)}")
    for x, y in toe:
        print(f"  Toe: x={x*1000:6.1f}mm, y={y*1000:6.1f}mm")
    print(f"Heel points: {len(heel)}")
    for x, y in heel:
        print(f"  Heel: x={x*1000:6.1f}mm, y={y*1000:6.1f}mm")
