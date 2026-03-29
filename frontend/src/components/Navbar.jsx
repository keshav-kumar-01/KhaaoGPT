import { Link, useLocation } from 'react-router-dom';

export default function Navbar({ user, onLogout }) {
  const location = useLocation();
  const isActive = (path) => location.pathname === path;

  return (
    <nav style={{
      position: 'sticky',
      top: 0,
      zIndex: 50,
      background: 'rgba(15, 15, 15, 0.85)',
      backdropFilter: 'blur(20px)',
      borderBottom: '1px solid var(--khao-dark-border)',
      padding: '0 24px',
    }}>
      <div style={{
        maxWidth: 1200,
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: 64,
      }}>
        {/* Logo */}
        <Link to="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: 10 }}>
          <span style={{ fontSize: 28 }}>🍛</span>
          <span className="gradient-text" style={{
            fontFamily: 'var(--font-heading)',
            fontSize: '1.4rem',
            fontWeight: 800,
            letterSpacing: '-0.5px',
          }}>
            KhaoGPT
          </span>
        </Link>

        {/* Nav Links */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 28 }}>
          {user ? (
            <>
              <Link to="/chat" className={`nav-link ${isActive('/chat') ? 'active' : ''}`}>
                💬 Chat
              </Link>
              <Link to="/profile" className={`nav-link ${isActive('/profile') ? 'active' : ''}`}>
                🧬 My DNA
              </Link>
              <Link to="/add-spot" className={`nav-link ${isActive('/add-spot') ? 'active' : ''}`}>
                📍 Add Spot
              </Link>
              {user.is_admin && (
                <Link to="/admin" className={`nav-link ${isActive('/admin') ? 'active' : ''}`}>
                  ⚙️ Admin
                </Link>
              )}
              <button onClick={onLogout} className="ghost-btn" style={{ padding: '8px 18px', fontSize: '0.85rem' }}>
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className={`nav-link ${isActive('/login') ? 'active' : ''}`}>
                Login
              </Link>
              <Link to="/register">
                <button className="glow-btn" style={{ padding: '8px 22px', fontSize: '0.85rem' }}>
                  Get Started
                </button>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
