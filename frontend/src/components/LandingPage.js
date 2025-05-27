import React from 'react';
import './styles/LandingPage.css';
import {Link} from 'react-router-dom'


const LandingPage = () => {
  
  return (
    <div className="fullpage">
    <div className="landing-container">
      <div className="landing-box">
        <h1>Project-X</h1>
        <div className="tagline">Just a Task Planner But Better!</div>
        <p>
          Take control of your projects and stay on top of your goals with Project-X  —
          smart, simple, and made for you.
        </p>
        <div className="buttons">
          {/* Buttons for navigation to Sign Up and Sign In pages */}
          <Link to="/register"><button className="btn btn-signup">Sign Up</button></Link>
          <Link to="/login"><button className="btn btn-login">Sign In</button></Link>
        </div>
        <footer>© 2025 Project-X. All rights reserved.</footer>
      </div>
    </div>
    </div>
  );
};

export default LandingPage;
