/* ============================================================
   Универсальный клиент REST API.
   Все методы возвращают Promise; при HTTP 401 — редирект на /login.
   ============================================================ */

const API_BASE = (window.PORTAL_API_BASE || `${window.location.protocol}//${window.location.host}`) + '/api';
const TOKEN_KEY = 'portal_token';
const USER_KEY = 'portal_user';

const Auth = {
  setSession(token, user) {
    localStorage.setItem(TOKEN_KEY, token);
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  },
  getToken() { return localStorage.getItem(TOKEN_KEY); },
  getUser() {
    const raw = localStorage.getItem(USER_KEY);
    try { return raw ? JSON.parse(raw) : null; }
    catch (_) { return null; }
  },
  clearSession() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  },
  isAuthenticated() { return Boolean(this.getToken()); },
  hasRole(...roles) {
    const u = this.getUser();
    return Boolean(u && roles.includes(u.role));
  },
};

async function apiRequest(path, { method = 'GET', body = null, isForm = false, skipAuthRedirect = false } = {}) {
  const headers = {};
  const token = Auth.getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  let payload = body;
  if (body !== null && !isForm) {
    headers['Content-Type'] = 'application/json';
    payload = JSON.stringify(body);
  }

  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, { method, headers, body: payload });
  } catch (err) {
    throw new Error('Сервер недоступен. Проверьте, запущен ли бэкенд.');
  }

  if (response.status === 401 && !skipAuthRedirect) {
    Auth.clearSession();
    if (!window.location.pathname.endsWith('login.html')) {
      window.location.href = '/static/pages/login.html';
    }
    throw new Error('Требуется повторная авторизация.');
  }

  if (response.status === 204) return null;

  const contentType = response.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    const data = await response.json();
    if (!response.ok) {
      const detail = data && (data.detail || data.message);
      throw new Error(typeof detail === 'string' ? detail : 'Ошибка выполнения запроса');
    }
    return data;
  }

  if (!response.ok) {
    throw new Error(`Ошибка ${response.status}`);
  }
  return response;
}

const Api = {
  login: (username, password) => apiRequest('/auth/login', {
    method: 'POST',
    body: { username, password },
    skipAuthRedirect: true,
  }),
  me: () => apiRequest('/auth/me'),
  register: (payload) => apiRequest('/auth/register', { method: 'POST', body: payload }),

  listUsers: (params = {}) => {
    const qs = new URLSearchParams();
    if (params.department) qs.set('department', params.department);
    if (params.search) qs.set('search', params.search);
    const q = qs.toString();
    return apiRequest(`/users/${q ? '?' + q : ''}`);
  },
  listDepartments: () => apiRequest('/users/departments'),
  updateMe: (payload) => apiRequest('/users/me', { method: 'PUT', body: payload }),
  changePassword: (payload) => apiRequest('/users/me/password', { method: 'POST', body: payload }),

  listNews: () => apiRequest('/news/'),
  createNews: (payload) => apiRequest('/news/', { method: 'POST', body: payload }),
  deleteNews: (id) => apiRequest(`/news/${id}`, { method: 'DELETE' }),

  listDocuments: () => apiRequest('/documents/'),
  uploadDocument: (formData) => apiRequest('/documents/', { method: 'POST', body: formData, isForm: true }),
  deleteDocument: (id) => apiRequest(`/documents/${id}`, { method: 'DELETE' }),
  downloadDocumentUrl: (id) => `${API_BASE}/documents/${id}/download`,
};

window.Api = Api;
window.Auth = Auth;
