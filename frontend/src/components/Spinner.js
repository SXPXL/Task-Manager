/**
 * GreenSpinner Component
 * ----------------------
 * Displays a centered green spinner for loading states.
 *
 * Usage:
 * Used throughout the app to indicate loading or pending operations.
 */

import "./styles/Spinner.css";

export default function GreenSpinner() {
  /**
   * Renders a green spinner animation.
   * @returns {JSX.Element} Spinner markup
   */
  return (
    <div className="spinner-container">
      <div className="spinner"></div>
    </div>
  );
}
