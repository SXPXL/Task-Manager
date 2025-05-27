import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './styles/ManagerDashboard.css';

const ManagerDashboard = () => {
  const [summary, setSummary] = useState({
    totalProjects: 0,
    totalTasks: 0,
    inProgressTasks: 0,
    completedTasks: 0,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const projectRes = await axios.get('http://localhost:8000/project/get-projects');
        const projects = projectRes.data;
        let totalTasks = 0;
        let inProgressTasks = 0;
        let completedTasks = 0;

        for (const project of projects) {
          const taskRes = await axios.get(`http://localhost:8000/project/${project.id}/tasks`);
          const tasks = taskRes.data;
          totalTasks += tasks.length;

          for (const task of tasks) {
            if (task.status === 'completed') {
              completedTasks++;
            } else {
              inProgressTasks++;
            }
          }
        }

        setSummary({
          totalProjects: projects.length,
          totalTasks,
          inProgressTasks,
          completedTasks,
        });
      } catch (error) {
        console.error('Error fetching project/task data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="manager-dashboard">
      <h2>Manager Dashboard</h2>
      <div className="summary-cards">
        <div className="summary-card blue">
          <h4>Total Projects</h4>
          <p>{summary.totalProjects}</p>
        </div>
        <div className="summary-card yellow">
          <h4>Tasks In Progress</h4>
          <p>{summary.inProgressTasks}</p>
        </div>
        <div className="summary-card green">
          <h4>Completed Tasks</h4>
          <p>{summary.completedTasks}</p>
        </div>
      </div>
    </div>
  );
};

export default ManagerDashboard;
