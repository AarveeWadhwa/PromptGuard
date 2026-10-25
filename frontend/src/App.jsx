import { useState } from 'react';

const API_URL = import.meta.env.VITE_API_URL || 'https://promptguard-mp7n.onrender.com';

export default function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function analyze() {
    if (!text.trim()) return;
    setLoading(true); setError('');
    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      if (!response.ok) throw new Error('Backend request failed');
      setResult(await response.json());
    } catch (err) {
      setError('Could not connect to PromptGuard backend. Make sure FastAPI is running.');
    } finally { setLoading(false); }
  }

  return (
    <main className="page">
      <section className="hero">
        <div className="badge">NLP SECURITY • EXPLAINABLE AI</div>
        <h1><span>Prompt</span>Guard</h1>
        <p>Detect prompt injection and jailbreak attacks with an explainable NLP classifier.</p>
      </section>

      <section className="card">
        <label htmlFor="prompt">Enter a prompt</label>
        <textarea id="prompt" value={text} onChange={e => setText(e.target.value)}
          placeholder="Paste a prompt here for analysis..." />
        <button onClick={analyze} disabled={loading || !text.trim()}>
          {loading ? 'Analyzing...' : 'Analyze Prompt'}
        </button>
      </section>

      {error && <div className="error">{error}</div>}

      {result && (
        <section className="result card">
          <div className={`label ${result.label === 'prompt_injection' ? 'danger' : 'safe'}`}>
            {result.label === 'prompt_injection' ? '⚠ PROMPT INJECTION' : '✓ BENIGN'}
          </div>
          <div className="confidence">Confidence: <strong>{(result.confidence * 100).toFixed(1)}%</strong></div>
          <div className="bar"><div style={{width: `${result.confidence * 100}%`}} /></div>
          <h2>Detected markers</h2>
          {result.markers.length === 0 ? <p className="muted">No configured markers detected.</p> :
            result.markers.map((m, i) => (
              <div className="marker" key={i}>
                <strong>{m.type.replaceAll('_', ' ')}</strong>
                <span>“{m.text}”</span>
                <small>{m.explanation}</small>
              </div>
            ))}
          <h2>Explanation</h2>
          <p>{result.explanation}</p>
          <small className="muted">Model: {result.model}</small>
        </section>
      )}
    </main>
  );
}
