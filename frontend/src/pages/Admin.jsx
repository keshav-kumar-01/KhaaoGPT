import { useState, useEffect } from 'react';
import api from '../api';

export default function Admin() {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(null);

  const fetchPending = async () => {
    try {
      const res = await api.get('/community/pending');
      setSubmissions(res.data.submissions || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchPending(); }, []);

  const handleApprove = async (id) => {
    setActionLoading(id);
    try {
      await api.post(`/community/${id}/approve`);
      setSubmissions(s => s.filter(sub => sub.id !== id));
    } catch (err) {
      alert(err.response?.data?.detail || 'Error approving');
    } finally {
      setActionLoading(null);
    }
  };

  const handleReject = async (id) => {
    const reason = prompt('Rejection reason:');
    if (!reason) return;
    setActionLoading(id);
    try {
      await api.post(`/community/${id}/reject`, { reason });
      setSubmissions(s => s.filter(sub => sub.id !== id));
    } catch (err) {
      alert(err.response?.data?.detail || 'Error rejecting');
    } finally {
      setActionLoading(null);
    }
  };

  if (loading) return (
    <div style={{ minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div className="typing-indicator"><span /><span /><span /></div>
    </div>
  );

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: '40px 24px' }}>
      <div className="fade-in-up" style={{ marginBottom: 32 }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 800 }}>
          ⚙️ Admin — <span className="gradient-text">Community Queue</span>
        </h1>
        <p style={{ color: 'var(--khao-text-muted)', marginTop: 8 }}>
          {submissions.length} pending submission{submissions.length !== 1 ? 's' : ''}
        </p>
      </div>

      {submissions.length === 0 ? (
        <div className="glass-card" style={{ padding: 40, textAlign: 'center' }}>
          <span style={{ fontSize: 48 }}>✅</span>
          <h3 style={{ marginTop: 16 }}>All clear!</h3>
          <p style={{ color: 'var(--khao-text-muted)', marginTop: 8 }}>
            No pending submissions to review.
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {submissions.map((sub, i) => (
            <div key={sub.id} className="glass-card fade-in-up" style={{
              padding: 24,
              animationDelay: `${i * 0.1}s`,
              opacity: 0,
            }}>
              {/* Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 14, flexWrap: 'wrap', gap: 8 }}>
                <div>
                  <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>{sub.spot_name}</h3>
                  <p style={{ fontSize: '0.85rem', color: 'var(--khao-text-muted)' }}>
                    {sub.spot_type} · {sub.area}
                  </p>
                </div>
                <span className="status-pending" style={{ padding: '4px 12px', borderRadius: 20, fontSize: '0.78rem', fontWeight: 600, alignSelf: 'flex-start' }}>
                  ⏳ Pending
                </span>
              </div>

              {/* Description */}
              {sub.description && (
                <p style={{ fontSize: '0.9rem', color: 'var(--khao-text-secondary)', marginBottom: 12, lineHeight: 1.5 }}>
                  "{sub.description}"
                </p>
              )}

              {/* Details */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: 8,
                marginBottom: 14,
                fontSize: '0.85rem',
              }}>
                <div style={{ background: 'var(--khao-dark)', borderRadius: 10, padding: '10px 14px' }}>
                  <span style={{ color: 'var(--khao-text-muted)' }}>Must-try: </span>
                  <span style={{ fontWeight: 600 }}>{sub.must_try_dish}</span>
                </div>
                <div style={{ background: 'var(--khao-dark)', borderRadius: 10, padding: '10px 14px' }}>
                  <span style={{ color: 'var(--khao-text-muted)' }}>Price: </span>
                  <span style={{ fontWeight: 600 }}>₹{sub.approx_price}</span>
                </div>
              </div>

              {/* Taste tags */}
              {sub.taste_tags && sub.taste_tags.length > 0 && (
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 14 }}>
                  {sub.taste_tags.map(t => (
                    <span key={t} className="taste-tag" style={{ cursor: 'default', fontSize: '0.75rem', padding: '4px 10px' }}>
                      {t}
                    </span>
                  ))}
                </div>
              )}

              {/* Dish description */}
              {sub.dish_description && (
                <div className="first-bite-card" style={{ marginBottom: 14 }}>
                  <p style={{ fontSize: '0.85rem', color: 'var(--khao-text-secondary)' }}>
                    {sub.dish_description}
                  </p>
                </div>
              )}

              {/* Action buttons */}
              <div style={{ display: 'flex', gap: 10 }}>
                <button
                  onClick={() => handleApprove(sub.id)}
                  disabled={actionLoading === sub.id}
                  className="glow-btn"
                  style={{ padding: '10px 24px', fontSize: '0.88rem' }}
                >
                  {actionLoading === sub.id ? '...' : '✅ Approve'}
                </button>
                <button
                  onClick={() => handleReject(sub.id)}
                  disabled={actionLoading === sub.id}
                  className="ghost-btn"
                  style={{
                    padding: '10px 24px',
                    fontSize: '0.88rem',
                    borderColor: 'var(--khao-crimson)',
                    color: 'var(--khao-crimson)',
                  }}
                >
                  ❌ Reject
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
