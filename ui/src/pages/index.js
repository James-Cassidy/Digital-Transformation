import React from 'react';
import './config.js';


const Home = () => {
  function set_display_text() {

    if (global.config.jwtToken.type == 'ltk') {
      return "Welcome " + global.config.userDetails.forename + " " + global.config.userDetails.surname;
      
    }
    else {
      return "Welcome. Please log in or sign up.";
    }
  }


  return (
    
    <div
      style={{
        display: 'flex',
        justifyContent: 'Center',
        alignItems: 'Left',
        height: '100vh',
        padding: '10px'
      }}
    >
      <h1>{set_display_text()}</h1>
    </div>
  );
};
  
export default Home;