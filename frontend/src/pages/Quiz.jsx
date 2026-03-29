import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

export default function Quiz() {
  const [questions, setQuestions] = useState([]);
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    api.get('/taste-dna/quiz').then(res => {
      setQuestions(res.data.questions);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const handleSelect = (option) => {
    setSelected(option);
  };

  const handleNext = () => {
    if (!selected) return;
    const q = questions[current];
    const newAnswers = { ...answers, [q.id]: selected };
    setAnswers(newAnswers);
    setSelected(null);

    if (current < questions.length - 1) {
      setCurrent(c => c + 1);
    } else {
      // Submit
      submitQuiz(newAnswers);
    }
  };

  const submitQuiz = async (allAnswers) => {
    setSubmitting(true);
    try {
      const formatted = Object.entries(allAnswers).map(([qId, answer]) => ({
        question_id: parseInt(qId),
        answer: answer,
      }));
      const res = await api.post('/taste-dna/quiz', { answers: formatted });
      setResult(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return (
    <div style={{ minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div className="typing-indicator">
        <span /><span /><span />
      </div>
    </div>
  );

  if (result) {
    const p = result.profile;
    return (
      <div style={{ minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24 }}>
        <div className="glass-card fade-in-up" style={{ padding: 40, maxWidth: 500, width: '100%', textAlign: 'center' }}>
          <span style={{ fontSize: 56 }}>🧬</span>
          <h2 style={{ fontSize: '1.8rem', fontWeight: 800, marginTop: 16, marginBottom: 8 }}>
            Your <span className="gradient-text">Taste DNA</span> is ready!
          </h2>
          <p style={{ color: 'var(--khao-text-muted)', marginBottom: 28 }}>
            Here's how your palate maps out:
          </p>

          {/* DNA Axes */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 32 }}>
            {[
              { label: '🌶️ Heat Ceiling', value: p.heat_ceiling },
              { label: '🍯 Sweet Tolerance', value: p.sweet_tolerance },
              { label: '🍋 Acid Affinity', value: p.acid_affinity },
              { label: '🍖 Umami Affinity', value: p.umami_affinity },
              { label: '🧈 Fat Palate', value: p.fat_palate },
              { label: '☕ Bitter Tolerance', value: p.bitter_tolerance },
            ].map(axis => (
              <div key={axis.label}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4, fontSize: '0.88rem' }}>
                  <span>{axis.label}</span>
                  <span className="gradient-text" style={{ fontWeight: 700 }}>{axis.value}/10</span>
                </div>
                <div style={{
                  height: 6,
                  background: 'var(--khao-dark-surface)',
                  borderRadius: 3,
                  overflow: 'hidden',
                }}>
                  <div style={{
                    height: '100%',
                    width: `${(axis.value / 10) * 100}%`,
                    background: 'linear-gradient(90deg, var(--khao-orange), var(--khao-gold))',
                    borderRadius: 3,
                    transition: 'width 1s ease',
                  }} />
                </div>
              </div>
            ))}
          </div>

          <button onClick={() => navigate('/chat')} className="glow-btn" style={{ width: '100%', padding: 14 }}>
            💬 Start Discovering Food
          </button>
        </div>
      </div>
    );
  }

  if (submitting) return (
    <div style={{ minHeight: '80vh', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 16 }}>
      <div className="typing-indicator">
        <span /><span /><span />
      </div>
      <p style={{ color: 'var(--khao-text-muted)' }}>Building your Taste DNA...</p>
    </div>
  );

  const q = questions[current];
  const progress = ((current) / questions.length) * 100;

  return (
    <div style={{ minHeight: 'calc(100vh - 64px)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24 }}>
      <div className="glass-card fade-in-up" style={{ padding: 40, maxWidth: 560, width: '100%' }}>
        {/* Progress bar */}
        <div style={{ marginBottom: 32 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, fontSize: '0.85rem' }}>
            <span style={{ color: 'var(--khao-text-muted)' }}>Question {current + 1} of {questions.length}</span>
            <span className="gradient-text" style={{ fontWeight: 600 }}>{Math.round(progress)}%</span>
          </div>
          <div style={{ height: 4, background: 'var(--khao-dark-surface)', borderRadius: 2 }}>
            <div style={{
              height: '100%',
              width: `${progress}%`,
              background: 'linear-gradient(90deg, var(--khao-orange), var(--khao-gold))',
              borderRadius: 2,
              transition: 'width 0.4s ease',
            }} />
          </div>
        </div>

        {/* Question */}
        <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: 28, lineHeight: 1.3 }}>
          {q.question}
        </h2>

        {/* Options */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 28 }}>
          {q.options.map(opt => (
            <div
              key={opt}
              className={`quiz-option ${selected === opt ? 'selected' : ''}`}
              onClick={() => handleSelect(opt)}
            >
              {opt}
            </div>
          ))}
        </div>

        {/* Next button */}
        <button
          onClick={handleNext}
          className="glow-btn"
          disabled={!selected}
          style={{
            width: '100%',
            padding: 14,
            opacity: selected ? 1 : 0.5,
            cursor: selected ? 'pointer' : 'not-allowed',
          }}
        >
          {current < questions.length - 1 ? 'Next →' : '🧬 Build My Taste DNA'}
        </button>
      </div>
    </div>
  );
}
