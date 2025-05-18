import React, { createContext, useContext, useEffect, useState } from 'react';
import { parseJWT } from '../utils/auth';



const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user,setUser]=useState(null);
  const [token,setToken] = useState(null);
  const [loading, setLoading] = useState(true);

 

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

  const login = (newToken) => {
    const decoded = parseJWT(newToken);
    if(decoded) {
      localStorage.setItem('token',newToken);
      setToken(newToken);
      setUser(decoded);
     
      
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setToken(null);
    
    
  };

  const value = {
    user,
    token,
    login,
    logout,
    isAuthenticated: !!user,
    loading,
  };
  return <AuthContext.Provider value ={value}>{children}</AuthContext.Provider>;
};