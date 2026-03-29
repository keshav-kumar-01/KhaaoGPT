import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api';

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await api.post('/auth/login', { email, password });
      onLogin(res.data.user, res.data.token);
      navigate('/chat');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: 'calc(100vh - 64px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: 24,
    }}>
      <div className="glass-card fade-in-up" style={{ padding: 40, width: '100%', maxWidth: 440 }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <span style={{ fontSize: 40 }}>🍛</span>
          <h1 style={{
            fontSize: '1.8rem',
            fontWeight: 800,
            marginTop: 12,
            letterSpacing: '-0.5px',
          }}>
            Welcome back
          </h1>
          <p style={{ color: 'var(--khao-text-muted)', marginTop: 8, fontSize: '0.95rem' }}>
            Your taste buds remember you
          </p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            className="khao-input"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            className="khao-input"
            required
          />

          {error && (
            <div style={{
              background: 'rgba(220, 38, 38, 0.1)',
              border: '1px solid rgba(220, 38, 38, 0.2)',
              borderRadius: 12,
              padding: '10px 16px',
              color: 'var(--khao-crimson)',
              fontSize: '0.9rem',
            }}>
              {error}
            </div>
          )}

          <button type="submit" className="glow-btn" disabled={loading}
            style={{ width: '100%', padding: '14px', marginTop: 8 }}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: 24, color: 'var(--khao-text-muted)', fontSize: '0.9rem' }}>
          Don't have an account?{' '}
          <Link to="/register" style={{ color: 'var(--khao-orange)', textDecoration: 'none', fontWeight: 600 }}>
            Sign up
          </Link>
        </p>

        <div style={{
          textAlign: 'center',
          marginTop: 20,
          padding: '12px',
          background: 'rgba(255,107,53,0.05)',
          borderRadius: 12,
          fontSize: '0.8rem',
          color: 'var(--khao-text-muted)',
        }}>
          Demo: <strong>admin@khaogpt.com</strong> / <strong>admin123</strong>
        </div>
      </div>
    </div>
  );
}
