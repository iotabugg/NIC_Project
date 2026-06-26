const Auth = {
  getToken() {
    return localStorage.getItem('access_token');
  },
  getRefreshToken() {
    return localStorage.getItem('refresh_token');
  },
  setTokens(access, refresh) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  },
  clear() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
  isLoggedIn() {
    return !!localStorage.getItem('access_token');
  },
  // Decode JWT payload (no verification — just for reading role/username)
  getPayload() {
    const token = this.getToken();
    if (!token) return null;
    try {
      return JSON.parse(atob(token.split('.')[1]));
    } catch {
      return null;
    }
  },
  redirectIfNotLoggedIn() {
    if (!this.isLoggedIn()) window.location.href = '/login/';
  },
};

function logout() {
  Auth.clear();
  window.location.href = '/login/';
}

// Show username + role in navbar on every page
document.addEventListener('DOMContentLoaded', () => {
  const payload = Auth.getPayload();
  if (!payload) return;

  const usernameEl = document.getElementById('navbar-username');
  const roleEl = document.getElementById('navbar-role');
  if (usernameEl) usernameEl.textContent = payload.username || '';
  if (roleEl) roleEl.textContent = payload.role || '';

  // Set profile link to current user's edit page
  const profileLink = document.getElementById('profile-link');
  if (profileLink && payload.user_id) {
    profileLink.href = '#';
    profileLink.dataset.userId = payload.user_id;
    // profileLink click opens modal and fetches profile
    profileLink.addEventListener('click', async function (e) {
      e.preventDefault();
      const userId = this.dataset.userId;
      if (!userId) return;

      // modal elements
      const modal = document.getElementById('profile-modal');
      const closeBtn = document.getElementById('profile-modal-close');
      const editLink = document.getElementById('profile-edit-link');

      // clear previous
      document.getElementById('pf-username').textContent = '';
      document.getElementById('pf-fullname').textContent = '';
      document.getElementById('pf-email').textContent = '';
      document.getElementById('pf-mobile').textContent = '';
      document.getElementById('pf-role').textContent = '';
      document.getElementById('pf-state').textContent = '';
      document.getElementById('pf-district').textContent = '';
      document.getElementById('pf-emp-id').textContent = '';
      document.getElementById('pf-emp-office').textContent = '';
      document.getElementById('pf-emp-dept').textContent = '';
      document.getElementById('pf-emp-designation').textContent = '';
      document.getElementById('pf-emp-type').textContent = '';
      document.getElementById('pf-emp-status').textContent = '';

      // show loading
      modal.classList.remove('hidden');

      try {
        const res = await fetch(`/api/users/edit/${userId}/`, {
          headers: { 'Authorization': `Bearer ${Auth.getToken()}` },
        });
        const data = await res.json();
        if (!res.ok) {
          alert(data.error || data.detail || 'Unable to load profile');
          modal.classList.add('hidden');
          return;
        }

        // data is UserSerializer output
        document.getElementById('pf-username').textContent = data.username || '';
        document.getElementById('pf-fullname').textContent = (data.first_name || '') + (data.last_name ? ' ' + data.last_name : '');
        document.getElementById('pf-email').textContent = data.email || '';
        document.getElementById('pf-mobile').textContent = data.mobile || '';
        document.getElementById('pf-role').textContent = data.role || '';
        document.getElementById('pf-state').textContent = data.state || '';
        document.getElementById('pf-district').textContent = data.district || '';

        // employee section
        if (data.employee) {
          document.getElementById('profile-employee-section').classList.remove('hidden');
          document.getElementById('pf-emp-id').textContent = data.employee.employee_id || '';
          document.getElementById('pf-emp-office').textContent = data.employee.office || '';
          document.getElementById('pf-emp-dept').textContent = data.employee.department || '';
          document.getElementById('pf-emp-designation').textContent = data.employee.designation || '';
          document.getElementById('pf-emp-type').textContent = data.employee.employment_type || '';
          document.getElementById('pf-emp-status').textContent = data.employee.employment_status || '';
          // set edit link to employee detail edit (user edit page still available)
          if (editLink) editLink.href = `/users/edit/${userId}/`;
        } else {
          document.getElementById('profile-employee-section').classList.add('hidden');
          if (editLink) editLink.href = `/users/edit/${userId}/`;
        }

        // close handler
        if (closeBtn) closeBtn.onclick = () => modal.classList.add('hidden');

      } catch (err) {
        alert('An error occurred while loading profile.');
        modal.classList.add('hidden');
      }
    });
  }

  // Show STATE_ADMIN-only sidebar links
  const role = payload.role || '';
  if (role === 'STATE_ADMIN') {
    document.querySelectorAll('.state-admin-only').forEach(el => {
      el.classList.remove('hidden');
    });
  }
});