// Authentication Manager
class AuthManager {
    constructor() {
        this.users = JSON.parse(localStorage.getItem('users')) || [];
    }

    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }

    validatePassword(password) {
        const re = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
        return re.test(password);
    }

    validateUsername(username) {
        const re = /^[a-zA-Z0-9_]{3,}$/;
        return re.test(username);
    }

    isUsernameTaken(username) {
        return this.users.some(user => user.username === username);
    }

    register(username, password, email, isAdmin = false) {
        if (!this.validateUsername(username)) {
            throw new Error('Username must be at least 3 characters long and contain only letters, numbers, and underscores');
        }

        if (!this.validatePassword(password)) {
            throw new Error('Password must be at least 8 characters long and contain at least one number and one letter');
        }

        if (!this.validateEmail(email)) {
            throw new Error('Please enter a valid email address');
        }

        if (this.isUsernameTaken(username)) {
            throw new Error('Username is already taken');
        }

        const user = {
            username,
            password,
            email,
            isAdmin,
            createdAt: new Date().toISOString()
        };

        this.users.push(user);
        localStorage.setItem('users', JSON.stringify(this.users));
        return user;
    }

    login(username, password) {
        const user = this.users.find(u => u.username === username && u.password === password);
        if (!user) {
            throw new Error('Invalid username or password');
        }
        return user;
    }

    getCurrentUser() {
        return JSON.parse(localStorage.getItem('currentUser'));
    }

    logout() {
        localStorage.removeItem('currentUser');
    }
}

function showError(input, message) {
    const formControl = input.parentElement;
    const errorDisplay = formControl.querySelector('.error');
    
    if (!errorDisplay) {
        const errorElement = document.createElement('small');
        errorElement.className = 'error';
        errorElement.textContent = message;
        formControl.appendChild(errorElement);
    } else {
        errorDisplay.textContent = message;
    }
    
    input.classList.add('error-border');
}

function clearError(input) {
    const formControl = input.parentElement;
    const errorDisplay = formControl.querySelector('.error');
    
    if (errorDisplay) {
        formControl.removeChild(errorDisplay);
    }
    
    input.classList.remove('error-border');
}

const authManager = new AuthManager();

function validateSignUp(event) {
    event.preventDefault();
    
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm-password');
    const email = document.getElementById('email');
    
    [username, password, confirmPassword, email].forEach(clearError);
    
    try {
        if (password.value !== confirmPassword.value) {
            throw new Error('Passwords do not match');
        }

        const isAdmin = document.getElementById('is-admin')?.checked || false;
        const user = authManager.register(
            username.value,
            password.value,
            email.value,
            isAdmin
        );

        localStorage.setItem('currentUser', JSON.stringify(user));
        window.location.href = 'login.html';
    } catch (error) {
        showError(username, error.message);
        showError(password, error.message);
        showError(confirmPassword, error.message);
        showError(email, error.message);
    }
    
    return false;
}

function validateLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    
    [username, password].forEach(clearError);
    
    try {
        const user = authManager.login(username.value, password.value);
        localStorage.setItem('currentUser', JSON.stringify(user));
        window.location.href = 'recipes_list.html';
    } catch (error) {
        showError(username, error.message);
        showError(password, error.message);
    }
    
    return false;
}

document.addEventListener('DOMContentLoaded', function() {
    const signUpForm = document.getElementById('signup-form');
    if (signUpForm) {
        signUpForm.onsubmit = validateSignUp;
    }
    
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.onsubmit = validateLogin;
    }
});