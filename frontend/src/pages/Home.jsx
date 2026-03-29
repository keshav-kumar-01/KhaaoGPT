import { Link } from 'react-router-dom';

const FEATURES = [
  { icon: '🧬', title: 'Taste DNA', desc: 'Your palate mapped across 7 axes in 90 seconds' },
  { icon: '🎯', title: 'Smart Matching', desc: 'Every dish scored 0-100 against your personal profile' },
  { icon: '👅', title: 'First Bite Preview', desc: 'Know exactly how it will taste before you order' },
  { icon: '💰', title: 'True Cost', desc: 'Real price including delivery + fees, not listed price' },
  { icon: '📍', title: 'Local Spots', desc: 'Community-powered hidden gems no app has listed' },
  { icon: '🔗', title: 'Order Redirect', desc: 'One tap to Zomato or Swiggy. We handle the brain work' },
];

const AREAS = [
  'Malviya Nagar', 'Hauz Khas', 'Saket', 'Connaught Place',
  'Old Delhi', 'Cyber City', 'Sector 29', 'Greater Kailash',
];

export default function Home({ user }) {
  return (
    <div style={{ overflow: 'hidden' }}>
      {/* ── Hero Section ── */}
      <section style={{
        minHeight: 'calc(100vh - 64px)',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        padding: '60px 24px',
        position: 'relative',
      }}>
        {/* Top badge */}
        <div className="fade-in-up" style={{
          background: 'rgba(255, 107, 53, 0.08)',
          border: '1px solid rgba(255, 107, 53, 0.2)',
          borderRadius: 30,
          padding: '8px 20px',
          fontSize: '0.85rem',
          color: 'var(--khao-orange)',
          fontWeight: 500,
          marginBottom: 32,
        }}>
          🚀 Taste Intelligence for Delhi NCR
        </div>

        {/* Main heading */}
        <h1 className="fade-in-up fade-in-up-delay-1" style={{
          fontFamily: 'var(--font-heading)',
          fontSize: 'clamp(2.5rem, 6vw, 4.5rem)',
          fontWeight: 900,
          lineHeight: 1.1,
          maxWidth: 800,
          marginBottom: 24,
          letterSpacing: '-1.5px',
        }}>
          Delhi has <span className="gradient-text">50,000</span> restaurants.
          <br />
          You eat from the same <span className="gradient-text">20</span>.
        </h1>

        {/* Subtitle */}
        <p className="fade-in-up fade-in-up-delay-2" style={{
          fontSize: 'clamp(1rem, 2vw, 1.25rem)',
          color: 'var(--khao-text-secondary)',
          maxWidth: 600,
          lineHeight: 1.6,
          marginBottom: 40,
        }}>
          KhaoGPT maps your palate, scores every dish against your taste, and
          finds the food your mouth was made for — including the street stall
          around the corner that no app has ever listed.
        </p>

        {/* CTA Buttons */}
        <div className="fade-in-up fade-in-up-delay-3" style={{ display: 'flex', gap: 16, flexWrap: 'wrap', justifyContent: 'center' }}>
          <Link to={user ? '/chat' : '/register'}>
            <button className="glow-btn" style={{ padding: '16px 36px', fontSize: '1.05rem' }}>
              {user ? '💬 Start Chatting' : '🍛 Find Your Food'}
            </button>
          </Link>
          {!user && (
            <Link to="/login">
              <button className="ghost-btn" style={{ padding: '15px 32px', fontSize: '1.05rem' }}>
                I have an account
              </button>
            </Link>
          )}
        </div>

        {/* Stats */}
        <div className="fade-in-up fade-in-up-delay-4" style={{
          display: 'flex',
          gap: 48,
          marginTop: 60,
          flexWrap: 'wrap',
          justifyContent: 'center',
        }}>
          {[
            { num: '10+', label: 'Restaurants' },
            { num: '25+', label: 'Dishes' },
            { num: '7', label: 'Taste Axes' },
            { num: '90s', label: 'Quiz Time' },
          ].map(s => (
            <div key={s.label} style={{ textAlign: 'center' }}>
              <div className="gradient-text" style={{ fontSize: '2rem', fontWeight: 800, fontFamily: 'var(--font-heading)' }}>
                {s.num}
              </div>
              <div style={{ fontSize: '0.85rem', color: 'var(--khao-text-muted)', marginTop: 4 }}>
                {s.label}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Features Grid ── */}
      <section style={{ padding: '80px 24px', maxWidth: 1200, margin: '0 auto' }}>
        <h2 style={{
          textAlign: 'center',
          fontSize: 'clamp(1.8rem, 4vw, 2.5rem)',
          marginBottom: 12,
          fontWeight: 800,
          letterSpacing: '-0.5px',
        }}>
          How it <span className="gradient-text">works</span>
        </h2>
        <p style={{
          textAlign: 'center',
          color: 'var(--khao-text-muted)',
          marginBottom: 48,
          fontSize: '1.05rem',
        }}>
          Not another food delivery app. A taste intelligence layer.
        </p>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: 20,
        }}>
          {FEATURES.map((f, i) => (
            <div key={f.title} className="glass-card fade-in-up" style={{
              padding: 28,
              animationDelay: `${i * 0.1}s`,
              opacity: 0,
              transition: 'transform 0.3s ease',
              cursor: 'default',
            }}
            onMouseEnter={e => e.currentTarget.style.transform = 'translateY(-4px)'}
            onMouseLeave={e => e.currentTarget.style.transform = 'translateY(0)'}
            >
              <div style={{ fontSize: '2rem', marginBottom: 12 }}>{f.icon}</div>
              <h3 style={{ fontSize: '1.15rem', marginBottom: 8, fontWeight: 700, color: 'var(--khao-text-primary)' }}>
                {f.title}
              </h3>
              <p style={{ color: 'var(--khao-text-secondary)', fontSize: '0.92rem', lineHeight: 1.5 }}>
                {f.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Areas Section ── */}
      <section style={{ padding: '60px 24px 100px', maxWidth: 1200, margin: '0 auto', textAlign: 'center' }}>
        <h2 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.5rem)', marginBottom: 12, fontWeight: 800 }}>
          Launching in <span className="gradient-text">Delhi NCR</span>
        </h2>
        <p style={{ color: 'var(--khao-text-muted)', marginBottom: 36, fontSize: '1.05rem' }}>
          Starting with South Delhi & Gurugram. Expanding fast.
        </p>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 12, justifyContent: 'center' }}>
          {AREAS.map(a => (
            <div key={a} className="taste-tag" style={{ cursor: 'default' }}>
              📍 {a}
            </div>
          ))}
        </div>
      </section>

      {/* ── Footer ── */}
      <footer style={{
        borderTop: '1px solid var(--khao-dark-border)',
        padding: '32px 24px',
        textAlign: 'center',
        color: 'var(--khao-text-muted)',
        fontSize: '0.85rem',
      }}>
        <span className="gradient-text" style={{ fontWeight: 700, fontFamily: 'var(--font-heading)' }}>KhaoGPT</span>
        {' '} · Taste Intelligence for Delhi NCR · Built with 🍛
      </footer>
    </div>
  );
}
