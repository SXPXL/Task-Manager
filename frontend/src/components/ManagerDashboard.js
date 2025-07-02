/**
 * ManagerDashboard Component
 * -------------------------
 * Displays a summary dashboard for managers, including project and task statistics.
 *
 * State:
 * - summary: Holds total projects, total tasks, in-progress tasks, and completed tasks
 *
 * Effects:
 * - Fetches all projects and their tasks on mount to compute summary statistics
 *
 * Functions:
 * - fetchData: Loads project and task data, computes summary, and updates state
 *
 * Usage:
 * Used by managers to get an overview of project/task status.
 */

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './styles/ManagerDashboard.css';
import BASE_URL from '../config';

const ManagerDashboard = () => {
  // State to hold summary data for projects and tasks
  const [summary, setSummary] = useState({
    totalProjects: 0,
    totalTasks: 0,
    inProgressTasks: 0,
    completedTasks: 0,
  });

  // To fetch projects and tasks data 
  useEffect(() => {
    /**
     * Fetches all projects and their tasks from the backend, computes summary statistics, and updates state.
     */
    const fetchData = async () => {
      try {

        // Fetching all projects from data
        const projectRes = await axios.get(`${BASE_URL}/project/get-projects`);
        const projects = projectRes.data;
        let totalTasks = 0;
        let inProgressTasks = 0;
        let completedTasks = 0;

        // Looping through all projects to fetch tasks 
        for (const project of projects) {
          const taskRes = await axios.get(`${BASE_URL}/project/${project.id}/tasks`);
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

        // Update summary state 
        setSummary({
          totalProjects: projects.length,
          totalTasks,
          inProgressTasks,
          completedTasks,
        });
      } catch (error) {
        alert('Error fetching project/task data');
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
