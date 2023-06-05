import React, { useState } from 'react';
import '../App.css';
import { Link, useNavigate } from 'react-router-dom';
//import { useNavigate } from 'react-router-dom';


const UserEmotion = () => {
    const navigate = useNavigate();

    const [userEmotion, setUserEmotion] = useState('');
    const [errortext, setErrortext] = useState('');

    const handleSubmitPress = event => {
        event.preventDefault(); //prevents page from reloading after form submit
        setErrortext("")
        console.log("submit pressed");
    
        
    UserUI();
}
function UserUI() {
    console.log("userEmotion: " + userEmotion);

    console.log("user Emotion Entered");
    
    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function() {
        console.log(this.status);

        var res = JSON.parse(this.response)

        if (this.readyState == 4){
        if(this.status == 200) {
            console.log("Inputted")
            /*
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
            }*/
            //console.log("global config: ", global.config)
            navigate('/userInput');
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

    let url = "http://0.0.0.0:3307/saveUserEmotion";
    
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    //send basic auth header
    xhttp.setRequestHeader("Authorization", "Basic " + window.btoa(userEmotion));

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
        <div class="parent">
            <div><Link to="/userInput" onclick={(e) => setUserEmotion("happy")} value={userEmotion} 
            >Happy</Link></div>
            <div><Link to="/userInput" onclick={(e) => setUserEmotion("happy")} value={userEmotion}
            >Sad</Link></div>
            <div><Link to="/userInput" onclick={(e) => setUserEmotion("happy")} value={userEmotion}
            >Upset</Link></div>
            <div><Link to="/userInput" onclick={(e) => setUserEmotion("happy")} value={userEmotion}
            >Stressed</Link></div>
            <div><Link to="/userInput" onclick={(e) => setUserEmotion("happy")} value={userEmotion}
            >Upset</Link></div>
            <div><Link to="/userInput" onclick={(e) => setUserEmotion("happy")} value={userEmotion}
            >Nervous</Link></div>
            <div><Link to="/userInput" onclick={(e) => setUserEmotion("happy")} value={userEmotion}
            >Depressed</Link></div>
            <div><Link to="/userInput" onclick={(e) => setUserEmotion("happy")} value={userEmotion}
            >Angry</Link></div>
            <div><Link to="/userInput" onclick={(e) => setUserEmotion("happy")} value={userEmotion}
            >Excited</Link></div>
        </div>
        
    );
};
export default UserEmotion;