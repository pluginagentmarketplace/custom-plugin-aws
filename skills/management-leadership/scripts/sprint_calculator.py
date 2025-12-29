#!/usr/bin/env python3
"""Sprint metrics calculator."""

def calculate_velocity(sprints: list) -> dict:
    """Calculate team velocity stats."""
    if not sprints:
        return {"error": "No data"}

    avg = sum(sprints) / len(sprints)
    return {
        "average_velocity": round(avg, 1),
        "last_sprint": sprints[-1],
        "trend": "up" if len(sprints) > 1 and sprints[-1] > sprints[-2] else "down",
        "recommended_commitment": round(avg * 0.9, 0)
    }

if __name__ == "__main__":
    velocities = [21, 23, 19, 25, 22]
    print(calculate_velocity(velocities))
