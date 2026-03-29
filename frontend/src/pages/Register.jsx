import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api';

export default function Register({ onLogin }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [area, setArea] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const AREAS = [
    'Malviya Nagar', 'Hauz Khas', 'Saket', 'Lajpat Nagar',
    'Connaught Place', 'Karol Bagh', 'Cyber City', 'Sector 29',
    'Greater Kailash', 'Old Delhi', 'Dwarka', 'Noida',
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await api.post('/auth/register', { name, email, password, area });
      onLogin(res.data.user, res.data.token);
      navigate('/quiz');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed');
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
      <div className="glass-card fade-in-up" style={{ padding: 40, width: '100%', maxWidth: 480 }}>
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <span style={{ fontSize: 40 }}>🧬</span>
          <h1 style={{
            fontSize: '1.8rem',
            fontWeight: 800,
            marginTop: 12,
            letterSpacing: '-0.5px',
          }}>
            Create your <span className="gradient-text">Taste DNA</span>
          </h1>
          <p style={{ color: 'var(--khao-text-muted)', marginTop: 8, fontSize: '0.95rem' }}>
            Takes 90 seconds. Changes how you eat forever.
          </p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <input
            type="text"
            placeholder="Your name"
            value={name}
            onChange={e => setName(e.target.value)}
            className="khao-input"
            required
          />
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
            placeholder="Password (6+ characters)"
            value={password}
            onChange={e => setPassword(e.target.value)}
            className="khao-input"
            minLength={6}
            required
          />
          <select
            value={area}
            onChange={e => setArea(e.target.value)}
            className="khao-input"
            style={{ cursor: 'pointer' }}
          >
            <option value="">Select your area (optional)</option>
            {AREAS.map(a => <option key={a} value={a}>{a}</option>)}
          </select>

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
            {loading ? 'Creating...' : '🍛 Create Account & Take Quiz'}
          </button>
        </form>

        <p style={{ textAlign: 'center', marginTop: 24, color: 'var(--khao-text-muted)', fontSize: '0.9rem' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: 'var(--khao-orange)', textDecoration: 'none', fontWeight: 600 }}>
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
