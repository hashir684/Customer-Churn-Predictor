import { useState } from 'react';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ChurnPredictor from './pages/ChurnPredictor';
import authService from './services/authService';
import './App.css';

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(authService.isLoggedIn());
  const [showRegister, setShowRegister] = useState(false);

  const handleLogout = () => {
    authService.logout();
    setIsLoggedIn(false);
  };

  if (!isLoggedIn) {
    return showRegister ? (
      <RegisterPage
        onRegisterSuccess={() => setShowRegister(false)}
        onSwitch={() => setShowRegister(false)}
      />
    ) : (
      <LoginPage
        onLoginSuccess={() => setIsLoggedIn(true)}
        onSwitch={() => setShowRegister(true)}
      />
    );
  }

  return (
    <div>
      <button className="logout-btn" onClick={handleLogout}>Logout</button>
      <ChurnPredictor />
    </div>
  );
}