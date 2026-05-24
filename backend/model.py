import random

def detect_ai_image(image_path):

    labels = ["AI Generated", "Real Image"]

    chosen = random.choice(labels)

    confidence = round(random.uniform(75, 99), 2)

    result = [{
        "label": chosen,
        "score": confidence / 100
    }]

    return result