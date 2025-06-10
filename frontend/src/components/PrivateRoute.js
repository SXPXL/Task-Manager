import { Navigate } from "react-router-dom";
import  { useAuth } from "../context/AuthContext";

// Function to redirect user that are not logged in when they directly enters a private url
const PrivateRoute = ({ children }) => {
  const { user } = useAuth();
  return user ? children :<Navigate to="/login"/>;
};

export default PrivateRoute;