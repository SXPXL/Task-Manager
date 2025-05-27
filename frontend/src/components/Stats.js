import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import GreenSpinner from "./Spinner";
import SummaryCard from "./SummaryCard";
import TaskChart from "./TaskChart";
import { useAuth } from "../context/AuthContext";
import ManagerDashboard from "./ManagerDashboard";
import './styles/Stats.css';
import AdminDashboard from "./AdminDashboard";

/**
 * Stats Component
 * ---------------
 * Displays the user-specific dashboard summary of tasks.
 * Fetches task counts and renders summary cards and a task chart.
 * Allows navigation to filtered task lists by clicking on summary cards.
 * Shows additional dashboards for users with 'manager' and 'admin' roles.
 */
export default function Stats() {
  const [summary, setSummary] = useState(null); // Holds the user's task summary data
  const [error, setError] = useState(""); // Stores any error message during API calls
  const { token, user } = useAuth(); // Retrieves auth token and current user info from context
  const navigate = useNavigate(); 
  
  /**
   * Handles clicks on the summary cards.
   * Converts the label text into a URL-friendly status string and navigates to that tasks page.
   * Example: "Due Soon" → "due_soon"
   */
  const handleClick = (label) => {
   
    const status = label.toLowerCase().replace(/\s/g, "_"); // "Due Soon" → "due_soon"
    navigate(`/tasks/${status}`);
  };
  
  // Fetch user task summary data when token changes
  useEffect(() => {
    if (!token) return; //Do nothing if token is not available

    const fetchSummary = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/summary/user-summary`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setSummary(response.data);
      } catch (err) {
        console.error("Failed to fetch summary:", err);
        setError("Unable to load dashboard data.");
      }
    };

    fetchSummary();
  }, [token]);
  if(!user) return <GreenSpinner/>;

  return (
    <div className="summary-container">
      <button className="back" onClick={() => navigate(-1)}>← Back</button>
      <h2 className="user-summary">User Stats</h2>
      {error && <p className="error-msg">{error}</p>}

      {/* Display summary cards and charts if data us available */}
      {summary ? (
        <div className="dashboard-body">
          <div className="card-labels">
            {/* Summary cards for different categories */}
            <SummaryCard label="Assigned Tasks" value={summary.assigned_tasks} onClick={handleClick} />
            <SummaryCard label="Completed Tasks" value={summary.completed_tasks} onClick={handleClick} />
            <SummaryCard label="Overdue Tasks" value={summary.overdue_tasks} onClick={handleClick} />
            <SummaryCard label="Due Soon" value={summary.soon_due_tasks} onClick={handleClick} />
          </div>
          <div className="chart-section">
            <TaskChart className="task-chart" data={summary} />
          </div>
        </div>
      ) : (
        !error && <GreenSpinner />
      )}

      {/* Render ManagerDashBoard if the user have manager or admin role */}
      {(user.role == 'manager' || user.role == 'admin') &&
      <ManagerDashboard/>
      }

      {/* Render AdminDashboard only if user role is admin */}
      {( user.role == 'admin') &&
      <AdminDashboard/>
      }

    </div>
    
  );
}
