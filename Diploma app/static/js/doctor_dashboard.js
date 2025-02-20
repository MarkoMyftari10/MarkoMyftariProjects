// Global modal reference
const modal = document.getElementById('patientModal');

function viewPatientDetails(patientId) {
    fetch(`/patient_details/${patientId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(patient => {
            showPatientModal(patient);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load patient details. Please try again.');
        });
}

function showPatientModal(patient) {
    const modalHtml = `
        <div class="modal" id="patientModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>${patient.name}</h2>
                    <span class="close-modal" onclick="closeModal()">&times;</span>
                </div>
                <div class="modal-body">
                    <div class="patient-details">
                        <img src="/static/images/${patient.image}" alt="${patient.name}" class="modal-patient-image">
                        <p><strong>Condition:</strong> ${patient.condition}</p>
                        <p><strong>Diagnosis:</strong> ${patient.diagnosis}</p>
                        <div class="progress-section">
                            <p><strong>Progress:</strong></p>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${patient.weekly_progress}%"></div>
                            </div>
                            <p>${patient.weekly_progress}%</p>
                        </div>
                        <p><strong>Treatment Week:</strong> ${patient.treatment_week} of ${patient.total_weeks}</p>
                        <p><strong>Next Appointment:</strong> ${patient.next_appointment}</p>
                        
                        <div class="tasks-section">
                            <h3>Daily Tasks</h3>
                            ${patient.daily_tasks.map(task => `
                                <div class="task-item">
                                    <span>${task.time} - ${task.name}</span>
                                    <span class="status ${task.completed ? 'status-completed' : 'status-pending'}">
                                        ${task.completed ? 'Completed' : 'Pending'}
                                    </span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Remove existing modal if any
    const existingModal = document.getElementById('patientModal');
    if (existingModal) {
        existingModal.remove();
    }

    // Add new modal
    document.body.insertAdjacentHTML('beforeend', modalHtml);

    // Show modal with animation
    setTimeout(() => {
        const modal = document.getElementById('patientModal');
        modal.classList.add('show');
    }, 10);
}

function closeModal() {
    const modal = document.getElementById('patientModal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.remove();
        }, 300);
    }
}

function populatePatientCards() {
    const patientsGrid = document.querySelector('.patients-grid');
    const patients = [
        {
            id: 1,
            name: 'John Doe',
            image: 'patient1.jpg',
            condition: 'Post-Surgery Recovery',
            progress: 75
        },
        {
            id: 2,
            name: 'Jane Smith',
            image: 'patient2.jpg',
            condition: 'Sports Injury',
            progress: 60
        },
        {
            id: 3,
            name: 'Mike Johnson',
            image: 'patient3.jpg',
            condition: 'Chronic Pain',
            progress: 45
        },
        {
            id: 4,
            name: 'Sarah Williams',
            image: 'patient4.jpg',
            condition: 'Rehabilitation',
            progress: 85
        }
    ];

    patientsGrid.innerHTML = patients.map(patient => `
        <div class="patient-card" onclick="viewPatientDetails(${patient.id})">
            <img src="/static/images/${patient.image}" alt="${patient.name}" class="patient-image">
            <div class="patient-info">
                <h3>${patient.name}</h3>
                <p>${patient.condition}</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${patient.progress}%"></div>
                </div>
                <p>Progress: ${patient.progress}%</p>
            </div>
        </div>
    `).join('');
}

document.addEventListener('DOMContentLoaded', function() {
    populatePatientCards();
});

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target == modal) {
        closeModal();
    }
}

// Initialize dashboard components
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded'); // Debug log
    populatePatientCards();
    initializeCalendar();
    initializeCharts();
    setupSearchAndFilters();
});

// Calendar initialization with appointments
function initializeCalendar() {
    const calendar = new FullCalendar.Calendar(document.getElementById('appointmentCalendar'), {
        initialView: 'dayGridWeek',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,dayGridWeek,dayGridDay'
        },
        events: [
            {
                title: 'John Doe - Follow-up',
                start: '2024-03-22T10:00:00',
                end: '2024-03-22T11:00:00',
                color: '#4CAF50'
            },
            // ... more appointments
        ],
        eventClick: function(info) {
            showAppointmentDetails(info.event);
        }
    });
    calendar.render();
}

// Analytics charts initialization
function initializeCharts() {
    // Patient Progress Chart
    const progressCtx = document.getElementById('progressChart').getContext('2d');
    new Chart(progressCtx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'Average Patient Progress',
                data: [30, 45, 60, 75],
                borderColor: '#4CAF50',
                tension: 0.1
            }]
        }
    });

    // Treatment Distribution Chart
    const distributionCtx = document.getElementById('treatmentDistribution').getContext('2d');
    new Chart(distributionCtx, {
        type: 'doughnut',
        data: {
            labels: ['Post-Surgery', 'Sports Injury', 'Chronic Pain', 'Rehabilitation'],
            datasets: [{
                data: [30, 25, 20, 25],
                backgroundColor: ['#4CAF50', '#2196F3', '#FFC107', '#9C27B0']
            }]
        }
    });
}

// Search and filter functionality
function setupSearchAndFilters() {
    const searchInput = document.getElementById('patientSearch');
    const conditionFilter = document.getElementById('conditionFilter');

    searchInput.addEventListener('input', filterPatients);
    conditionFilter.addEventListener('change', filterPatients);
}

function filterPatients() {
    const searchTerm = document.getElementById('patientSearch').value.toLowerCase();
    const condition = document.getElementById('conditionFilter').value;
    const patientCards = document.querySelectorAll('.patient-card');

    patientCards.forEach(card => {
        const name = card.querySelector('h3').textContent.toLowerCase();
        const patientCondition = card.querySelector('.condition').textContent.toLowerCase();
        
        const matchesSearch = name.includes(searchTerm);
        const matchesCondition = !condition || patientCondition.includes(condition);

        card.style.display = matchesSearch && matchesCondition ? 'block' : 'none';
    });
}

// Add new patient functionality
function showAddPatientModal() {
    const modal = document.getElementById('addPatientModal');
    modal.style.display = 'block';
}

function handleAddPatient(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    fetch('/add_patient', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Patient added successfully');
            populatePatientCards();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to add patient');
    });
} 