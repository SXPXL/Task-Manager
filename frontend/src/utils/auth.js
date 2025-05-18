export function parseJWT(token) {
  try {
    const Base64Url = token.split('.')[1];
    const Base64 = Base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(Base64)
      .split('')
      .map(c => '%' + ('00'+c.charCodeAt(0).toString(16)).slice(-2))
      .join('')
    );
    return JSON.parse(jsonPayload);
  }
  catch (e) {
    return null;
  }
}