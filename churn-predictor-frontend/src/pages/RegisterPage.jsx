import { useState } from 'react';
import authService from '../services/authService';
import './AuthPages.css';

export default function RegisterPage({ onRegisterSuccess, onSwitch }) {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await authService.register(email, username, password);
      onRegisterSuccess();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-layout">
        <div className="auth-intro">
          <p className="auth-eyebrow">CHURN PREDICTOR / NEW MEMBER</p>
          <h1>Join the frame.</h1>
          <p className="auth-sub">Create an account to start predicting.</p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label htmlFor="email">Email address</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {error && <p className="auth-error">{error}</p>}

          <button type="submit" className="auth-btn" disabled={loading}>
            {loading ? 'Creating...' : 'Create account'}
          </button>

          <button type="button" className="auth-link" onClick={onSwitch}>
            Already have an account? Sign in
          </button>
        </form>
      </div>
    </div>
  );
}