function createRequest(method, payload = null) {
    req = {
        method: method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
        },
        credentials: 'include'
    }
    if (payload != null) req['body'] = JSON.stringify(payload);
    return req;
}

async function logout() {
    window.location = createUrl('/logout');
}

async function login() {
    const final_url = createUrl('/api/login');
    var next_url = document.getElementById('next_url');
    const payload = {
        'username': document.getElementById('username').value,
        'password': document.getElementById('password').value
    }
    const req = createRequest('POST', payload);
    response = await fetch(final_url, req);
    if (response.ok) {
        let redirect_url = createUrl('/');
        if (next_url && next_url.value) redirect_url = createUrl(next_url.value);
        window.location = redirect_url;
    } else {
        window.location = createUrl('/login?error=Felaktig%20inloggning');
    }
}

async function apiGET(url) {
    const final_url = createUrl(url);
    req = createRequest('GET')
    return await apiCall(final_url, req);
}

async function apiPOST(url, payload = {}) {
    const final_url = createUrl(url);
    req = createRequest('POST', payload)
    return await apiCall(final_url, req);
}

async function apiCall(url, req) {
    response = await fetch(url, req);
    if (response.status == 401) {
        // Try to refresh token
        const ref_url = createUrl('/api/token/refresh')
        ref_req = createRequest('POST')
        ref_resp = await fetch(ref_url, ref_req)
        if (ref_resp.ok) {
            return await apiCall(url, req);
        }
        window.location = createUrl('/login?error=Din%20inloggning%20har%20löpt%20ut')
    }
    json_resp = await response.json()
    return json_resp;
}

function createUrl(path) {
    return `${window.location.protocol}//${window.location.host}${path}`
}
