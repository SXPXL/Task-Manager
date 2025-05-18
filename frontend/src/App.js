import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./components/Register";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import ProjectDetail from "./components/ProjectDetails";

function App() {
  return(
    <Router>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path ="/dashboard" element={<Dashboard />} />
         <Route path="/project/:projectId" element={<ProjectDetail />} />

      </Routes>
    </Router>
  );
}

export default App;

