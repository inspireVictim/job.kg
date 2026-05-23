/* ============================================================
   Общий каркас защищённых страниц: проверка токена, шапка, выход.
   ============================================================ */

const ROLE_LABELS = {
  admin: 'Администратор',
  hr: 'HR-менеджер',
  employee: 'Сотрудник',
};

function guardOrRedirect() {
  if (!Auth.isAuthenticated()) {
    window.location.href = '/static/pages/login.html';
    return false;
  }
  return true;
}

function renderHeader(activePage) {
  const user = Auth.getUser();
  if (!user) return;

  const header = document.createElement('header');
  header.className = 'app-header';
  header.innerHTML = `
    <div class="brand">Корпоративный портал <span>«Job.kg»</span></div>
    <nav>
      <a href="/static/pages/index.html"      data-page="index">Главная</a>
      <a href="/static/pages/employees.html"  data-page="employees">Сотрудники</a>
      <a href="/static/pages/documents.html"  data-page="documents">Документы</a>
      <a href="/static/pages/profile.html"    data-page="profile">Профиль</a>
    </nav>
    <div class="user-box">
      <div class="user-info">
        <div class="name">${escapeHtml(user.full_name)}</div>
        <div class="role">${ROLE_LABELS[user.role] || user.role}</div>
      </div>
      <button class="btn-logout" id="logoutBtn">Выход</button>
    </div>
  `;
  document.body.prepend(header);

  const link = header.querySelector(`nav a[data-page="${activePage}"]`);
  if (link) link.classList.add('active');

  document.getElementById('logoutBtn').addEventListener('click', () => {
    Auth.clearSession();
    window.location.href = '/static/pages/login.html';
  });
}

function escapeHtml(value) {
  if (value === null || value === undefined) return '';
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function formatDateTime(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString('ru-RU', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

function formatSize(bytes) {
  if (!bytes && bytes !== 0) return '';
  if (bytes < 1024) return `${bytes} Б`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} КБ`;
  return `${(bytes / 1024 / 1024).toFixed(2)} МБ`;
}

function showAlert(container, message, type = 'error') {
  if (typeof container === 'string') container = document.getElementById(container);
  if (!container) return;
  container.innerHTML = `<div class="alert alert-${type}">${escapeHtml(message)}</div>`;
  if (type === 'success') {
    setTimeout(() => { container.innerHTML = ''; }, 3500);
  }
}

function initials(fullName) {
  if (!fullName) return '?';
  return fullName
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map(part => part.charAt(0).toUpperCase())
    .join('');
}

window.Layout = {
  guardOrRedirect,
  renderHeader,
  escapeHtml,
  formatDateTime,
  formatSize,
  showAlert,
  initials,
  ROLE_LABELS,
};
