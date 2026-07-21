let currentChart = null;

// Escape user-provided text before injecting into HTML.
function escapeHtml(value) {
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

document.addEventListener('DOMContentLoaded', async () => {
    const user = auth.requireAuth();
    if (!user) return;

    document.getElementById('username-display').textContent = user.username;
    document.getElementById('logout-btn').addEventListener('click', auth.logout);

    setupNavigation();
    setupLogForm(user.id);
    setupGoalForm(user.id);

    // Mood range sync
    const moodInput = document.getElementById('log-mood');
    const moodVal = document.getElementById('mood-val');
    moodInput.addEventListener('input', (e) => moodVal.textContent = e.target.value);

    // Load initial data
    await loadDashboardData(user.id);
    await loadGoalProgress(user.id);
});

// ==================== NAVIGATION ====================
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-links li');
    const sections = document.querySelectorAll('.view-section');

    navLinks.forEach(link => {
        link.addEventListener('click', async () => {
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            const targetId = link.getAttribute('data-target');
            sections.forEach(sec => sec.style.display = sec.id === targetId ? 'block' : 'none');

            const user = auth.getUser();
            if (targetId === 'dashboard-view') await loadDashboardData(user.id);
            else if (targetId === 'history-view') await loadHistory(user.id);
            else if (targetId === 'goals-view') await loadGoalProgress(user.id);
        });
    });
}

// ==================== TOAST ====================
function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 3000);
}

// ==================== DASHBOARD DATA ====================
async function loadDashboardData(userId) {
    try {
        const data = await api.analytics.getSummary(userId);

        // Productivity Score Ring
        const score = data.insights.productivity_score || 0;
        document.getElementById('productivity-score').textContent = score;
        const circle = document.getElementById('score-circle');
        const circumference = 2 * Math.PI * 45;
        circle.style.strokeDasharray = circumference;
        circle.style.strokeDashoffset = circumference - (score / 100) * circumference;

        if (score >= 70) circle.style.stroke = '#10b981';
        else if (score >= 40) circle.style.stroke = '#f59e0b';
        else circle.style.stroke = '#ef4444';

        // Stats
        document.getElementById('stat-study').textContent = data.insights.total_study_hours;
        document.getElementById('stat-screen').textContent = data.insights.total_screen_time;
        document.getElementById('stat-mood').textContent = data.insights.average_mood + '/10';
        document.getElementById('stat-productive').textContent = data.insights.productive_days_count;
        document.getElementById('stat-task-completion').textContent = (data.insights.task_completion_percent || 0) + '%';

        // Smart Insights
        const insightsList = document.getElementById('insights-list');
        insightsList.innerHTML = '';
        (data.insights.text_insights || []).forEach(text => {
            const li = document.createElement('li');
            li.textContent = text;
            insightsList.appendChild(li);
        });

        // Weekly Summary
        const ws = data.weekly_summary;
        if (ws) {
            document.getElementById('ws-best').textContent = ws.best_day ? `${ws.best_day.date} (${ws.best_day.study_hours}h)` : '-';
            document.getElementById('ws-worst').textContent = ws.worst_day ? `${ws.worst_day.date} (${ws.worst_day.study_hours}h)` : '-';
            document.getElementById('ws-avg-study').textContent = ws.avg_study_hours + ' hrs';
            document.getElementById('ws-avg-screen').textContent = ws.avg_screen_time + ' hrs';
        }

        // Chart
        renderChart(data.chart_data);
    } catch (error) {
        console.error('Failed to load dashboard:', error);
    }
}

// ==================== CHART ====================
function setChartState(message) {
    const canvas = document.getElementById('trendsChart');
    const wrapper = canvas.closest('.chart-wrapper');
    let stateEl = document.getElementById('chart-empty-state');

    if (!stateEl) {
        stateEl = document.createElement('div');
        stateEl.id = 'chart-empty-state';
        stateEl.className = 'chart-empty-state';
        wrapper.appendChild(stateEl);
    }

    if (message) {
        canvas.style.display = 'none';
        stateEl.textContent = message;
        stateEl.style.display = 'flex';
    } else {
        canvas.style.display = 'block';
        stateEl.style.display = 'none';
    }
}

function renderChart(chartData) {
    const canvas = document.getElementById('trendsChart');
    if (!canvas) return;

    if (currentChart) {
        currentChart.destroy();
        currentChart = null;
    }

    if (typeof Chart === 'undefined') {
        setChartState('Chart library failed to load. Check internet or include Chart.js locally.');
        return;
    }

    if (!Array.isArray(chartData) || chartData.length === 0) {
        setChartState('No trend data yet. Add at least one daily log to see the graph.');
        return;
    }

    setChartState('');

    const ctx = canvas.getContext('2d');

    currentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.map(d => d.date),
            datasets: [
                { label: 'Study Hours', data: chartData.map(d => d.study_hours), borderColor: '#4f46e5', backgroundColor: 'rgba(79,70,229,0.1)', borderWidth: 2, fill: true, tension: 0.4 },
                { label: 'Screen Time', data: chartData.map(d => d.screen_time), borderColor: '#ec4899', backgroundColor: 'rgba(236,72,153,0.1)', borderWidth: 2, fill: true, tension: 0.4 }
            ]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } }, scales: { y: { beginAtZero: true } } }
    });
}

// ==================== LOG FORM ====================
function setupLogForm(userId) {
    document.getElementById('log-date').valueAsDate = new Date();
    document.getElementById('add-log-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const rawTasks = document.getElementById('log-tasks').value || '';
        const tasks = rawTasks
            .split('\n')
            .map(task => task.trim())
            .filter(task => task.length > 0);

        const logData = {
            user_id: userId,
            date: document.getElementById('log-date').value,
            study_hours: parseFloat(document.getElementById('log-study').value),
            screen_time_hours: parseFloat(document.getElementById('log-screen').value),
            mood_score: parseInt(document.getElementById('log-mood').value, 10),
            tasks
        };

        try {
            await api.logs.add(logData);
            showToast('Activity logged successfully!');
            document.getElementById('add-log-form').reset();
            document.getElementById('log-date').valueAsDate = new Date();
            document.getElementById('mood-val').textContent = '5';
            setTimeout(() => document.querySelector('[data-target="dashboard-view"]').click(), 1000);
        } catch (error) {
            alert('Error: ' + error.message);
        }
    });
}

// ==================== HISTORY (with Edit, Task Status & Delete) ====================
async function loadHistory(userId) {
    const tbody = document.getElementById('history-tbody');
    tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;">Loading...</td></tr>';

    try {
        const logs = await api.logs.fetch(userId);
        tbody.innerHTML = '';

        if (logs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;">No logs found.</td></tr>';
            return;
        }

        logs.forEach(log => {
            const score = calcScore(log.study_hours, log.screen_time_hours, log.mood_score);
            const scoreClass = score >= 70 ? 'score-high' : score >= 40 ? 'score-mid' : 'score-low';

            const tasks = Array.isArray(log.tasks) ? log.tasks : [];
            const completedTasks = tasks.filter(task => task.is_completed).length;
            const taskPercent = tasks.length ? Math.round((completedTasks / tasks.length) * 100) : 0;

            const progressClass = tasks.length === 0
                ? 'task-progress-empty'
                : taskPercent === 100
                    ? 'task-progress-complete'
                    : 'task-progress-partial';
            const progressLabel = tasks.length ? `${completedTasks}/${tasks.length} (${taskPercent}%)` : 'No tasks';

            const tasksHtml = tasks.length
                ? `<ul class="task-list">${tasks.map(task => `
                    <li>
                        <label class="task-item ${task.is_completed ? 'done' : ''}">
                            <input type="checkbox" ${task.is_completed ? 'checked' : ''} onchange="toggleTaskStatus(${log.id}, ${task.id}, this.checked)">
                            <span>${escapeHtml(task.task_name)}</span>
                        </label>
                    </li>
                `).join('')}</ul>`
                : '<span class="tasks-empty">No tasks</span>';

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${log.date}</td>
                <td>${log.study_hours}</td>
                <td>${log.screen_time_hours}</td>
                <td>${log.mood_score}/10</td>
                <td class="tasks-cell">${tasksHtml}</td>
                <td><span class="task-progress-badge ${progressClass}">${progressLabel}</span></td>
                <td><span class="badge ${scoreClass}">${score}</span></td>
                <td>
                    <button class="action-btn edit-btn" onclick="openEditModal(${log.id}, ${log.study_hours}, ${log.screen_time_hours}, ${log.mood_score})">Edit</button>
                    <button class="action-btn delete-btn" onclick="deleteLog(${log.id})">Delete</button>
                </td>`;
            tbody.appendChild(tr);
        });
    } catch (error) {
        tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:red;">Failed to load.</td></tr>';
    }
}

// Frontend-side productivity score calc (mirrors backend)
function calcScore(study, screen, mood) {
    const raw = (study / (screen + 1)) * mood;
    return Math.min(Math.round((raw / 15) * 100), 100);
}

window.toggleTaskStatus = async function(logId, taskId, isCompleted) {
    try {
        const user = auth.getUser();
        await api.logs.updateTaskStatus(logId, taskId, user.id, isCompleted);
        await Promise.all([
            loadHistory(user.id),
            loadDashboardData(user.id)
        ]);

        showToast(isCompleted ? 'Task marked as completed' : 'Task marked as pending');
    } catch (error) {
        alert('Error: ' + error.message);
        const user = auth.getUser();
        await loadHistory(user.id);
    }
};

// ==================== EDIT MODAL ====================
window.openEditModal = function(logId, study, screen, mood) {
    document.getElementById('edit-log-id').value = logId;
    document.getElementById('edit-study').value = study;
    document.getElementById('edit-screen').value = screen;
    document.getElementById('edit-mood').value = mood;
    document.getElementById('edit-modal').style.display = 'flex';
};

window.closeEditModal = function() {
    document.getElementById('edit-modal').style.display = 'none';
};

document.getElementById('edit-log-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const logId = document.getElementById('edit-log-id').value;
    const user = auth.getUser();
    const updateData = {
        user_id: user.id,
        study_hours: parseFloat(document.getElementById('edit-study').value),
        screen_time_hours: parseFloat(document.getElementById('edit-screen').value),
        mood_score: parseInt(document.getElementById('edit-mood').value, 10)
    };

    try {
        await api.logs.update(logId, updateData);
        closeEditModal();
        showToast('Log updated successfully!');
        await loadHistory(user.id);
        await loadDashboardData(user.id);
    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// ==================== DELETE ====================
window.deleteLog = async function(logId) {
    if (!confirm('Are you sure you want to delete this log?')) return;

    try {
        const user = auth.getUser();
        await api.logs.delete(logId, user.id);
        showToast('Log deleted');
        await loadHistory(user.id);
        await loadDashboardData(user.id);
    } catch (error) {
        alert('Error: ' + error.message);
    }
};

// ==================== GOAL TRACKING ====================
function setupGoalForm(userId) {
    document.getElementById('goal-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const goal = parseFloat(document.getElementById('goal-input').value);
        try {
            await api.goals.set(userId, goal);
            showToast('Goal set to ' + goal + ' hours/day!');
            await loadGoalProgress(userId);
        } catch (error) {
            alert('Error: ' + error.message);
        }
    });
}

async function loadGoalProgress(userId) {
    try {
        const data = await api.goals.get(userId);
        const fill = document.getElementById('goal-progress-fill');
        const text = document.getElementById('goal-progress-text');
        const msg = document.getElementById('goal-message');
        const goalInput = document.getElementById('goal-input');

        goalInput.value = data.study_goal;
        fill.style.width = data.progress_percent + '%';
        text.textContent = data.progress_percent + '%';

        if (data.progress_percent >= 100) {
            fill.style.background = 'linear-gradient(90deg, #10b981, #059669)';
            msg.textContent = 'Goal achieved! Amazing work today!';
        } else if (data.progress_percent >= 50) {
            fill.style.background = 'linear-gradient(90deg, #f59e0b, #d97706)';
            msg.textContent = `You have studied ${data.today_study_hours}h out of ${data.study_goal}h. Keep going!`;
        } else {
            fill.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
            msg.textContent = `Only ${data.today_study_hours}h logged today. Your goal is ${data.study_goal}h.`;
        }
    } catch (error) {
        console.error('Failed to load goal:', error);
    }
}
