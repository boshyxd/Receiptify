// Auth state observer
firebase.auth().onAuthStateChanged((user) => {
    if (user) {
        // User is signed in
        if (window.location.pathname.includes('login.html')) {
            window.location.href = 'index.html';
        }
    } else {
        // User is signed out
        if (!window.location.pathname.includes('login.html')) {
            window.location.href = 'login.html';
        }
    }
});

function showTab(tabName) {
    // Update button states
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Show selected form
    document.getElementById('login-form').style.display = tabName === 'login' ? 'flex' : 'none';
    document.getElementById('signup-form').style.display = tabName === 'signup' ? 'flex' : 'none';
}

async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        await firebase.auth().signInWithEmailAndPassword(email, password);
        window.location.href = 'index.html';
    } catch (error) {
        showError('login-form', error.message);
    }
}

async function signup() {
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('signup-confirm-password').value;

    if (password !== confirmPassword) {
        showError('signup-form', 'Passwords do not match');
        return;
    }

    try {
        await firebase.auth().createUserWithEmailAndPassword(email, password);
        window.location.href = 'index.html';
    } catch (error) {
        showError('signup-form', error.message);
    }
}

function showError(formId, message) {
    const form = document.getElementById(formId);
    let errorDiv = form.querySelector('.error-message');
    
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        form.appendChild(errorDiv);
    }
    
    errorDiv.textContent = message;
}

function logout() {
    firebase.auth().signOut().then(() => {
        window.location.href = 'login.html';
    }).catch((error) => {
        console.error('Error signing out:', error);
    });
} 