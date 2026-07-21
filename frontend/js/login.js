document.addEventListener('DOMContentLoaded', () => {
    if (auth.getUser()) {
        window.location.href = 'index.html';
        return;
    }

    const form = document.getElementById('auth-form');
    const errorMsg = document.getElementById('auth-error');
    const successMsg = document.getElementById('auth-success');
    const submitBtn = document.getElementById('auth-submit');
    const passwordInput = document.getElementById('auth-password');
    const toggleBtn = document.getElementById('toggle-password');
    const rememberMeInput = document.getElementById('remember-me');
    const urlParams = new URLSearchParams(window.location.search);

    if (urlParams.get('registered') === '1' && successMsg) {
        successMsg.textContent = 'Account created successfully. Please sign in.';
    }

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

        if (successMsg) successMsg.textContent = '';
        errorMsg.textContent = '';
        submitBtn.disabled = true;
        submitBtn.textContent = 'Signing In...';

        const email = document.getElementById('auth-email').value.trim();
        const password = passwordInput.value.trim();
        const rememberMe = rememberMeInput ? rememberMeInput.checked : true;

        try {
            const res = await api.auth.login(email, password);
            auth.setUser(res.user, rememberMe);
            window.location.href = 'index.html';
        } catch (error) {
            errorMsg.textContent = error.message || 'Invalid email or password';
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Sign In';
        }
    });
});
