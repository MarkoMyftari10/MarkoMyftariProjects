// Handle task status updates
async function updateTask(taskId, isCompleted) {
    try {
        const response = await fetch('/update_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                task_id: taskId,
                completed: isCompleted
            })
        });

        if (!response.ok) {
            throw new Error('Failed to update task');
        }

        const data = await response.json();
        
        // Update UI based on response
        if (data.success) {
            // Show success notification
            showNotification('Task updated successfully', 'success');
            
            // Update progress bar if provided in response
            if (data.weekly_progress !== undefined) {
                updateProgressBar(data.weekly_progress);
            }

            // If task is rescheduled, update the UI
            if (data.rescheduled) {
                showNotification('Incomplete task rescheduled for tomorrow', 'info');
            }
        }

    } catch (error) {
        console.error('Error updating task:', error);
        showNotification('Failed to update task', 'error');
        
        // Revert checkbox state on error
        const checkbox = document.querySelector(`input[data-task-id="${taskId}"]`);
        if (checkbox) {
            checkbox.checked = !isCompleted;
        }
    }
}

// Update progress bar visualization
function updateProgressBar(percentage) {
    const progressBar = document.querySelector('.progress');
    const progressText = document.querySelector('.progress-stats span');
    
    if (progressBar && progressText) {
        progressBar.style.width = `${percentage}%`;
        progressText.textContent = `${percentage}% Complete`;
    }
}

// Notification system
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    // Add notification to the page
    const container = document.querySelector('.dashboard-container');
    container.appendChild(notification);

    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Initialize dashboard features
document.addEventListener('DOMContentLoaded', () => {
    // Set up task time sorting
    setupTaskSorting();
    
    // Initialize progress tracking
    initializeProgress();

    document.querySelectorAll('.progress').forEach(progress => {
        const width = progress.dataset.progress;
        progress.style.setProperty('--progress-width', width + '%');
    });
});

// Sort tasks by time
function setupTaskSorting() {
    const taskList = document.querySelector('.task-list');
    if (taskList) {
        const tasks = Array.from(taskList.children);
        tasks.sort((a, b) => {
            const timeA = a.querySelector('.task-time').textContent;
            const timeB = b.querySelector('.task-time').textContent;
            return timeA.localeCompare(timeB);
        });
        
        tasks.forEach(task => taskList.appendChild(task));
    }
}

// Initialize progress tracking
function initializeProgress() {
    // Add any initial progress calculations or visualizations
    const checkboxes = document.querySelectorAll('.task-item input[type="checkbox"]');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            // Prevent default checkbox behavior until server confirms
            e.preventDefault();
            
            const taskId = checkbox.id.replace('task-', '');
            updateTask(taskId, checkbox.checked);
        });
    });
} 