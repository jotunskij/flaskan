function createRequest(method, access_token, payload = null) {
    req = {
        method: method,
        headers: {
            'Authorization': `Bearer ${access_token}`,
            'Content-Type': 'application/json'
        }
    }
    if (payload != null) req['data'] = JSON.stringify(payload);
    return req;
}

async function apiGET(url) {
    access_token = getAccessToken();
    access_token = await refreshTokenIfExpired(access_token);
    const final_url = `${document.location.protocol}//${document.location.host}${url}`;
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
    const token = Cookies.get('access_token');
    console.log(`Current cookies: ${JSON.stringify(Cookies.get())}`)
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
    const refresh_token = Cookies.get('refresh_token');
    const refresh_url = createUrl('/api/token/refresh');
    const req = createRequest('POST', refresh_token);
    response = await fetch(refresh_url, req);
    if (response.ok) {
        json_body = await response.json();
        Cookies.set('access_token', json_body['access_token']);
        return json_body['access_token'];
    }
    return null;
}

function createUrl(path) {
    return `${window.location.protocol}//${window.location.host}${path}`
}
