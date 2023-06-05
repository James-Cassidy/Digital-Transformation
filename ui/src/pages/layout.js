import { Outlet, Link } from "react-router-dom";
import logo from '../health_logo.png';
import appName from '../name2.png'
import '../App.css';

const Layout = () => {
  return (
    <>
      <header className="header">
        <Link to="/index">
        <img src={appName} className="App-name" alt="app name" />
        </Link>
    </header>
      <div class="layout">
      <nav>
        <ul>
          <li>
           <Link to="/index"><img href="https://www.flaticon.com/free-icons/daily-health-app" src={logo} className="App-logo" alt="logo" /></Link>
          </li>
          <li>
            <Link to="/index">Home</Link>
          </li>
          <li>
            <Link to="/patient_records">Patient Records</Link>
          </li>
          <li>
            <Link to="/prescriptions">Prescriptions</Link>
          </li>
          <li>
            <Link to="/reports">Reports</Link>
          </li>
          <li>
            <Link to="/billing">Billing</Link>
          </li>
          <li>
            <Link to="/admin">Admin</Link>
          </li>
          <li>
            <Link to="/help">User Requests</Link>
          </li>
          <li>
            <Link to="/UserUI">UserUI</Link>
          </li>
          <li>
            <Link to="/faq">Add User</Link>
          </li>
          <li style={{float:"right"}}>
            <Link to="/login">Log-in</Link>
          </li>
          <li style={{float:"right"}}>
            <Link to="/signup">Sign-up</Link>
          </li>
        </ul>
      </nav>
      </div>
      
      <Outlet />
    </>
  )
};

export default Layout;