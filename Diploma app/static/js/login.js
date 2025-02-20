document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const userType = document.querySelector('input[name="user_type"]:checked').value;
        const username = document.getElementById('username').value;
        const passcode = document.getElementById('passcode').value;

        console.log('Attempting login with:', { userType, username }); // Debug log

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                user_type: userType,
                username: username,
                passcode: passcode
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirect based on user type
                window.location.href = userType === 'doctor' ? '/doctor_dashboard' : '/patient_dashboard';
            } else {
                throw new Error(data.error || 'Login failed');
            }
        })
        .catch(error => {
            console.error('Login error:', error);
            alert('Login failed: ' + (error.message || 'Please try again'));
        });
    });
}); 