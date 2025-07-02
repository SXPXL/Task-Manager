import'./styles/SummaryCard.css'

/**
 * SummaryCard Component
 * ---------------------
 * Displays a card with a label and a value.
 * Calls the onClick callback with the label when clicked.
 *
 * Props:
 * - label: The label to display on the card
 * - value: The value to display on the card
 * - onClick: Callback function to call when the card is clicked
 *
 * Usage:
 * Used in the Stats dashboard to show task summary counts.
 */
export default function SummaryCard({ label, value, onClick }) {
  /**
   * Handles click on the card and calls the onClick callback with the label.
   * @returns {void}
   */
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
