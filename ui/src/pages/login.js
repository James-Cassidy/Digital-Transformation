import React, { useState } from 'react';
import '../login/login.css';
import { useNavigate } from 'react-router-dom';
import './config.js';

const Login = () => {
  const navigate = useNavigate();

  const [userEmail, setUserEmail] = useState('');
  const [userPassword, setUserPassword] = useState('');
  const [errortext, setErrortext] = useState('');


  const handleSubmitPress = event => {
    event.preventDefault(); //prevents page from reloading after form submit
    setErrortext("")
    console.log("submit pressed");

    login_req()
  }

  //TODO: send login get request to server
  // If successful, save tfa jwt token and navigate to tfa page
  function login_req() {
    console.log("username: " + userEmail + "password: " + userPassword)

    console.log("login function");
 
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
      console.log(this.status);

      var res = JSON.parse(this.response)

      if (this.readyState == 4){
        if(this.status == 200) {
          console.log("tfa generated")

          global.config = {
            jwtToken: {
              token: res.answer.tfaToken,
              type: 'tfa'
            },
            userDetails:{
              forename:res.answer.userForename,
              surname:res.answer.userSurname,
              therapist:res.answer.userTherapist
          }
          }
          console.log("global config: ", global.config)
          navigate('/tfa');
        }
        //error handling for status 0
        else if (this.status == 0){
          console.log("error, no response from server");
          setErrortext("ERROR: no response from server");
        }
        else{
            setErrortext("ERROR: Wrong username or password");
            alert("ERROR: Wrong username or password");
        }
    }
    };

    let url = "http://0.0.0.0:3307/login";
    
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    //send basic auth header
    xhttp.setRequestHeader("Authorization", "Basic " + window.btoa(userEmail + ":" + userPassword));

    //access control allow origin
    xhttp.setRequestHeader("Access-Control-Allow-Origin", "*");
    // //set header to application/json
    xhttp.setRequestHeader("Content-Type", "application/json");
      
    xhttp.timeout = 40000;
    xhttp.ontimeout = function (e){
        xhttp.abort();
        console.log("xhttp timout.");
        setErrortext("ERROR: request timed out")
    }
    xhttp.send();
}


  return (
    <form onSubmit={handleSubmitPress}>
      <div className="form-inner">
        <h2>Login</h2>
        {(errortext !== "") ? (<div className='error'>{errortext}</div> ) : ""}

        <div className="form-group">
          <label htmlFor="email">Email: </label>
          <input type="email" name="email" id="email" onChange={(e) => setUserEmail(e.target.value)} value={userEmail}
          required/>
        </div>
        
        <div className="form-group">
          <label htmlFor="password">Password: </label>
          <input type="password" name="password" id="password" onChange={e => setUserPassword(e.target.value)} value={userPassword}
          required/>
      </div>
      <input type="submit" value="LOGIN" />
      </div>
    </form>
  );
}
    
export default Login;