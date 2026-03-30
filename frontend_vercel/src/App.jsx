import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './index.css';

function App() {
  const [data, setData] = useState([]);
  const [simActive, setSimActive] = useState(true);

  // Generate simulated data every 5 seconds
  useEffect(() => {
    let interval;
    if (simActive) {
      interval = setInterval(() => {
        const temp = parseFloat((Math.random() * (35.0 - 20.0) + 20.0).toFixed(2));
        const humid = parseFloat((Math.random() * (80.0 - 40.0) + 40.0).toFixed(2));
        const now = new Date().toLocaleTimeString([], { hour12: false });
        
        setData(prev => {
          const newData = [...prev, { time: now, temp, humid }];
          // Keep the last 50 data points for the chart
          return newData.length > 50 ? newData.slice(newData.length - 50) : newData;
        });
      }, 2000); // 2 seconds interval
    }
    return () => clearInterval(interval);
  }, [simActive]);

  const latest = data.length > 0 ? data[data.length - 1] : { temp: '--', humid: '--', time: '--' };

  return (
    <div className="dashboard-container">
      <header className="header">
        <div>
          <h1 style={{ margin: 0, fontSize: '2rem' }}>AIoT Dashboard ☁️</h1>
          <p style={{ color: 'var(--text-muted)', margin: '0.5rem 0 0' }}>Vercel Cloud Simulator Demo</p>
        </div>
        
        <div className="controls-section">
          <div className="control-group">
            <div className="control-title">
              <span className="status-dot" style={{ backgroundColor: simActive ? 'var(--success)' : 'var(--danger)' }}></span>
              Cloud Simulator
            </div>
            <div className="toggle-buttons">
              <button className="btn btn-on" onClick={() => setSimActive(true)} disabled={simActive}>ON</button>
              <button className="btn btn-off" onClick={() => setSimActive(false)} disabled={!simActive}>OFF</button>
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
