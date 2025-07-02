/**
 * TaskChart Component
 * -------------------
 * Renders a pie chart displaying the distribution of tasks by status.
 * Uses Recharts library for visualization.
 *
 * Props:
 * - data: An object containing task counts with keys:
 *    assigned_tasks, completed_tasks, overdue_tasks, soon_due_tasks
 *
 * Usage:
 * Used in the Stats dashboard to visualize task status distribution.
 */

import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";
import './styles/TaskChart.css'



/**
 * Prepares data and renders a pie chart for task status distribution.
 * @param {object} data - Task summary data
 * @returns {JSX.Element} Pie chart markup
 */
export default function TaskChart({ data }) {
  
  //prepare data for the Pie chart slices using the task counts
  const chartData = [
    { name: "Assigned", value: data.assigned_tasks },
    { name: "Completed", value: data.completed_tasks },
    { name: "Overdue", value: data.overdue_tasks },
    { name: "Soon Due", value: data.soon_due_tasks },
  ];

  //Definig colour corresponding to each status slice
  const COLORS = ["#8884d8", "#82ca9d", "#ff7f7f", "#ffd966"];

  return (
    <div className="chart-container">
      <h2 className="chart-heading">Task Status Overview</h2>
      <PieChart width={400} height={300}>
        {/* PieChart configurations */}
        <Pie data={chartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} fill="#8884d8" label>
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        {/* Tooltip shows details on hover */}
        <Tooltip />
        {/* Legend displays color coded task statuses */}
        <Legend />
      </PieChart>
    </div>
  );
}
