import numpy as np
from .models import Mehndi

def recommend_designs(features):

    # User feature vector (already extracted)
    user_vector = np.array([
        float(features["palm_width_ratio"]),
        float(features["finger_length_ratio"])
    ])

    designs = Mehndi.objects.all()
    scored = []

    for design in designs:

        db_vector = np.array([
            float(design.palm_width_ratio),
            float(design.finger_length_ratio)
        ])

        # Euclidean Distance
        dist = np.linalg.norm(user_vector - db_vector)

        scored.append((dist, design))

    scored.sort(key=lambda x: x[0])

    return [x[1] for x in scored[:5]]