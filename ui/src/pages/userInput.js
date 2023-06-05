import React, { useState } from 'react';
import '../login/login.css';
import { useNavigate } from 'react-router-dom';
import './config.js';

const UserInput = () => {
  const navigate = useNavigate();
  const [userFeeling, setUserFeelings] = useState('');
  const [errortext, setErrortext] = useState('');
  
  const handleSubmitPress = event => {
    event.preventDefault(); //prevents page from reloading after form submit
    setErrortext("")
    console.log("submit pressed");

    submit_response()
  }

  //TODO: send login get request to server
  // If successful, save tfa jwt token and navigate to tfa page
  function submit_response() {
    console.log("user: " + userFeeling)

    console.log("login function");
 
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
      console.log(this.status);
      console.log(this.response);

      var res = JSON.parse(this.response)

      if (this.readyState == 4){
        if(this.status == 200) {
          console.log("tfa generated")

          global.config = {
            jwtToken: {
              token: res.answer,
              type: 'tfa'
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
    xhttp.setRequestHeader("Authorization", "Basic " + window.btoa(userFeeling));

    //access control allow origin
    xhttp.setRequestHeader("Access-Control-Allow-Origin", "*");
    // //set header to application/json
    xhttp.setRequestHeader("Content-Type", "application/json");
      
    xhttp.timeout = 10000;
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
        <h2>Text Input</h2>
        {(errortext !== "") ? (<div className='error'>{errortext}</div> ) : ""}
        <div className="form-group">
          <label htmlFor="email">Feeling</label>
          <input type="text" name="feelings" id="feelings" onChange={(e) => setUserFeelings(e.target.value)} value={userFeeling}
          required/>
        </div>
      <input type="submit" value="Submit response" />
      </div>
    </form>
  );
  //test
}
    
export default UserInput;