import json
import os

# Sample patient data
patient_data = {
    "12345": {  # Changed patient ID/password to 12345
        "name": "John Doe",
        "id": "12345",  # Updated to match the password
        "condition": "Post-surgery recovery",
        "weekly_progress": 75,
        "daily_tasks": [
            {
                "id": "task1",
                "name": "Morning Walk",
                "time": "08:00",
                "completed": True,
                "date": "2024-03-20"
            },
            {
                "id": "task2",
                "name": "Physical Therapy",
                "time": "10:30",
                "completed": False,
                "date": "2024-03-20"
            }
        ],
        "exercises": [
            {
                "name": "Gentle Stretching",
                "duration": "15 minutes"
            },
            {
                "name": "Leg Raises",
                "duration": "10 reps x 3 sets"
            }
        ],
        "diet": [
            {
                "time": "08:30",
                "description": "High-protein breakfast"
            },
            {
                "time": "12:30",
                "description": "Light lunch with vegetables"
            }
        ]
    }
}

# Sample doctor data
doctor_data = {
    "456": {
        "name": "Dr. Smith",
        "id": "456",
        "assigned_patients": ["12345"],  # Updated to match new patient ID
        "total_patients": 1,
        "active_plans": 1,
        "completed_today": 1,
        "recent_activities": [
            {
                "time": "08:15",
                "patient_name": "John Doe",
                "description": "completed Morning Walk"
            }
        ]
    }
}

# Create directory if it doesn't exist
if not os.path.exists('patients_data'):
    os.makedirs('patients_data')

# Save patient data
for patient_id, data in patient_data.items():
    with open(f'patients_data/patient_{patient_id}.txt', 'w') as f:
        json.dump(data, f, indent=4)

# Save doctor data
for doctor_id, data in doctor_data.items():
    with open(f'patients_data/doctor_{doctor_id}.txt', 'w') as f:
        json.dump(data, f, indent=4)

print("Sample data created successfully!")
print("Patient login: 12345")
print("Doctor login: 456") 