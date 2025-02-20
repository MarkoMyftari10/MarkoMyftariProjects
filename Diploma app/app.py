from flask import Flask, render_template, request, redirect, session, url_for, jsonify, flash
import os
import json
from datetime import datetime, timedelta
import hashlib
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a real secret key

PATIENTS_DATA_DIR = 'patients_data'

# Define templates variable
templates = [
    {
        'id': 1,
        'name': 'Post-Surgery Recovery',
        'duration': '12 weeks',
        'phases': [
            {
                'name': 'Initial Recovery',
                'duration': '2 weeks',
                'exercises': [
                    {'name': 'Gentle ROM', 'frequency': '3x daily', 'duration': '10 mins'},
                    {'name': 'Ice Therapy', 'frequency': '4x daily', 'duration': '15 mins'}
                ]
            },
            {
                'name': 'Strength Building',
                'duration': '4 weeks',
                'exercises': [
                    {'name': 'Resistance Band', 'frequency': '2x daily', 'duration': '15 mins'},
                    {'name': 'Weight Training', 'frequency': '1x daily', 'duration': '20 mins'}
                ]
            }
        ]
    }
]

# Define notifications variable
notifications = []

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

def ensure_data_directory():
    """Create data directory if it doesn't exist"""
    if not os.path.exists(PATIENTS_DATA_DIR):
        os.makedirs(PATIENTS_DATA_DIR)
        print(f"Created directory: {PATIENTS_DATA_DIR}")

def load_patient_data(passcode):
    """Load patient data from file"""
    file_path = os.path.join(PATIENTS_DATA_DIR, f'patient_{passcode}.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.loads(f.read())
    return None

def load_doctor_data(passcode):
    """Load doctor data from file"""
    file_path = os.path.join(PATIENTS_DATA_DIR, f'doctor_{passcode}.txt')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.loads(f.read())
    return None

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print("Login attempt data:", data)  # Debug print
        
        user_type = data.get('user_type')
        username = data.get('username')
        passcode = data.get('passcode')

        print(f"Attempting login - Type: {user_type}, Username: {username}")  # Debug print

        # Define valid credentials
        valid_credentials = {
            'doctor': {'username': 'doctor', 'passcode': '1234'},
            'patient': {'username': 'patient', 'passcode': '5678'}
        }

        # Check credentials
        if (user_type in valid_credentials and 
            username == valid_credentials[user_type]['username'] and 
            passcode == valid_credentials[user_type]['passcode']):
            
            session.clear()
            session['user_id'] = f"{user_type}_1"
            session['user_type'] = user_type
            session['username'] = username
            
            print(f"Login successful for {user_type}")  # Debug print
            print(f"Session data: {session}")  # Debug print
            
            return jsonify({
                'success': True,
                'redirect': f'/{user_type}_dashboard'
            })
        
        print("Invalid credentials provided")  # Debug print
        return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug print
        return jsonify({'error': 'Login failed'}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    if session.get('user_type') != 'doctor':
        return redirect(url_for('login_page'))
    return render_template('doctor_dashboard.html')

@app.route('/patient_dashboard')
@login_required
def patient_dashboard():
    print("Patient dashboard access - Session:", session)  # Debug print
    if session.get('user_type') != 'patient':
        print("Invalid user type for patient dashboard")  # Debug print
        return redirect(url_for('login_page'))
    return render_template('patient_dashboard.html')

@app.route('/patient_details/<patient_id>')
@login_required
def patient_details(patient_id):
    if session.get('user_type') != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 401

    # Define patient data
    patients_data = {
        '1': {
            'id': 1,
            'name': 'John Doe',
            'image': 'patient1.jpg',
            'condition': 'Post-Surgery Recovery',
            'diagnosis': 'Total Knee Replacement',
            'weekly_progress': 75,
            'treatment_week': 6,
            'total_weeks': 12,
            'next_appointment': 'Tomorrow, 10:00 AM',
            'daily_tasks': [
                {'time': '09:00 AM', 'name': 'Morning Exercise', 'completed': True},
                {'time': '02:00 PM', 'name': 'Physical Therapy', 'completed': False}
            ]
        },
        '2': {
            'id': 2,
            'name': 'Jane Smith',
            'image': 'patient2.jpg',
            'condition': 'Sports Injury',
            'diagnosis': 'ACL Tear',
            'weekly_progress': 60,
            'treatment_week': 4,
            'total_weeks': 8,
            'next_appointment': 'Friday, 2:00 PM',
            'daily_tasks': [
                {'time': '10:00 AM', 'name': 'Strength Training', 'completed': True},
                {'time': '03:00 PM', 'name': 'Ice Therapy', 'completed': True}
            ]
        },
        '3': {
            'id': 3,
            'name': 'Mike Johnson',
            'image': 'patient3.jpg',
            'condition': 'Chronic Pain',
            'diagnosis': 'Lower Back Pain',
            'weekly_progress': 45,
            'treatment_week': 2,
            'total_weeks': 6,
            'next_appointment': 'Next Monday, 11:00 AM',
            'daily_tasks': [
                {'time': '09:30 AM', 'name': 'Stretching Exercises', 'completed': False},
                {'time': '02:30 PM', 'name': 'Heat Therapy', 'completed': True}
            ]
        },
        '4': {
            'id': 4,
            'name': 'Sarah Williams',
            'image': 'patient4.jpg',
            'condition': 'Rehabilitation',
            'diagnosis': 'Post-Stroke Recovery',
            'weekly_progress': 85,
            'treatment_week': 8,
            'total_weeks': 10,
            'next_appointment': 'Thursday, 1:00 PM',
            'daily_tasks': [
                {'time': '09:30 AM', 'name': 'Speech Therapy', 'completed': True},
                {'time': '02:30 PM', 'name': 'Motor Skills Exercise', 'completed': True}
            ]
        }
    }

    try:
        # Convert patient_id to string for dictionary lookup
        patient_id = str(patient_id)
        if patient_id in patients_data:
            response = jsonify(patients_data[patient_id])
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        else:
            return jsonify({'error': f'Patient with ID {patient_id} not found'}), 404
    except Exception as e:
        print(f"Error in patient_details: {str(e)}")
        return jsonify({'error': 'Failed to load patient details'}), 500

@app.route('/doctor/activity_feed')
def activity_feed():
    if 'user_type' not in session or session['user_type'] != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 401
        
    try:
        # Use a default value if passcode is not in session
        passcode = session.get('passcode', None)
        if passcode is None:
            return jsonify({'error': 'Session expired'}), 401
            
        doctor_data = load_doctor_data(passcode)
        return jsonify(doctor_data)
    except Exception as e:
        print(f"Error in activity_feed: {str(e)}")
        return jsonify({'error': 'Failed to load activity feed'}), 500

def get_patient_activities(patient_data):
    """Helper function to get patient activities"""
    activities = []
    today = datetime.now().date()
    
    for task in patient_data['daily_tasks']:
        task_date = datetime.strptime(task['date'], '%Y-%m-%d').date()
        if task_date == today:
            activities.append({
                'time': task['time'],
                'patient_name': patient_data['name'],
                'description': f"{'completed' if task['completed'] else 'scheduled'} {task['name']}"
            })
    
    return activities

@app.route('/update_task', methods=['POST'])
def update_task():
    if 'user_type' not in session or session['user_type'] != 'patient':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.get_json()
        task_id = data.get('task_id')
        completed = data.get('completed')
        
        # Find and update the task in patient's data
        patient_data = {
            'name': 'John Doe',
            'weekly_progress': 75,
            'daily_tasks': [
                {'id': 1, 'time': '09:00 AM', 'name': 'Morning Exercise', 'completed': False},
                {'id': 2, 'time': '02:00 PM', 'name': 'Physical Therapy', 'completed': True}
            ]
        }
        
        # Update the task completion status
        for task in patient_data['daily_tasks']:
            if str(task['id']) == str(task_id):
                task['completed'] = completed
                
                # Recalculate progress
                completed_tasks = sum(1 for t in patient_data['daily_tasks'] if t['completed'])
                total_tasks = len(patient_data['daily_tasks'])
                new_progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
                
                return jsonify({
                    'success': True,
                    'weekly_progress': new_progress
                })
        
        return jsonify({'success': False, 'message': 'Task not found'}), 404
        
    except Exception as e:
        print(f"Error updating task: {str(e)}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

def get_gravatar_url(email, size=80):
    """Get Gravatar URL for an email"""
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"

@app.route('/add_patient', methods=['POST'])
@login_required
def add_patient():
    if session.get('user_type') != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 401
    # Add new patient logic here
    return jsonify({'success': True})

@app.route('/update_treatment/<patient_id>', methods=['POST'])
@login_required
def update_treatment():
    if session.get('user_type') != 'doctor':
        return jsonify({'error': 'Unauthorized'}), 401
    # Update treatment logic here
    return jsonify({'success': True})

@app.route('/schedule_appointment/<patient_id>', methods=['POST'])
@login_required
def schedule_appointment():
    # Appointment scheduling logic
    return jsonify({'success': True})

@app.route('/patient_progress/<patient_id>')
@login_required
def patient_progress(patient_id):
    # Return patient progress data
    progress_data = {
        'pain': [
            {'date': '2024-03-01', 'value': 7},
            {'date': '2024-03-07', 'value': 5},
            {'date': '2024-03-14', 'value': 3}
        ],
        'mobility': [
            {'date': '2024-03-01', 'value': 60},
            {'date': '2024-03-07', 'value': 75},
            {'date': '2024-03-14', 'value': 85}
        ],
        'strength': [
            {'date': '2024-03-01', 'value': 50},
            {'date': '2024-03-07', 'value': 65},
            {'date': '2024-03-14', 'value': 80}
        ]
    }
    return jsonify(progress_data)

@app.route('/treatment_templates')
@login_required
def treatment_templates():
    # Return treatment templates
    return jsonify(templates)

@app.route('/create_treatment_plan', methods=['POST'])
@login_required
def create_treatment_plan():
    # Create new treatment plan
    return jsonify({'success': True})

@app.route('/update_progress', methods=['POST'])
@login_required
def update_progress():
    # Update patient progress
    return jsonify({'success': True})

@app.route('/get_notifications')
@login_required
def get_notifications():
    # Return notifications
    return jsonify(notifications)

if __name__ == '__main__':
    ensure_data_directory()
    app.run(debug=True) 