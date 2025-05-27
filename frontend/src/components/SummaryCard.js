import'./styles/SummaryCard.css'

export default function SummaryCard({ label, value, onClick }) {
  const handleClick = () => {
    if (onClick) {
      onClick(label); // Pass label back to Stats for routing
    }
  };

  return (
    <div onClick={handleClick} className="card-container">
      <h3 className="label-heading">{label}</h3>
      <p className="label-text">{value}</p>
    </div>
  );
}
