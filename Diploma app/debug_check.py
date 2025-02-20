import os
import json

def check_setup():
    print("\n=== ReviveCycle Debug Check ===\n")

    # 1. Check if patients_data directory exists
    print("1. Checking patients_data directory...")
    if os.path.exists('patients_data'):
        print("✓ patients_data directory found")
    else:
        print("✗ patients_data directory NOT found")
        return

    # 2. Check patient file
    print("\n2. Checking patient file...")
    patient_file = 'patients_data/patient_12345.txt'
    if os.path.exists(patient_file):
        print("✓ patient_12345.txt found")
        try:
            with open(patient_file, 'r') as f:
                patient_data = json.load(f)
                print("✓ Patient data loaded successfully")
                print(f"   Name: {patient_data.get('name', 'Not found')}")
                print(f"   ID: {patient_data.get('id', 'Not found')}")
        except json.JSONDecodeError:
            print("✗ Error: Invalid JSON in patient file")
        except Exception as e:
            print(f"✗ Error reading patient file: {str(e)}")
    else:
        print("✗ patient_12345.txt NOT found")

    # 3. Check doctor file
    print("\n3. Checking doctor file...")
    doctor_file = 'patients_data/doctor_456.txt'
    if os.path.exists(doctor_file):
        print("✓ doctor_456.txt found")
        try:
            with open(doctor_file, 'r') as f:
                doctor_data = json.load(f)
                print("✓ Doctor data loaded successfully")
                print(f"   Name: {doctor_data.get('name', 'Not found')}")
                print(f"   ID: {doctor_data.get('id', 'Not found')}")
        except json.JSONDecodeError:
            print("✗ Error: Invalid JSON in doctor file")
        except Exception as e:
            print(f"✗ Error reading doctor file: {str(e)}")
    else:
        print("✗ doctor_456.txt NOT found")

    # 4. Check templates
    print("\n4. Checking templates...")
    templates = ['templates/index.html', 'templates/patient_dashboard.html', 'templates/doctor_dashboard.html']
    for template in templates:
        if os.path.exists(template):
            print(f"✓ {template} found")
        else:
            print(f"✗ {template} NOT found")

    print("\n=== Debug Check Complete ===\n")

if __name__ == "__main__":
    check_setup() 