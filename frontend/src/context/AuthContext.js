import React, { createContext, useContext, useEffect, useState } from 'react';
import { parseJWT } from '../utils/auth';

/* AuthContext.js
 * 
 * This context provides authentication state and methods for the application.
 * It manages user login, logout, and token storage.
 */
const AuthContext = createContext();

// custom hook to use the AuthContext
export const useAuth = () => useContext(AuthContext);

// AuthProvider component to wrap around the application
export const AuthProvider = ({ children }) => {
  const [user,setUser]=useState(null); // Holds user information decoded from the JWT 
  const [token,setToken] = useState(null); // Stores the raw JWT
  const [loading, setLoading] = useState(true); // Tracks if authentication status is beign checked

  //On initialization, check localStorage for a token
  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if(storedToken) {
      const decoded = parseJWT(storedToken);
      if(decoded) {
        setUser(decoded);
        setToken(storedToken);
      }
    }
    setLoading(false);
  },[])

  // Function to log in and store the user and token
  const login = (newToken) => {
    const decoded = parseJWT(newToken);
    if(decoded) {
      localStorage.setItem('token',newToken);
      setToken(newToken);
      setUser(decoded);
     
      
    }
  };

  // Function to log out the user and clear user data
  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setToken(null);
    
    
  };

  // The value provided to all components that consume this context
  const value = {
    user,
    token,
    login,
    logout,
    isAuthenticated: !!user,
    loading,
  };
  
  // Provide the context to all children components
  return <AuthContext.Provider value ={value}>{children}</AuthContext.Provider>;
};