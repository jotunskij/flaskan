function createRequest(method, access_token, payload = null) {
    req = {
        method: method,
        headers: {
            'Authorization': `Bearer ${access_token}`,
            'Content-Type': 'application/json'
        }
    }
    if (payload != null) req['body'] = JSON.stringify(payload);
    return req;
}

async function logout() {
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('refresh_token');
    window.location = createUrl('/');
}

async function login() {
    const final_url = createUrl('/api/login');
    var next_url = document.getElementById('next_url');
    const payload = {
        'username': document.getElementById('username').value,
        'password': document.getElementById('password').value
    }
    const req = createRequest('POST', 'not_required', payload);
    response = await fetch(final_url, req);
    if (response.ok) {
        json_body = await response.json();
        sessionStorage.setItem('access_token', json_body['access_token']);
        sessionStorage.setItem('refresh_token', json_body['refresh_token']);
        let redirect_url = createUrl('/');
        if (next_url && next_url.value) redirect_url = createUrl(next_url.value);
        window.location = redirect_url;
    } else {
        window.location = createUrl('/login?error=Felaktig%20inloggning');
    }
}

async function apiGET(url) {
    access_token = getAccessToken();
    access_token = await refreshTokenIfExpired(access_token);
    const final_url = createUrl(url);
    req = createRequest('GET', access_token)
    return await apiCall(final_url, req);
}

async function apiPOST(url, payload = {}) {
    access_token = getAccessToken();
    access_token = await refreshTokenIfExpired(access_token);
    const final_url = `${document.location.protocol}//${document.location.host}${url}`;
    req = createRequest('POST', access_token, payload)
    return await apiCall(final_url, req);
}

async function apiCall(url, req) {
    response = await fetch(url, req);
    return await response.json();
}

function getAccessToken() {
    const token = sessionStorage.getItem('access_token');
    if (!token) {
        window.location = createUrl('/login');
    }
    return token;
}

async function refreshTokenIfExpired(access_token) {
    const now = new Date();
    const secondsSinceEpoch = Math.round(now.getTime() / 1000);
    decoded_token = jwt_decode(access_token);
    if (decoded_token['exp'] < secondsSinceEpoch) {
        access_token = await refreshToken();
        if (!access_token) {
            window.location = createUrl('/login');
        }
    }
    return access_token;
}

async function refreshToken() {
    const refresh_token = sessionStorage.getItem('refresh_token');
    const refresh_url = createUrl('/api/token/refresh');
    const req = createRequest('POST', refresh_token);
    response = await fetch(refresh_url, req);
    if (response.ok) {
        json_body = await response.json();
        sessionStorage.setItem('access_token', json_body['access_token']);
        return json_body['access_token'];
    }
    return null;
}

function createUrl(path) {
    return `${window.location.protocol}//${window.location.host}${path}`
}
