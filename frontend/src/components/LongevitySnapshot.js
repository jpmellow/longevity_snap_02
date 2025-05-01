import React, { useState } from 'react';
import { registerWithEmail, loginWithEmail } from '../sdk/firebase';

const gradientBg = {
  background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  minHeight: '100vh',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};

const cardStyle = {
  background: 'rgba(255,255,255,0.95)',
  borderRadius: '20px',
  boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
  padding: '2.5rem 2rem',
  width: '100%',
  maxWidth: '380px',
  textAlign: 'center',
};

const inputStyle = {
  width: '100%',
  padding: '0.75rem',
  margin: '0.5rem 0',
  borderRadius: '8px',
  border: '1px solid #d4f5e9',
  outline: 'none',
  fontSize: '1rem',
};

const buttonStyle = {
  width: '100%',
  padding: '0.75rem',
  margin: '1rem 0 0 0',
  borderRadius: '8px',
  border: 'none',
  background: 'linear-gradient(90deg, #43e97b 0%, #38f9d7 100%)',
  color: '#fff',
  fontWeight: 'bold',
  fontSize: '1.1rem',
  cursor: 'pointer',
  transition: 'background 0.3s',
};

const LongevitySnapshot = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      if (isRegister) {
        await registerWithEmail(email, password);
        setSuccess('Registration successful! You can now log in.');
      } else {
        await loginWithEmail(email, password);
        setSuccess('Login successful!');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={gradientBg}>
      <form style={cardStyle} onSubmit={handleSubmit}>
        <h2 style={{ color: '#21c97b', marginBottom: '1.5rem', fontWeight: 700 }}>
          Longevity Snapshot
        </h2>
        <input
          style={inputStyle}
          type="email"
          placeholder="Email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
        <input
          style={inputStyle}
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
        {error && <div style={{ color: 'red', margin: '0.5rem 0' }}>{error}</div>}
        {success && <div style={{ color: 'green', margin: '0.5rem 0' }}>{success}</div>}
        <button type="submit" style={buttonStyle}>
          {isRegister ? 'Register' : 'Login'}
        </button>
        <div style={{ marginTop: '1rem' }}>
          {isRegister ? 'Already have an account?' : "Don't have an account?"}
          <button
            type="button"
            style={{ ...buttonStyle, background: 'none', color: '#21c97b', margin: '0.5rem 0 0 0', fontSize: '1rem', fontWeight: 400 }}
            onClick={() => setIsRegister(!isRegister)}
          >
            {isRegister ? 'Login' : 'Register'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default LongevitySnapshot;
