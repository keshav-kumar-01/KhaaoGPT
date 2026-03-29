import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Chat from './pages/Chat';
import Profile from './pages/Profile';
import Quiz from './pages/Quiz';
import CommunitySubmit from './pages/CommunitySubmit';
import Admin from './pages/Admin';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem('khao_user');
    const token = localStorage.getItem('khao_token');
    if (stored && token) {
      setUser(JSON.parse(stored));
    }
    setLoading(false);
  }, []);

  const handleLogin = (userData, token) => {
    localStorage.setItem('khao_user', JSON.stringify(userData));
    localStorage.setItem('khao_token', token);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('khao_user');
    localStorage.removeItem('khao_token');
    setUser(null);
  };

  if (loading) return null;

  return (
    <BrowserRouter>
      <div style={{ position: 'relative', minHeight: '100vh' }}>
        <div className="particles-bg" />
        <div style={{ position: 'relative', zIndex: 1 }}>
          <Navbar user={user} onLogout={handleLogout} />
          <Routes>
            <Route path="/" element={<Home user={user} />} />
            <Route path="/login" element={
              user ? <Navigate to="/chat" /> : <Login onLogin={handleLogin} />
            } />
            <Route path="/register" element={
              user ? <Navigate to="/chat" /> : <Register onLogin={handleLogin} />
            } />
            <Route path="/chat" element={
              user ? <Chat user={user} /> : <Navigate to="/login" />
            } />
            <Route path="/quiz" element={
              user ? <Quiz user={user} /> : <Navigate to="/login" />
            } />
            <Route path="/profile" element={
              user ? <Profile user={user} /> : <Navigate to="/login" />
            } />
            <Route path="/add-spot" element={
              user ? <CommunitySubmit user={user} /> : <Navigate to="/login" />
            } />
            <Route path="/admin" element={
              user?.is_admin ? <Admin /> : <Navigate to="/" />
            } />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
