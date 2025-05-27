import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";
import './styles/TaskChart.css'

export default function TaskChart({ data }) {
  
  
  const chartData = [
    { name: "Assigned", value: data.assigned_tasks },
    { name: "Completed", value: data.completed_tasks },
    { name: "Overdue", value: data.overdue_tasks },
    { name: "Soon Due", value: data.soon_due_tasks },
  ];

  const COLORS = ["#8884d8", "#82ca9d", "#ff7f7f", "#ffd966"];

  return (
    <div className="chart-container">
      <h2 className="chart-heading">Task Status Overview</h2>
      <PieChart width={400} height={300}>
        <Pie data={chartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={100} fill="#8884d8" label>
          {chartData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
}
