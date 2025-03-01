#!/usr/bin/env python3
import os
import sys
import json
import random
from datetime import datetime, timedelta

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


def generate_sample_resources():
    """Generate sample resource data."""
    machinery = [
        {
            "id": f"machine_{i}",
            "type": random.choice(["tractor", "harvester", "irrigation_system", "sprayer"]),
            "model": f"Model {random.randint(100, 999)}",
            "year": random.randint(2010, 2023),
            "maintenance_status": random.choice(
                ["operational", "needs_repair", "scheduled_maintenance"]
            ),
        }
        for i in range(10)
    ]

    personnel = [
        {
            "id": f"employee_{i}",
            "name": f"Employee {i}",
            "role": random.choice(["farm_manager", "agronomist", "field_worker", "mechanic"]),
            "skills": random.sample(
                ["irrigation", "crop_management", "machinery_repair", "pest_control"],
                random.randint(1, 4),
            ),
        }
        for i in range(15)
    ]

    usage_log = []
    for machine in machinery:
        for _ in range(random.randint(1, 5)):
            usage_log.append(
                {
                    "machine_id": machine["id"],
                    "date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime(
                        "%Y-%m-%d"
                    ),
                    "hours_used": random.uniform(0.5, 8),
                    "operator_id": random.choice(personnel)["id"],
                    "task": random.choice(["planting", "harvesting", "irrigation", "maintenance"]),
                }
            )

    return {"machinery": machinery, "personnel": personnel, "usage_log": usage_log}


def generate_sample_climate_data():
    """Generate sample climate data for different regions."""
    regions = ["Central Valley", "Coastal Area", "Mountain Region", "Southern Plains"]
    climate_data = {}

    for region in regions:
        climate_data[region] = {
            "average_temperature": {
                "winter": round(random.uniform(5, 15), 1),
                "summer": round(random.uniform(20, 35), 1),
            },
            "annual_rainfall": round(random.uniform(300, 1500), 1),
            "soil_types": random.sample(
                ["clay", "sandy", "loam", "silt", "peat"], random.randint(1, 3)
            ),
            "frost_days": random.randint(0, 30),
        }

    return climate_data


def generate_sample_crop_data():
    """Generate sample crop data."""
    crops = {
        "wheat": {
            "optimal_temperature_range": {"min": 10, "max": 25},
            "water_requirement": round(random.uniform(300, 600), 1),
            "growing_season_length": random.randint(90, 150),
            "recommended_fertilizers": random.sample(
                ["nitrogen", "phosphorus", "potassium"], random.randint(1, 3)
            ),
        },
        "corn": {
            "optimal_temperature_range": {"min": 15, "max": 35},
            "water_requirement": round(random.uniform(500, 800), 1),
            "growing_season_length": random.randint(90, 120),
            "recommended_fertilizers": random.sample(
                ["nitrogen", "phosphorus", "potassium"], random.randint(1, 3)
            ),
        },
        "avocado": {
            "optimal_temperature_range": {"min": 10, "max": 30},
            "water_requirement": round(random.uniform(800, 1200), 1),
            "growing_season_length": random.randint(180, 270),
            "recommended_fertilizers": random.sample(
                ["nitrogen", "phosphorus", "potassium"], random.randint(1, 3)
            ),
        },
    }
    return crops


def save_sample_data():
    """Save generated sample data to JSON files."""
    data_dir = os.path.join(project_root, "data")
    os.makedirs(data_dir, exist_ok=True)

    # Save resources data
    resources = generate_sample_resources()
    for resource_type, data in resources.items():
        with open(os.path.join(data_dir, f"{resource_type}_data.json"), "w") as f:
            json.dump(data, f, indent=2)

    # Save climate data
    climate_data = generate_sample_climate_data()
    with open(os.path.join(data_dir, "climate_data.json"), "w") as f:
        json.dump(climate_data, f, indent=2)

    # Save crop data
    crop_data = generate_sample_crop_data()
    with open(os.path.join(data_dir, "crops_data.json"), "w") as f:
        json.dump(crop_data, f, indent=2)

    print("Sample data generated successfully.")


def main():
    try:
        save_sample_data()
    except Exception as e:
        print(f"Error generating sample data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
