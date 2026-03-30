import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './index.css';

const API_BASE = "http://localhost:8000/api";

function App() {
  const [data, setData] = useState([]);
  const [simActive, setSimActive] = useState(false);
  const [esp32Active, setEsp32Active] = useState(true);

  // Function to fetch latest data
  const fetchData = async () => {
    try {
      const res = await fetch(`${API_BASE}/sensor?limit=50`, { cache: 'no-store' });
      const json = await res.json();
      if (json.status === 'success') {
        // Reverse array because SQLite returns descending
        const chartData = json.data.reverse().map(item => ({
          time: new Date(item.created_at).toLocaleTimeString([], { hour12: false }),
          temp: item.temp,
          humid: item.humid
        }));
        setData(chartData);
      }
    } catch (e) {
      console.error("Failed to fetch data", e);
    }
  };

  // Poll exactly every 2 seconds
  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  // Control APIs
  const toggleFeature = async (feature, turnOn) => { // feature: 'simulator' | 'esp32'
    try {
      const endpoint = turnOn ? `/${feature}/on` : `/${feature}/off`;
      const res = await fetch(`${API_BASE}${endpoint}`, { method: 'POST' });
      if (res.ok) {
        if (feature === 'simulator') {
          setSimActive(turnOn);
          if (turnOn) setEsp32Active(false); // Auto toggle other
        }
        if (feature === 'esp32') {
          setEsp32Active(turnOn);
          if (turnOn) setSimActive(false); // Auto toggle other
        }
      } else {
        const errorData = await res.json();
        alert(`${errorData.detail || 'Unknown error occurred'}`);
      }
    } catch (e) {
      alert(`Cannot control ${feature}. Is backend running?`);
    }
  };

  const latest = data.length > 0 ? data[data.length - 1] : { temp: '--', humid: '--', time: '--' };

  return (
    <div className="dashboard-container">
      <header className="header">
        <div>
          <h1 style={{ margin: 0, fontSize: '2rem' }}>AIoT Dashboard 🌡️💧</h1>
          <p style={{ color: 'var(--text-muted)', margin: '0.5rem 0 0' }}>Real-time Dual Source Monitor</p>
        </div>
        
        <div className="controls-section">
          <div className="control-group">
            <div className="control-title">
              <span className="status-dot" style={{ backgroundColor: simActive ? 'var(--success)' : 'var(--danger)' }}></span>
              Software Simulator
            </div>
            <div className="toggle-buttons">
              <button className="btn btn-on" onClick={() => toggleFeature('simulator', true)} disabled={simActive}>ON</button>
              <button className="btn btn-off" onClick={() => toggleFeature('simulator', false)} disabled={!simActive}>OFF</button>
            </div>
          </div>

          <div className="control-group">
            <div className="control-title">
              <span className="status-dot" style={{ backgroundColor: esp32Active ? 'var(--success)' : 'var(--danger)' }}></span>
              ESP32 Hardware
            </div>
            <div className="toggle-buttons">
              <button className="btn btn-on" onClick={() => toggleFeature('esp32', true)} disabled={esp32Active}>ON</button>
              <button className="btn btn-off" onClick={() => toggleFeature('esp32', false)} disabled={!esp32Active}>OFF</button>
            </div>
          </div>
        </div>
      </header>

      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-label">Latest Temperature (°C)</div>
          <div className="metric-value" style={{ color: '#ef4444' }}>{typeof latest.temp === 'number' ? latest.temp.toFixed(2) : latest.temp}</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Latest Humidity (%)</div>
          <div className="metric-value" style={{ color: '#3b82f6' }}>{typeof latest.humid === 'number' ? latest.humid.toFixed(2) : latest.humid}</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Last Updated</div>
          <div className="metric-value" style={{ fontSize: '1.5rem', marginTop: '0.5rem' }}>{latest.time}</div>
        </div>
      </div>

      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis dataKey="time" stroke="var(--text-muted)" tick={{ fill: 'var(--text-muted)' }} />
            <YAxis stroke="var(--text-muted)" tick={{ fill: 'var(--text-muted)' }} />
            <Tooltip 
              contentStyle={{ backgroundColor: 'var(--card-bg)', border: 'none', borderRadius: '8px', color: '#fff' }}
              itemStyle={{ color: '#fff' }}
            />
            <Legend />
            <Line type="monotone" dataKey="temp" name="Temperature (°C)" stroke="#ef4444" strokeWidth={3} dot={false} activeDot={{ r: 6 }} />
            <Line type="monotone" dataKey="humid" name="Humidity (%)" stroke="#3b82f6" strokeWidth={3} dot={false} activeDot={{ r: 6 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default App;
