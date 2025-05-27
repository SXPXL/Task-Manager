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

export default function Stats() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");
  const { token, user } = useAuth();
  const navigate = useNavigate();
  

  const handleClick = (label) => {
   
    const status = label.toLowerCase().replace(/\s/g, "_"); // "Due Soon" → "due_soon"
    navigate(`/tasks/${status}`);
  };
  

  useEffect(() => {
    if (!token) return;

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
      {summary ? (
        <div className="dashboard-body">
          <div className="card-labels">
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

      {(user.role == 'manager' || user.role == 'admin') &&
      <ManagerDashboard/>
      }
      {( user.role == 'admin') &&
      <AdminDashboard/>
      }

    </div>
    
  );
}
