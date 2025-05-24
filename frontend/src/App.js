import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./components/Register";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import TaskDetail from "./components/TaskDetails";
import ProjectDetail from "./components/ProjectDetails";
import LandingPage from "./components/LandingPage";
function App() {
  // Example: manage user and token in state
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  useEffect(() => {
    // Example: load user/token from localStorage or your auth logic
    const storedUser = JSON.parse(localStorage.getItem("user"));
    const storedToken = localStorage.getItem("token");
    if (storedUser && storedToken) {
      setUser(storedUser);
      setToken(storedToken);
    }
  }, []);

  return (
    <Router>
      <Routes>
        <Route path ="/"element={<LandingPage />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard user={user} token={token} />} />
        <Route path="/project/:projectId" element={<ProjectDetail user={user} token={token} />} />
        {/* Pass user and token props to TaskDetail */}
        <Route path="/project/:projectId/tasks/:taskId"
          element={<TaskDetail user={user} token={token} />} />
        

      </Routes>
    </Router>
  );
}

export default App;
