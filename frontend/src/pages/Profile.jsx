import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';

export default function Profile({ user }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/taste-dna/profile')
      .then(res => {
        setProfile(res.data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.response?.data?.detail || 'Failed to load profile');
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <div style={{ minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div className="typing-indicator"><span /><span /><span /></div>
    </div>
  );

  if (error) return (
    <div style={{ minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24 }}>
      <div className="glass-card" style={{ padding: 40, textAlign: 'center', maxWidth: 400 }}>
        <span style={{ fontSize: 48 }}>🧬</span>
        <h2 style={{ marginTop: 16, marginBottom: 12 }}>No Taste DNA yet</h2>
        <p style={{ color: 'var(--khao-text-muted)', marginBottom: 24 }}>
          Take the 90-second quiz to map your palate!
        </p>
        <Link to="/quiz">
          <button className="glow-btn" style={{ padding: '14px 32px' }}>
            Take the Quiz →
          </button>
        </Link>
      </div>
    </div>
  );

  const AXES = [
    { key: 'heat_ceiling', label: '🌶️ Heat Ceiling', color: '#EF4444' },
    { key: 'sweet_tolerance', label: '🍯 Sweet Tolerance', color: '#F59E0B' },
    { key: 'acid_affinity', label: '🍋 Acid Affinity', color: '#10B981' },
    { key: 'umami_affinity', label: '🍖 Umami Affinity', color: '#8B5CF6' },
    { key: 'fat_palate', label: '🧈 Fat Palate', color: '#F97316' },
    { key: 'bitter_tolerance', label: '☕ Bitter Tolerance', color: '#6366F1' },
  ];

  const cuisineScores = profile.cuisine_scores || {};
  const topCuisines = Object.entries(cuisineScores)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5);

  return (
    <div style={{ maxWidth: 600, margin: '0 auto', padding: '40px 24px' }}>
      {/* Header */}
      <div className="fade-in-up" style={{ textAlign: 'center', marginBottom: 40 }}>
        <span style={{ fontSize: 56 }}>🧬</span>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, marginTop: 12 }}>
          <span className="gradient-text">{user.name}'s</span> Taste DNA
        </h1>
        <p style={{ color: 'var(--khao-text-muted)', marginTop: 8 }}>
          {profile.total_ratings} meals rated · {profile.quiz_completed ? 'Quiz completed' : 'Quiz pending'}
        </p>
      </div>

      {/* DNA Axes */}
      <div className="glass-card fade-in-up fade-in-up-delay-1" style={{ padding: 28, marginBottom: 20 }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: 20 }}>Taste Axes</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {AXES.map(axis => {
            const val = profile[axis.key] || 5;
            return (
              <div key={axis.key}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6, fontSize: '0.9rem' }}>
                  <span>{axis.label}</span>
                  <span style={{ fontWeight: 700, color: axis.color }}>{val.toFixed(1)}/10</span>
                </div>
                <div style={{
                  height: 8,
                  background: 'var(--khao-dark)',
                  borderRadius: 4,
                  overflow: 'hidden',
                }}>
                  <div style={{
                    height: '100%',
                    width: `${(val / 10) * 100}%`,
                    background: `linear-gradient(90deg, ${axis.color}88, ${axis.color})`,
                    borderRadius: 4,
                    transition: 'width 1s ease',
                  }} />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Cuisine Preferences */}
      {topCuisines.length > 0 && (
        <div className="glass-card fade-in-up fade-in-up-delay-2" style={{ padding: 28, marginBottom: 20 }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: 16 }}>Cuisine Preferences</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10 }}>
            {topCuisines.map(([cuisine, score]) => (
              <div key={cuisine} style={{
                background: 'var(--khao-dark)',
                border: '1px solid var(--khao-dark-border)',
                borderRadius: 14,
                padding: '10px 18px',
                display: 'flex',
                alignItems: 'center',
                gap: 8,
              }}>
                <span style={{ fontSize: '0.9rem', textTransform: 'capitalize' }}>
                  {cuisine.replace(/_/g, ' ')}
                </span>
                <span className="gradient-text" style={{ fontWeight: 700, fontSize: '0.85rem' }}>
                  {score}/10
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Stats */}
      <div className="glass-card fade-in-up fade-in-up-delay-3" style={{ padding: 28 }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: 16 }}>Your Stats</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          <div style={{ textAlign: 'center', padding: 16, background: 'var(--khao-dark)', borderRadius: 14 }}>
            <div className="gradient-text" style={{ fontSize: '1.8rem', fontWeight: 800 }}>{profile.total_ratings}</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--khao-text-muted)', marginTop: 4 }}>Meals Rated</div>
          </div>
          <div style={{ textAlign: 'center', padding: 16, background: 'var(--khao-dark)', borderRadius: 14 }}>
            <div className="gradient-text" style={{ fontSize: '1.8rem', fontWeight: 800 }}>
              {profile.texture_pref || 'Mixed'}
            </div>
            <div style={{ fontSize: '0.85rem', color: 'var(--khao-text-muted)', marginTop: 4 }}>Texture Pref</div>
          </div>
        </div>
      </div>

      {/* Retake Quiz */}
      <div style={{ textAlign: 'center', marginTop: 28 }}>
        <Link to="/quiz">
          <button className="ghost-btn">🔄 Retake Quiz</button>
        </Link>
      </div>
    </div>
  );
}
