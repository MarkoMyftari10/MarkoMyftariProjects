// Patient search functionality
document.getElementById('patientSearch').addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase();
    const patientCards = document.querySelectorAll('.patient-card');
    
    patientCards.forEach(card => {
        const patientName = card.querySelector('h3').textContent.toLowerCase();
        const patientCondition = card.querySelector('.condition').textContent.toLowerCase();
        
        if (patientName.includes(searchTerm) || patientCondition.includes(searchTerm)) {
            card.style.display = 'flex';
        } else {
            card.style.display = 'none';
        }
    });
});

// View patient details
async function viewPatientDetails(patientId) {
    try {
        const response = await fetch(`/patient_details/${patientId}`);
        if (!response.ok) throw new Error('Failed to fetch patient details');
        
        const data = await response.json();
        showPatientModal(data);
    } catch (error) {
        console.error('Error:', error);
        showNotification('Failed to load patient details', 'error');
    }
}

// Show patient details in modal
function showPatientModal(patient) {
    const modalContent = document.getElementById('modalContent');
    modalContent.innerHTML = `
        <div class="patient-details">
            <div class="patient-header">
                <img src="${url_for('static', filename='images/' + patient.image)}" 
                     alt="${patient.name}" 
                     class="patient-image">
                <h2>${patient.name}</h2>
                <span class="condition-badge ${patient.condition_type}">${patient.condition}</span>
            </div>
            
            <div class="details-grid">
                <div class="detail-section">
                    <h3>Diagnosis</h3>
                    <p>${patient.diagnosis}</p>
                </div>
                
                <div class="detail-section">
                    <h3>Progress</h3>
                    <div class="progress-bar">
                        <div class="progress" style="width: ${patient.weekly_progress}%"></div>
                    </div>
                    <p>${patient.weekly_progress}% Complete</p>
                </div>
                
                <div class="detail-section">
                    <h3>Treatment Timeline</h3>
                    <p>Week ${patient.treatment_week} of ${patient.total_weeks}</p>
                    <p>Next Appointment: ${patient.next_appointment}</p>
                </div>
                
                <div class="detail-section">
                    <h3>Today's Tasks</h3>
                    <ul class="tasks-list">
                        ${patient.daily_tasks ? patient.daily_tasks.map(task => `
                            <li class="${task.completed ? 'completed' : ''}">
                                <span class="task-time">${task.time}</span>
                                <span class="task-name">${task.name}</span>
                            </li>
                        `).join('') : 'No tasks scheduled'}
                    </ul>
                </div>
            </div>
        </div>
    `;
    
    const modal = document.getElementById('patientModal');
    modal.style.display = 'block';
}

// Close modal
function closeModal() {
    const modal = document.getElementById('patientModal');
    modal.style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('patientModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Real-time updates (if implemented)
function initializeRealtimeUpdates() {
    // This could be implemented with WebSocket or Server-Sent Events
    setInterval(async () => {
        const response = await fetch('/doctor/activity_feed');
        if (response.ok) {
            const activities = await response.json();
            updateActivityFeed(activities);
        }
    }, 30000); // Update every 30 seconds
}

// Update activity feed
function updateActivityFeed(activities) {
    const feed = document.querySelector('.activity-feed');
    activities.forEach(activity => {
        const activityElement = document.createElement('div');
        activityElement.className = 'activity-item';
        activityElement.innerHTML = `
            <span class="activity-time">${activity.time}</span>
            <span class="activity-text">
                <strong>${activity.patient_name}</strong> ${activity.description}
            </span>
        `;
        feed.insertBefore(activityElement, feed.firstChild);
    });
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    initializeRealtimeUpdates();
    document.querySelectorAll('.progress').forEach(progress => {
        const width = progress.dataset.progress;
        progress.style.setProperty('--progress-width', width + '%');
    });
}); 