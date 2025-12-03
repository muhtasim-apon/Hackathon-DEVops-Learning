// ==================== CONFIGURATION ====================
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// ==================== UTILITY FUNCTIONS ====================
function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.add('show');
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.remove('show');
}

function showToast(message, isError = false) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');

    if (toast && toastMessage) {
        toastMessage.textContent = message;
        toast.classList.toggle('error', isError);
        toast.classList.add('show');

        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;

    return date.toLocaleDateString();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ==================== API FUNCTIONS ====================
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// ==================== HOME PAGE FUNCTIONS ====================
async function checkAPIHealth() {
    try {
        const startTime = performance.now();
        const data = await apiRequest('/health');
        const endTime = performance.now();
        const responseTime = Math.round(endTime - startTime);

        const statusBadge = document.getElementById('statusBadge');
        const dbStatus = document.getElementById('dbStatus');
        const responseTimeEl = document.getElementById('responseTime');
        const lastChecked = document.getElementById('lastChecked');

        if (statusBadge) {
            statusBadge.innerHTML = '<i class="fas fa-circle"></i> Online';
            statusBadge.classList.remove('error');
        }

        if (dbStatus) {
            dbStatus.textContent = data.database === 'connected' ? 'Connected ✅' : 'Disconnected ❌';
        }

        if (responseTimeEl) {
            responseTimeEl.textContent = `${responseTime}ms`;
        }

        if (lastChecked) {
            lastChecked.textContent = new Date().toLocaleTimeString();
        }

        return data;
    } catch (error) {
        const statusBadge = document.getElementById('statusBadge');
        if (statusBadge) {
            statusBadge.innerHTML = '<i class="fas fa-circle"></i> Offline';
            statusBadge.classList.add('error');
        }
        console.error('Health check failed:', error);
    }
}

async function loadHomePageStats() {
    try {
        const stats = await apiRequest('/stats');

        const totalRequests = document.getElementById('totalRequests');
        const totalTodos = document.getElementById('totalTodos');

        if (totalRequests) {
            animateCounter(totalRequests, 0, 1247, 1000);
        }

        if (totalTodos) {
            animateCounter(totalTodos, 0, stats.total || 0, 1000);
        }
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

function animateCounter(element, start, end, duration) {
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        const easeOutQuad = progress * (2 - progress);
        const current = Math.floor(start + (end - start) * easeOutQuad);

        element.textContent = current.toLocaleString();

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

// ==================== TODO PAGE FUNCTIONS ====================
let allTodos = [];
let currentFilter = 'all';

async function loadTodos() {
    try {
        showLoading();
        const data = await apiRequest('/todos');
        allTodos = data.todos || [];
        renderTodos();
        hideLoading();
    } catch (error) {
        showToast('Failed to load todos', true);
        hideLoading();
    }
}

async function loadStats() {
    try {
        const stats = await apiRequest('/stats');

        document.getElementById('totalCount').textContent = stats.total || 0;
        document.getElementById('completedCount').textContent = stats.completed || 0;
        document.getElementById('pendingCount').textContent = stats.pending || 0;
        document.getElementById('highPriorityCount').textContent = stats.by_priority?.high || 0;
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

function renderTodos() {
    const todoList = document.getElementById('todoList');
    if (!todoList) return;

    let filteredTodos = allTodos;

    // Apply filters
    switch (currentFilter) {
        case 'completed':
            filteredTodos = allTodos.filter(t => t.completed);
            break;
        case 'pending':
            filteredTodos = allTodos.filter(t => !t.completed);
            break;
        case 'high':
            filteredTodos = allTodos.filter(t => t.priority === 'high');
            break;
    }

    // Search filter
    const searchValue = document.getElementById('searchInput')?.value.toLowerCase();
    if (searchValue) {
        filteredTodos = filteredTodos.filter(t =>
            t.title.toLowerCase().includes(searchValue) ||
            (t.description && t.description.toLowerCase().includes(searchValue))
        );
    }

    if (filteredTodos.length === 0) {
        todoList.innerHTML = `
            <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
                <i class="fas fa-inbox" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                <p>No todos found</p>
            </div>
        `;
        return;
    }

    todoList.innerHTML = filteredTodos.map(todo => `
        <div class="todo-item ${todo.completed ? 'completed' : ''}" data-id="${todo._id}">
            <div class="todo-checkbox ${todo.completed ? 'checked' : ''}" onclick="toggleTodo('${todo._id}')"></div>
            <div class="todo-content">
                <div class="todo-title">${escapeHtml(todo.title)}</div>
                ${todo.description ?  `<div class="todo-description">${escapeHtml(todo.description)}</div>` : ''}
            </div>
            <div class="todo-meta">
                <span class="priority-badge ${todo.priority}">${todo.priority}</span>
            </div>
            <div class="todo-actions">
                <button class="action-btn delete" onclick="deleteTodo('${todo._id}')" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

// ==================== ADD TODO (Direct MongoDB Insert) ====================
async function addTodo(event) {
    event.preventDefault();

    const title = document.getElementById('todoTitle').value;
    const description = document.getElementById('todoDescription').value;
    const priority = document.getElementById('todoPriority').value;

    if (!title.trim()) {
        showToast('Please enter a title', true);
        return;
    }

    try {
        showLoading();

        // Create todo object
        const newTodo = {
            title: title.trim(),
            description: description.trim() || null,
            priority: priority,
            completed: false
        };

        // Send to API (which saves to MongoDB)
        const response = await apiRequest('/todos', {
            method: 'POST',
            body: JSON.stringify(newTodo)
        });

        console.log('✅ Todo saved to MongoDB:', response);

        showToast('✅ Todo added to MongoDB successfully!');

        // Clear form
        document.getElementById('addTodoForm').reset();

        // Reload data
        await loadTodos();
        await loadStats();

        hideLoading();
    } catch (error) {
        console.error('❌ Failed to add todo:', error);
        showToast('Failed to add todo to database', true);
        hideLoading();
    }
}

// ==================== TOGGLE TODO (Update MongoDB) ====================
async function toggleTodo(todoId) {
    try {
        await apiRequest(`/todos/${todoId}/toggle`, {
            method: 'PATCH'
        });

        // Update local state
        const todo = allTodos.find(t => t._id === todoId);
        if (todo) {
            todo.completed = !todo.completed;
        }

        renderTodos();
        await loadStats();
        showToast('✅ Todo updated in MongoDB!');
    } catch (error) {
        console.error('❌ Failed to update todo:', error);
        showToast('Failed to update todo', true);
    }
}

// ==================== DELETE TODO (Remove from MongoDB) ====================
async function deleteTodo(todoId) {
    if (!confirm('Are you sure you want to delete this todo?')) {
        return;
    }

    try {
        showLoading();

        await apiRequest(`/todos/${todoId}`, {
            method: 'DELETE'
        });

        console.log('✅ Todo deleted from MongoDB');

        showToast('✅ Todo deleted from MongoDB!');

        // Reload data
        await loadTodos();
        await loadStats();

        hideLoading();
    } catch (error) {
        console.error('❌ Failed to delete todo:', error);
        showToast('Failed to delete todo', true);
        hideLoading();
    }
}

// ==================== FILTER TODOS ====================
function setFilter(filter) {
    currentFilter = filter;

    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    renderTodos();
}

// ==================== SEARCH TODOS ====================
function setupSearch() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            renderTodos();
        });
    }
}

// ==================== NAVBAR SCROLL EFFECT ====================
function setupNavbar() {
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// ==================== MOBILE MENU ====================
function setupMobileMenu() {
    const toggle = document.getElementById('mobileMenuToggle');
    const navLinks = document.querySelector('.nav-links');

    if (toggle && navLinks) {
        toggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }
}

// ==================== KEYBOARD SHORTCUTS ====================
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('searchInput');
            if (searchInput) searchInput.focus();
        }

        // Escape to clear search
        if (e.key === 'Escape') {
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                searchInput.value = '';
                renderTodos();
            }
        }
    });
}

// ==================== QUICK ADD WITH ENTER ====================
function setupQuickAdd() {
    const titleInput = document.getElementById('todoTitle');
    if (titleInput) {
        titleInput.addEventListener('keydown', (e) => {
            // Shift + Enter to quick add with default priority
            if (e.shiftKey && e.key === 'Enter') {
                e.preventDefault();
                const form = document.getElementById('addTodoForm');
                if (form) {
                    form.dispatchEvent(new Event('submit'));
                }
            }
        });
    }
}

// ==================== INITIALIZE ON PAGE LOAD ====================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 FastAPI Frontend Initialized');

    // Setup UI components
    setupNavbar();
    setupMobileMenu();
    setupKeyboardShortcuts();
    setupSearch();
    setupQuickAdd();

    // Detect current page
    const currentPath = window.location.pathname;

    if (currentPath === '/' || currentPath === '/index.html') {
        // Home page
        console.log('📄 Loading home page...');
        await checkAPIHealth();
        await loadHomePageStats();

        // Refresh health check every 30 seconds
        setInterval(checkAPIHealth, 30000);
    }
    else if (currentPath === '/todos' || currentPath === '/todos.html') {
        // Todos page
        console.log('📋 Loading todos page...');

        // Load initial data
        await loadTodos();
        await loadStats();

        // Setup form handler
        const form = document.getElementById('addTodoForm');
        if (form) {
            form.addEventListener('submit', addTodo);
        }

        // Setup filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                currentFilter = btn.dataset.filter;
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderTodos();
            });
        });

        // Auto-refresh every 60 seconds
        setInterval(async () => {
            await loadTodos();
            await loadStats();
        }, 60000);
    }

    console.log('✅ Initialization complete!');
});

// ==================== CONSOLE ART ====================
console.log(`
%c
╔═══════════════════════════════════════╗
║                                       ║
║      FastAPI + MongoDB Backend        ║
║                                       ║
║   🚀 Built for Hackathons             ║
║   ⚡ Lightning Fast                   ║
║   🎨 Modern UI                        ║
║                                       ║
╚═══════════════════════════════════════╝
`, 'color: #667eea; font-weight: bold;');

console.log('%c💡 Tip: Press Ctrl/Cmd + K to search todos', 'color: #10b981;');
console.log('%c💡 Tip: Press Shift + Enter in title field to quick add', 'color: #10b981;');

// ==================== EXPORT FOR TESTING ====================
window.API = {
    addTodo,
    deleteTodo,
    toggleTodo,
    loadTodos,
    loadStats,
    apiRequest
};