/**
 * PrivateRoute Component
 * ----------------------
 * Protects routes by redirecting unauthenticated users to the login page.
 *
 * Props:
 * - children: The protected component(s) to render if authenticated
 *
 * Usage:
 * Wrap protected routes in your router with <PrivateRoute>...</PrivateRoute>
 */

import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import GreenSpinner from "./Spinner";

// Redirect user to /login if not logged in or token missing
const PrivateRoute = ({ children }) => {
  /**
   * Checks authentication state and renders children or redirects to login.
   * @param {object} children - The protected component(s)
   */

  const { user, token, loading } = useAuth();

  if (loading) return <GreenSpinner />;

  // If no user or no token, redirect to login
  if (!user || !token) {
    return <Navigate to="/login" />;
  }

  // Otherwise show children components (protected page)
  return children;
};

export default PrivateRoute;
