import React, {useState} from 'react'
import '../login/login.css';

function TFAForm({Login: TFA, error}) {
  const [details, setDetails] = useState({tfaCode: ""})

  const submitHandler = e =>{
    e.preventDefault();

    TFA(details);
  }

  return (
    <form onSubmit={submitHandler}>
      <div className="form-inner">
        <h2>Two Factor Authentication</h2>
        {(error !== "") ? (<div className='error'>{error}</div> ) : ""}
        <div className="form-group">
          <label htmlFor="tfaCode">Two Factor Authentication Code: </label>
          <input type="text" name="tfaCode" id="tfaCode" onChange={e => setDetails({...details, tfaCode: e.target.value})} value={details.tfaCode}/>
        </div>
        <input type="submit" value="TFA" />
      </div>
    </form>
  )
}

export default TFAForm