import React, { useState } from 'react';
import '../login/login.css';
import { useNavigate } from 'react-router-dom';
import './config.js';
import adduser from '../adduser.png';
import smiling from '../smilingpeople.jpeg'

const Login = () => {
  const navigate = useNavigate();

  const handleSubmitPress = event => {
    event.preventDefault(); //prevents page from reloading after form submit
   
    console.log("submit pressed");

    login_req()
  }

  //TODO: send login get request to server
  // If successful, save tfa jwt token and navigate to tfa page
  function login_req() {
    

    console.log("login function");
 
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
      console.log(this.status);

      var res = JSON.parse(this.response)

      if (this.readyState == 4){
        if(this.status == 200) {
          console.log("tfa generated")

          
          console.log("global config: ", global.config)
          navigate('/tfa');
        }
        //error handling for status 0
        else if (this.status == 0){
          console.log("error, no response from server");
         
        }
        else{
            
        }
    }
    };

    let url = "http://0.0.0.0:3307/login";
    
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    //send basic auth header
    

    //access control allow origin
    xhttp.setRequestHeader("Access-Control-Allow-Origin", "*");
    // //set header to application/json
    xhttp.setRequestHeader("Content-Type", "application/json");
      
    xhttp.timeout = 40000;
    xhttp.ontimeout = function (e){
        xhttp.abort();
        console.log("xhttp timout.");
  
    }
    xhttp.send();
}
  return (
    <div>
      <form onSubmit={handleSubmitPress}>
        <div className="form-inner">
          <h2>Input the name of the user you want to add</h2>

        <div className="form-group">
          <label htmlFor="">Name: </label>
          <input type="text" name="emotion" id="emotion" 
          required/>
        </div>
        
          <input type="submit" value="Submit"/>
        </div>
      </form>
      <div>
      <img src={smiling} />
      </div>

    </div>
  );
};
  
export default Login;
  
