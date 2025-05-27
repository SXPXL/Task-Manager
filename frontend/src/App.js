import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./components/Register";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import TaskDetail from "./components/TaskDetails";
import ProjectDetail from "./components/ProjectDetails";
import LandingPage from "./components/LandingPage";
import Stats from "./components/Stats"
import TaskListPage from "./components/TaskList";

function App() {

  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  useEffect(() => {

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
        <Route path="/project/:projectId/tasks/:taskId"
        element={<TaskDetail user={user} token={token} />} />
        <Route path="/summary" element={<Stats user={user} token={token} />}/>
        <Route path="/tasks/:status" element={<TaskListPage />} />
        

      </Routes>
      
    </Router>
  );
}

export default App;
