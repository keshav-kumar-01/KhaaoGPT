import { useState, useRef, useEffect } from 'react';
import api from '../api';
import RecommendationCard from '../components/RecommendationCard';

export default function Chat({ user }) {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      text: `Hey ${user.name || 'there'}! 🍛 Tell me what you're craving — a mood, a cuisine, a budget, or just "surprise me". I'll find the perfect match for your Taste DNA.`,
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const SUGGESTIONS = [
    '🌶️ Something spicy in Hauz Khas',
    '🥬 Veg under ₹200',
    '🍗 Best biryani near me',
    '🥟 Street food vibes',
    '🍝 Italian in Saket',
    '🔥 Surprise me!',
  ];

  const sendMessage = async (text) => {
    if (!text.trim()) return;
    setInput('');

    // Add user message
    setMessages(prev => [...prev, { type: 'user', text }]);
    setLoading(true);

    try {
      const res = await api.post('/chat', {
        message: text,
        area: user.area || null,
      });

      const recs = res.data.recommendations || [];
      const msg = res.data.message || '';

      setMessages(prev => [
        ...prev,
        { type: 'bot', text: msg, recommendations: recs },
      ]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { type: 'bot', text: 'Oops, something went wrong. Try again?' },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleRating = async (rec, rating) => {
    try {
      await api.post('/ratings', {
        dish_id: rec.dish_id,
        restaurant_id: '', // We don't have separate restaurant id in rec
        rating,
      });
      setMessages(prev => [
        ...prev,
        {
          type: 'bot',
          text: rating === 1
            ? "Loved it! 🎉 Your Taste DNA just got smarter."
            : rating === 3
            ? "Got it! We'll adjust your recommendations. 🔧"
            : "Noted! 📝",
        },
      ]);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{
      maxWidth: 800,
      margin: '0 auto',
      height: 'calc(100vh - 64px)',
      display: 'flex',
      flexDirection: 'column',
    }}>
      {/* Chat Header */}
      <div style={{
        padding: '18px 24px',
        borderBottom: '1px solid var(--khao-dark-border)',
        display: 'flex',
        alignItems: 'center',
        gap: 12,
      }}>
        <div style={{
          width: 40,
          height: 40,
          borderRadius: 12,
          background: 'linear-gradient(135deg, var(--khao-orange), var(--khao-gold))',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 20,
        }}>
          🍛
        </div>
        <div>
          <h3 style={{ fontSize: '1rem', fontWeight: 700, lineHeight: 1.2 }}>KhaoGPT</h3>
          <span style={{ fontSize: '0.78rem', color: 'var(--khao-green)' }}>● Online</span>
        </div>
      </div>

      {/* Messages */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '20px 24px',
        display: 'flex',
        flexDirection: 'column',
        gap: 16,
      }}>
        {messages.map((msg, i) => (
          <div key={i}>
            <div className={msg.type === 'user' ? 'msg-user' : 'msg-bot'}>
              {msg.text}
            </div>
            {msg.recommendations && msg.recommendations.length > 0 && (
              <div style={{ marginTop: 12, display: 'flex', flexDirection: 'column', gap: 12 }}>
                {msg.recommendations.map((rec, j) => (
                  <RecommendationCard
                    key={j}
                    rec={rec}
                    onRate={(rating) => handleRating(rec, rating)}
                    index={j}
                  />
                ))}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="typing-indicator">
            <span /><span /><span />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggestions */}
      {messages.length <= 1 && (
        <div style={{
          padding: '0 24px 12px',
          display: 'flex',
          gap: 8,
          flexWrap: 'wrap',
        }}>
          {SUGGESTIONS.map(s => (
            <button
              key={s}
              className="taste-tag"
              onClick={() => sendMessage(s.replace(/^[^\s]+\s/, ''))}
              style={{ cursor: 'pointer' }}
            >
              {s}
            </button>
          ))}
        </div>
      )}

      {/* Input Bar */}
      <div style={{
        padding: '16px 24px',
        borderTop: '1px solid var(--khao-dark-border)',
        display: 'flex',
        gap: 12,
      }}>
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage(input)}
          placeholder="Tell me what you're craving..."
          className="khao-input"
          style={{ flex: 1 }}
          disabled={loading}
        />
        <button
          onClick={() => sendMessage(input)}
          className="glow-btn"
          disabled={loading || !input.trim()}
          style={{
            padding: '12px 24px',
            opacity: input.trim() ? 1 : 0.5,
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
