import React, { useState } from 'react';
import '../login/login.css';
import { useNavigate } from 'react-router-dom';
import './config.js';


const TFA = () => {
  const navigate = useNavigate();

  const [tfaCode, setTfaCode] = useState('');
  const [errortext, setErrortext] = useState('');


  const handleSubmitPress = event => {
    event.preventDefault(); //prevents page from reloading after form submit
    setErrortext("")
    
    tfa_req()
  }

  //TODO: send signup get request to server
  function tfa_req() {
    console.log("tfa request")
    console.log('tfaCode: ', tfaCode)
 
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
      console.log(this.status);
      console.log(this.response);

      var res = JSON.parse(this.response)

      if (this.readyState == 4){
        if(this.status == 200) {
          console.log("signup successful")

          global.config.jwtToken = {
              token: res.answer,
              type: 'ltk'
          }

        alert("login successful")

        console.log("global config: ", global.config)
          navigate('/index');
        }
        //error handling for status 0
        else if (this.status == 0){
          console.log("error, no response from server");
          setErrortext("ERROR: no response from server");
        }
        else{
            setErrortext("ERROR: " + res.string);
            alert("ERROR: " + res.string);
        }
    }
    };

    let url = "http://0.0.0.0:3307/2fa";
    url = url + "?tfacode=" + tfaCode   

    // send get request to url with tfacode as query string
    xhttp.open("GET", url, true);

    //access control allow origin
    xhttp.setRequestHeader("Access-Control-Allow-Origin", "*");
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.setRequestHeader("x-access-token", global.config.jwtToken.token);
      
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
        <h2>Two Factor Authentication</h2>

        <div className="form-group">
          <label htmlFor="tfaCode">Two Factor Authentication Code: </label>
          <input type="text" name="tfaCode" id="tfaCode" onChange={(e) => setTfaCode(e.target.value)} value={tfaCode}/>
        </div>
        <input type="submit" value="SUBMIT" />
      </div>


    </form>
  );
}
    
export default TFA;