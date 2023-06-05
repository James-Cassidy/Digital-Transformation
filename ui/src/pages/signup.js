import React, { useState } from 'react';
import '../login/login.css';
import { useNavigate } from 'react-router-dom';
import './config.js';


const Signup = () => {
  const navigate = useNavigate();

  //fields needed for signup
  const [details, setDetails] = useState({email:"", password:"", forename:"", middle_names:"", surname:"", dob:"",
  gender:"", address1:"", address2:"", address3:"", city:"", country:"", postcode:""});
  const [error, setErrortext] = useState("");

  const handleSubmitPress = event => {
    event.preventDefault(); //prevents page from reloading after form submit

    setErrortext("")
    console.log("submit pressed");

    signup_req()

  }

    //TODO: send signup get request to server
    function signup_req() {
      console.log("signup request")
      console.log('details: ', details)
   
      let xhttp = new XMLHttpRequest();
  
      xhttp.onreadystatechange = function() {
        console.log(this.status);
        console.log(this.response);

        var res = JSON.parse(this.response)

        if (this.readyState == 4){
          if(this.status == 200) {
            console.log("signup successful")

            global.config = {
              jwtToken: {
                token: res.answer,
                type: 'ltk'
            }
            }

            global.config = {
              jwtToken: {
                token: res.answer,
                type: 'ltk'
              },
              userDetails:{
                forename:details.forename,
                surname:details.surname,
                therapist:false
            }
            }

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

      let url = "http://0.0.0.0:3307/register";
      url = url + "?email=" + details.email + "&password=" + details.password + "&forename=" + details.forename + "&middle_names=" + details.middle_names + "&surname=" + details.surname + "&dob=" + details.dob + "&gender"
      + details.gender + "&address1=" + details.address1 + "&address2=" + details.address2 + "&address3=" + details.address3 + "&city=" + details.city + "&country=" + details.country + "&postcode=" + details.postcode;
      

      // send get request to url with details as query string
      xhttp.open("GET", url, true);
  
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
        <h2>Signup</h2>
        {(error !== "") ? (<div className='error'>{error}</div> ) : ""}

        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input type="email" name="email" id="email"
          onChange={e => setDetails({...details, email: e.target.value})} value={details.email}
          required/>
        </div>

        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input type="password" name="password" id="password" onChange={e => setDetails({...details, password: e.target.value})} value={details.password}
          required/>
        </div>

        <div className="form-group">
          <label htmlFor="forename">Forename:</label>
          <input type="text" name="forename" id="forename" onChange={e => setDetails({...details, forename: e.target.value})} value={details.forename}
          required/>
        </div>

        <div className="form-group">
          <label htmlFor="middle_names">Middle Names:</label>
          <input type="text" name="middle_names" id="middle_names" onChange={e => setDetails({...details, middle_names: e.target.value})} value={details.middle_names}/>
        </div>

        <div className="form-group">
          <label htmlFor="surname">Surname:</label>
          <input type="text" name="surname" id="surname" onChange={e => setDetails({...details, surname: e.target.value})} value={details.surname}
          required/>
        </div>

        <div className="form-group">
          <label htmlFor="dob">Date of Birth:</label>
          <input type="date" name="dob" id="dob" onChange={e => setDetails({...details, dob: e.target.value})} value={details.dob}
          required/>
        </div>

        <div className="form-group">
          <label htmlFor="gender">Gender:
          <select name="gender" id="gender" onChange={e => setDetails({...details, gender: e.target.value})} value={details.gender}>
            <option value="prefer_not_to_say">Prefer not to say</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </label>
        </div>

        <div className="form-group">
          <label htmlFor="address1">Address 1:</label>
          <input type="text" name="address1" id="address1" onChange={e => setDetails({...details, address1: e.target.value})} value={details.address1}
          required/>
        </div>

        <div className="form-group">
          <label htmlFor="address2">Address 2:</label>
          <input type="text" name="address2" id="address2" onChange={e => setDetails({...details, address2: e.target.value})} value={details.address2}/>
        </div>

        <div className="form-group">
          <label htmlFor="address3">Address 3:</label>
          <input type="text" name="address3" id="address3" onChange={e => setDetails({...details, address3: e.target.value})} value={details.address3}/>
        </div>

        <div className="form-group">
          <label htmlFor="city">City:</label>
          <input type="text" name="city" id="city" onChange={e => setDetails({...details, city: e.target.value})} value={details.city}
          required/>
        </div>

        <div className="form-group">
          <label htmlFor="country">Country:</label>
          <input type="text" name="country" id="country" onChange={e => setDetails({...details, country: e.target.value})} value={details.country}
          required/>
        </div>

        <div className="form-group">
          <label htmlFor="postcode">Postcode:</label>
          <input type="text" name="postcode" id="postcode" onChange={e => setDetails({...details, postcode: e.target.value})} value={details.postcode}
          required/>
        </div>

        <input type="submit" value="SIGNUP"/>
      </div>
    </form>
  );
}
    
export default Signup;