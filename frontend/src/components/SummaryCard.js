import'./styles/SummaryCard.css'

/**
 * SummaryCard Component
 * ---------------------
 * Displays a card with a label and a value.
 * Calls the onClick callback with the label when clicked.
 */
export default function SummaryCard({ label, value, onClick }) {
  // Handle click on the card
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
