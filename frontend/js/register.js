document.addEventListener('DOMContentLoaded', () => {
    if (auth.getUser()) {
        window.location.href = 'index.html';
        return;
    }

    const form = document.getElementById('register-form');
    const errorMsg = document.getElementById('register-error');
    const submitBtn = document.getElementById('register-submit');
    const passwordInput = document.getElementById('register-password');
    const toggleBtn = document.getElementById('toggle-register-password');

    if (toggleBtn && passwordInput) {
        toggleBtn.addEventListener('click', () => {
            const isHidden = passwordInput.type === 'password';
            passwordInput.type = isHidden ? 'text' : 'password';
            toggleBtn.setAttribute('aria-label', isHidden ? 'Hide password' : 'Show password');
            toggleBtn.setAttribute('title', isHidden ? 'Hide password' : 'Show password');
        });
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        errorMsg.textContent = '';
        submitBtn.disabled = true;
        submitBtn.textContent = 'Creating Account...';

        const username = document.getElementById('register-username').value.trim();
        const email = document.getElementById('register-email').value.trim();
        const password = passwordInput.value.trim();

        try {
            const res = await api.auth.register(username, email, password);
            auth.setUser(res.user, true);
            window.location.href = 'index.html';
        } catch (error) {
            errorMsg.textContent = error.message || 'Unable to create account';
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Create Account';
        }
    });
});
