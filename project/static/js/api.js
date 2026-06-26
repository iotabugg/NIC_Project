const API = {
  async request(url, options = {}) {
    const token = Auth.getToken();
    const res = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...(options.headers || {}),
      },
    });

    if (res.status === 401) {
      Auth.clear();
      window.location.href = '/login/';
      return;
    }

    return res.json();
  },
  get(url)          { return this.request(url); },
  post(url, data)   { return this.request(url, { method: 'POST',   body: JSON.stringify(data) }); },
  patch(url, data)  { return this.request(url, { method: 'PATCH',  body: JSON.stringify(data) }); },
  put(url, data)    { return this.request(url, { method: 'PUT',    body: JSON.stringify(data) }); },
  delete(url)       { return this.request(url, { method: 'DELETE' }); },
};