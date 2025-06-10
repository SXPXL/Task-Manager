import React, { useState, useEffect } from "react";
import PrivateRoute from "./components/PrivateRoute";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./components/Register";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import TaskDetail from "./components/TaskDetails";
import ProjectDetail from "./components/ProjectDetails";
import LandingPage from "./components/LandingPage";
import Stats from "./components/Stats"
import TaskListPage from "./components/TaskList";

/* App Component
 * -------------------
 * Main application component that sets up routing and state management.
 * It initializes user and token state from localStorage.
 */

function App() {

  // State to hold user and token information
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  // On component mount, check localStorage for user and token
  useEffect(() => {

    const storedUser = JSON.parse(localStorage.getItem("user"));
    const storedToken = localStorage.getItem("token");
    if (storedUser && storedToken) {
      setUser(storedUser);
      setToken(storedToken);
    }
  }, []);

  return (
    
    // Router wraps the whole apps to enable routing
    <Router>
      <Routes>

        {/* Define routes for different components */}
        <Route path="/"element={<LandingPage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />

        {/* Protected routes that require user and token */}
         <Route path="/dashboard" element={<PrivateRoute><Dashboard user={user} token={token} /></PrivateRoute>} />
        <Route path="/project/:projectId" element={<PrivateRoute><ProjectDetail user={user} token={token} /></PrivateRoute>} />
        <Route path="/project/:projectId/tasks/:taskId"
        element={<PrivateRoute><TaskDetail user={user} token={token} /></PrivateRoute>} />
        <Route path="/summary" element={<PrivateRoute><Stats user={user} token={token} /></PrivateRoute>}/>

        {/* Dynamic route for task lists based on status */}
        <Route path="/tasks/:status" element={<PrivateRoute><TaskListPage /></PrivateRoute>} />
      </Routes>
    </Router>
  );
}

export default App;
