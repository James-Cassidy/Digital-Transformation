import {React,  useState, Fragment} from 'react';
import { Line } from "react-chartjs-2";
import { Bar } from 'react-chartjs-2';
import { faker } from '@faker-js/faker';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Data } from '../components/data/patients'
import sad from "../components/reactions/sad.png";
import angry from "../components/reactions/angry.png";
import miserable from "../components/reactions/miserable.png";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: false,
      text: 'Chart.js Line Chart',
    },
  },
};

export const options1 = {
  responsive: true,
  plugins: {
    legend: {
      display: false,
    },
    title: {
      display: false,
      text: 'Chart.js Line Chart',
    },
  },
};

const optionsT = [
  [ '00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00', '00:00'], 
  [ '00:00', '06:00', '12:00', '18:00', '00:00', '06:00', '12:00', '18:00', '00:00'],
  [ 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'],
 ]; 

 const labels = [ 'affectionate', 'angry', 'annoyed', 'awkward', 'happy', 'miserable', 'sad', 'shocked', 'tired'];

 export const EmotionalData = {
  labels,
  datasets: [
      {
        label: "",
        data: ['2','6','4','1','7','3','1','12','9'],
        borderColor: 'rgb(118, 36, 181)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },      
    ],
  };

export const HeartRateData = {
  labels: null,
  datasets: [
    {
      label: 'Heart Rate',
      data: optionsT[0].map(() => faker.datatype.number({ min: 0, max: 200 })),
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.5)',
    },
  ],
};

export const BloodPressureData = {
  labels: null,
  datasets: [
      {
        label: 'Systolic',
        data: optionsT[0].map(() => faker.datatype.number({ min: 90, max: 130 })), //90-130 hard-coded
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
      },
      {
        label: 'Diastolic',
        data: optionsT[0].map(() => faker.datatype.number({ min: 60, max: 90 })),//60-90 hard-coded
        borderColor: 'rgb(53, 162, 235)',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      },
    ],
  };


export const CortisolData = {
  labels: null,
  datasets: [
    {
      label: 'Corisol',
      data: optionsT[0].map(() => faker.datatype.number({ min: 0, max: 20 })),
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.5)',
    },
  ],
};


export default function PatientRecords(){
 
  HeartRateData.labels = optionsT[0];
  BloodPressureData.labels = optionsT[0];
  CortisolData.labels = optionsT[0];

  const [details, setDetails] = useState({labels1:optionsT[0], labels2:optionsT[0], labels3:optionsT[0]});
  HeartRateData.labels = details.labels1;
  BloodPressureData.labels = details.labels2;
  CortisolData.labels = details.labels3;
  
  const current = new Date();
  const date = `${current.getDate()}/${current.getMonth()+1}/${current.getFullYear()}`;
 
  function alertMSG() {
    alert("Patient notes saved.");
  }

  return (
    
    
    <Fragment> 
    <div style={{
        display: 'flex',
        justifyContent: 'Center',
        alignItems: 'Left',
        height: '10vh',
        padding: '10px'
      }}>
      <br></br><h2>Patient Records</h2><br></br>
    </div>

    <form>
      <div className="form-inner">
        <h3>Patient #{Data[0].id}</h3>
        <br></br>
        <p>Select patient: <select id="mySelect" placeholder="Select an option"  >
                    <option value="p1">{Data[0].id}</option>
                    <option value="p2">{Data[1].id}</option>
                    <option value="p3">{Data[2].id}</option>
                  </select></p>
        
        <br></br>
        <div className="form-group">
          <label htmlFor="email">Name: </label>
          <input type="name" name="name" id="name" value={Data[0].name} readonly/>
        </div>

        <div className="form-group">
          <label htmlFor="reactions">Current Response:&nbsp;  </label>
          <img src={sad} className="App-logo" alt="logo" />&nbsp;
          <img src={angry} className="App-logo" alt="logo" />&nbsp;
          <img src={miserable} className="App-logo" alt="logo" />

          </div>

        <div className="form-group">
          <label htmlFor="password">Notes: </label>
          <textarea type="notes" name="notes" id="notes" rows="4" cols="50" value={Data[0].notes}></textarea>
      </div>
      <button onClick={alertMSG}>Save Notes</button>
      </div>
    </form>

    <div style={{
        display: 'flex',
        justifyContent: 'Center',
        alignItems: 'Left',
        height: '10vh',
        padding: '10px'
      }}>
      <br></br><h2>Patient Analytics</h2>
    </div>
    

      <div style={{ position: "relative", margin: "auto", width: "50vw" }}>
      <br></br>

      <h2 style={{ textAlign: "center" }}>Patient Emotions</h2>
      <Bar options={options1} data={EmotionalData} />

      <br></br><p>The graph above indicates how many times today ({date}) each emotion has been triggered by ({Data[0].name}).</p><br></br>
      
      <h2 style={{ textAlign: "center" }}>Heart Rate (bpm)</h2>
      <Line options={options} data={HeartRateData} redraw/>

      <br></br><p>Please select the time interval you wish to view for Heart-Rate:</p>
      <select  onChange={e => setDetails({...details, labels1: optionsT[e.target.selectedIndex]})} placeholder="Select an option"  >
            <option value="labels1">24 hours</option>
            <option value="labels2">48 hours</option>
            <option value="labels3">7-day average</option>
          </select>


      <br></br><br></br>
      <h2 style={{ textAlign: "center" }}>Blood Pressure (mmHg)</h2>
      <Bar options={options} data={BloodPressureData} />

      <br></br><p>Please select the time interval you wish to view for Blood Pressure:</p>
      <select  onChange={e => setDetails({...details, labels2: optionsT[e.target.selectedIndex]})} placeholder="Select an option"  >
            <option value="labels1">24 hours</option>
            <option value="labels2">48 hours</option>
            <option value="labels3">7-day average</option>
          </select>

      <br></br><br></br>
      <h2 style={{ textAlign: "center" }}>Cortisol (mcg/dL)</h2>
      <Line options={options} data={CortisolData} />

      <br></br><p>Please select the time interval you wish to view for Cortisol:</p>
      <select  onChange={e => setDetails({...details, labels3: optionsT[e.target.selectedIndex]})} placeholder="Select an option"  >
            <option value="labels1">24 hours</option>
            <option value="labels2">48 hours</option>
            <option value="labels3">7-day average</option>
          </select>
      
      <br></br>  <br></br>  <br></br>
      </div>
    </Fragment>
  )
}