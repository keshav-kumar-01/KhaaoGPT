import { useState } from 'react';
import api from '../api';

const SPOT_TYPES = ['Restaurant', 'Cafe', 'Dhaba', 'Street Stall', 'Home Kitchen', 'Food Cart'];
const TASTE_TAGS = [
  'Spicy', 'Very Spicy', 'Mild', 'Tangy', 'Sweet', 'Sour',
  'Rich', 'Light', 'Crispy', 'Soft', 'Smoky', 'Oily',
  'Street Style', 'Cheap & Filling'
];

export default function CommunitySubmit() {
  const [form, setForm] = useState({
    spot_name: '', spot_type: '', area: '', address: '',
    description: '', must_try_dish: '', dish_description: '',
    approx_price: '', taste_tags: [], zomato_url: '', swiggy_url: '',
  });
  const [status, setStatus] = useState(null);
  const [message, setMessage] = useState('');

  const toggleTag = (tag) => {
    setForm(f => ({
      ...f,
      taste_tags: f.taste_tags.includes(tag)
        ? f.taste_tags.filter(t => t !== tag)
        : [...f.taste_tags, tag]
    }));
  };

  const handleSubmit = async () => {
    if (!form.spot_name || !form.area || !form.must_try_dish || !form.spot_type) {
      setMessage('Please fill all required fields.');
      return;
    }
    setStatus('loading');
    try {
      const res = await api.post('/community/submit', {
        ...form,
        approx_price: parseInt(form.approx_price) || 100,
        photo_urls: [],
      });
      setStatus('success');
      setMessage(res.data.message);
    } catch (err) {
      setStatus('error');
      setMessage(err.response?.data?.detail || 'Something went wrong.');
    }
  };

  if (status === 'success') return (
    <div style={{ minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24 }}>
      <div className="glass-card fade-in-up" style={{ padding: 40, textAlign: 'center', maxWidth: 460 }}>
        <span style={{ fontSize: 56 }}>🎉</span>
        <h2 style={{ fontSize: '1.6rem', fontWeight: 800, marginTop: 16, marginBottom: 12 }}>
          Spot submitted!
        </h2>
        <p style={{ color: 'var(--khao-text-secondary)', marginBottom: 24 }}>{message}</p>
        <button onClick={() => { setStatus(null); setMessage(''); setForm({
          spot_name: '', spot_type: '', area: '', address: '',
          description: '', must_try_dish: '', dish_description: '',
          approx_price: '', taste_tags: [], zomato_url: '', swiggy_url: '',
        }); }} className="glow-btn" style={{ padding: '12px 28px' }}>
          Add another spot
        </button>
      </div>
    </div>
  );

  return (
    <div style={{ maxWidth: 560, margin: '0 auto', padding: '40px 24px' }}>
      <div className="fade-in-up" style={{ textAlign: 'center', marginBottom: 36 }}>
        <span style={{ fontSize: 48 }}>📍</span>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 800, marginTop: 12 }}>
          Add a <span className="gradient-text">local spot</span>
        </h1>
        <p style={{ color: 'var(--khao-text-muted)', marginTop: 8, fontSize: '0.95rem' }}>
          Know a hidden gem? Share it with Delhi NCR.
        </p>
      </div>

      <div className="glass-card" style={{ padding: 28 }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <input
            placeholder="Spot name *"
            value={form.spot_name}
            onChange={e => setForm(f => ({ ...f, spot_name: e.target.value }))}
            className="khao-input"
          />

          <select
            value={form.spot_type}
            onChange={e => setForm(f => ({ ...f, spot_type: e.target.value }))}
            className="khao-input"
            style={{ cursor: 'pointer' }}
          >
            <option value="">Type of spot *</option>
            {SPOT_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
          </select>

          <input
            placeholder="Area / Locality *"
            value={form.area}
            onChange={e => setForm(f => ({ ...f, area: e.target.value }))}
            className="khao-input"
          />

          <input
            placeholder="Full address (optional)"
            value={form.address}
            onChange={e => setForm(f => ({ ...f, address: e.target.value }))}
            className="khao-input"
          />

          <textarea
            placeholder="Tell us about this place — what makes it special? *"
            value={form.description}
            onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
            className="khao-input"
            rows={3}
            style={{ resize: 'vertical' }}
          />

          <input
            placeholder="Must-try dish name *"
            value={form.must_try_dish}
            onChange={e => setForm(f => ({ ...f, must_try_dish: e.target.value }))}
            className="khao-input"
          />

          <textarea
            placeholder="How would you describe how that dish tastes?"
            value={form.dish_description}
            onChange={e => setForm(f => ({ ...f, dish_description: e.target.value }))}
            className="khao-input"
            rows={2}
            style={{ resize: 'vertical' }}
          />

          <input
            placeholder="Approx price per person (₹) *"
            type="number"
            value={form.approx_price}
            onChange={e => setForm(f => ({ ...f, approx_price: e.target.value }))}
            className="khao-input"
          />

          {/* Taste tags */}
          <div>
            <p style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: 10, color: 'var(--khao-text-secondary)' }}>
              Taste tags
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
              {TASTE_TAGS.map(tag => (
                <button
                  key={tag}
                  onClick={() => toggleTag(tag)}
                  className={`taste-tag ${form.taste_tags.includes(tag) ? 'active' : ''}`}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>

          <input
            placeholder="Zomato link (optional)"
            value={form.zomato_url}
            onChange={e => setForm(f => ({ ...f, zomato_url: e.target.value }))}
            className="khao-input"
          />

          <input
            placeholder="Swiggy link (optional)"
            value={form.swiggy_url}
            onChange={e => setForm(f => ({ ...f, swiggy_url: e.target.value }))}
            className="khao-input"
          />

          {message && status === 'error' && (
            <div style={{
              background: 'rgba(220, 38, 38, 0.1)',
              border: '1px solid rgba(220, 38, 38, 0.2)',
              borderRadius: 12,
              padding: '10px 16px',
              color: 'var(--khao-crimson)',
              fontSize: '0.9rem',
            }}>
              {message}
            </div>
          )}

          <button
            onClick={handleSubmit}
            className="glow-btn"
            disabled={status === 'loading'}
            style={{ width: '100%', padding: 14, marginTop: 8 }}
          >
            {status === 'loading' ? 'Submitting...' : '📍 Submit Spot'}
          </button>
        </div>
      </div>
    </div>
  );
}
