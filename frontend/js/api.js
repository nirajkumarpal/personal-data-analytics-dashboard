const API_BASE_URL = 'http://localhost:5001/api';

const api = {
    _request: async (endpoint, options = {}) => {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                ...options,
                headers: { 'Content-Type': 'application/json', ...options.headers }
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'API Request Failed');
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    auth: {
        login: (email, password) => api._request('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
        register: (username, email, password) => api._request('/auth/register', { method: 'POST', body: JSON.stringify({ username, email, password }) })
    },

    logs: {
        add: (logData) => api._request('/logs/add', { method: 'POST', body: JSON.stringify(logData) }),
        fetch: (userId) => api._request(`/logs/fetch?user_id=${userId}`),
        update: (logId, data) => api._request(`/logs/update/${logId}`, { method: 'PUT', body: JSON.stringify(data) }),
        delete: (logId, userId) => api._request(`/logs/delete/${logId}?user_id=${userId}`, { method: 'DELETE' }),
        updateTaskStatus: (logId, taskId, userId, isCompleted) => api._request(`/logs/${logId}/tasks/${taskId}/status`, {
            method: 'PUT',
            body: JSON.stringify({ user_id: userId, is_completed: isCompleted })
        })
    },

    analytics: {
        getSummary: (userId) => api._request(`/analytics/summary?user_id=${userId}`)
    },

    goals: {
        set: (userId, studyGoal) => api._request('/goals/set', { method: 'POST', body: JSON.stringify({ user_id: userId, study_goal: studyGoal }) }),
        get: (userId) => api._request(`/goals/get?user_id=${userId}`)
    }
};

const auth = {
    getUser: () => {
        try {
            const localUser = localStorage.getItem('user');
            if (localUser) return JSON.parse(localUser);

            const sessionUser = sessionStorage.getItem('user');
            if (sessionUser) return JSON.parse(sessionUser);
        } catch (error) {
            localStorage.removeItem('user');
            sessionStorage.removeItem('user');
        }
        return null;
    },
    setUser: (user, remember = true) => {
        const payload = JSON.stringify(user);
        if (remember) {
            localStorage.setItem('user', payload);
            sessionStorage.removeItem('user');
        } else {
            sessionStorage.setItem('user', payload);
            localStorage.removeItem('user');
        }
    },
    logout: () => {
        localStorage.removeItem('user');
        sessionStorage.removeItem('user');
        window.location.href = 'login.html';
    },
    requireAuth: () => {
        const user = auth.getUser();
        const path = window.location.pathname || '';
        const isAuthPage = path.indexOf('login.html') !== -1 || path.indexOf('register.html') !== -1;
        if (!user && !isAuthPage) window.location.href = 'login.html';
        return user;
    }
};
