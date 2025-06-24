import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import GreenSpinner from "./Spinner";

// Redirect user to /login if not logged in or token missing
const PrivateRoute = ({ children }) => {
  const { user, token, loading } = useAuth();

  if (loading) return <GreenSpinner/>
  
  // If no user or no token, redirect to login
  if (!user || !token) {
    return <Navigate to="/login" />;
  }

  // Otherwise show children components (protected page)
  return children;
};

export default PrivateRoute;
