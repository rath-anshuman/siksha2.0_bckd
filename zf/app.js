const BASE_URL = 'http://127.0.0.1:8000';

const loginForm = document.getElementById('login-form');
const dashboardSection = document.getElementById('dashboard-section');
const loginSection = document.getElementById('login-section');

// Elements to display user data
const userName = document.getElementById('user-name');
const userEmail = document.getElementById('user-email');
const userSection = document.getElementById('user-section');
const userRegNo = document.getElementById('user-regno');
const logoutButton = document.getElementById('logout-button');

// Login User
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${BASE_URL}/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('token', data.token); // Save token for authentication
            fetchUserData();
        } else {
            alert(data.error);
        }
    } catch (err) {
        console.error(err);
        alert('Error logging in. Please try again.');
    }
});

// Fetch User Data
async function fetchUserData() {
    try {
        const token = localStorage.getItem('token');

        if (!token) {
            alert('User not logged in!');
            return;
        }

        const response = await fetch(`${BASE_URL}/get_user_data/`, {
            method: 'GET',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` 
            },
        });

        const data = await response.json();

        if (response.ok) {
            // Populate user data
            userName.textContent = data.name;
            userEmail.textContent = data.email;
            userSection.textContent = data.section;
            userRegNo.textContent = data.regno;

            // Show dashboard and hide login
            loginSection.style.display = 'none';
            dashboardSection.style.display = 'block';
        } else {
            alert(data.error);
        }
    } catch (err) {
        console.error(err);
        alert('Error fetching user data.');
    }
}

// Logout
logoutButton.addEventListener('click', () => {
    localStorage.removeItem('token'); // Clear token
    loginSection.style.display = 'block';
    dashboardSection.style.display = 'none';
});
