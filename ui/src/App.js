import React from 'react';
import './App.css';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages';
import PatientRecords from './pages/patient_records';
import Prescriptions from './pages/prescriptions';
import Reports from './pages/reports';
import Billing from './pages/billing';
import Admin from './pages/admin';
import Help from './pages/help';
import FAQ from './pages/faq';
import SignUp from './pages/signup';
import Login from './pages/login';
import Layout from './pages/layout';
import TFA from './pages/tfa';
import UserUI from './pages/userUI';
import UserInput from './pages/userInput';

function App() {
  return (
    <BrowserRouter>
       <Routes>
        <Route path="/" element={<Layout />}>
        <Route path="/" element={<Navigate to="/index"/>} />
        <Route path="/index" element={<Home />} />
        <Route path="/patient_records" element={<PatientRecords />} />
        <Route path='/prescriptions' element={<Prescriptions />} />
        <Route path='/reports' element={<Reports />} />
        <Route path="/billing" element={<Billing />} />
        <Route path='/admin' element={<Admin />} />
        <Route path='/help' element={<Help />} />
        <Route path='/faq' element={<FAQ />} />
        <Route path='/signup' element={<SignUp />} />
        <Route path='/login' element={<Login />} />
        <Route path='/tfa' element={<TFA />} />
        <Route path='/userUI' element={<UserUI />} />
        <Route path='/userInput' element={<UserInput />} />
        </Route>
      </Routes>
    </BrowserRouter>
    
  );
}


export default App;