/* This function decodes a JWT token and returns the payload as a JSON object.
 * It handles Base64 URL encoding and decoding, and returns null if the token is invalid.
 */ 
export function parseJWT(token) {
  try {
    // JWT format: header.payload.signature
    // Split token and get payload at index 1
    const Base64Url = token.split('.')[1];

    // Replace URL-safe characters with standard Base64 characters
    const Base64 = Base64Url.replace(/-/g, '+').replace(/_/g, '/');
    
    // Decode Base64 string to JSON string
    const jsonPayload = decodeURIComponent(
      atob(Base64)
      .split('')
      .map(c => '%' + ('00'+c.charCodeAt(0).toString(16)).slice(-2))
      .join('')
    );

    // Parse the JSON string to an object
    return JSON.parse(jsonPayload);
  }
  catch (e) {
    return null;
  }
}