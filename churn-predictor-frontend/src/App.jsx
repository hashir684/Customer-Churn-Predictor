import { useState } from 'react';
import axios from 'axios';
import './App.css';

export default function App() {
  const [formData, setFormData] = useState({
    tenure: 14,
    monthly_charges: 80.12,
    total_charges: 500,
    has_partner: 'no',
    has_dependents: 'no',
    internet_type: 'dsl',
    contract_type: 'month_to_month'
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: isNaN(value) ? value : parseFloat(value)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(
        'http://localhost:8000/predict',
        formData
      );
      setResult(response.data);
      setLastUpdated(new Date().toLocaleTimeString());
    } catch (err) {
      setError(err.response?.data?.error || 'Error connecting to API');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData({
      tenure: 14,
      monthly_charges: 80.12,
      total_charges: 500,
      has_partner: 'no',
      has_dependents: 'no',
      internet_type: 'dsl',
      contract_type: 'month_to_month'
    });
    setResult(null);
    setError(null);
    setLastUpdated(null);
  };

  return (
    <div className="app-wrapper">
      {/* HEADER */}
      <div className="app-header">
        <div className="header-content">
          <h1>👥 Predict Customer Churn</h1>
          <p>AI-powered retention analytics to identify customers at risk before they leave.</p>
        </div>
      </div>

      {/* MAIN LAYOUT */}
      <div className="app-container">
        {/* LEFT: FORM */}
        <div className="form-panel">
          <div className="panel-header">
            <h2>👤 Customer Details</h2>
            <p>Enter customer information to get churn prediction</p>
          </div>

          <form onSubmit={handleSubmit}>
            {/* Row 1: Numbers with Icons */}
            <div className="form-row three-cols">
              <div className="form-group">
                <div className="label-icon">
                  <span>📅</span>
                  <label>Tenure</label>
                </div>
                <input
                  type="number"
                  name="tenure"
                  value={formData.tenure}
                  onChange={handleInputChange}
                  min="0"
                  max="72"
                />
                <div className="helper-text">0-72 months</div>
              </div>

              <div className="form-group">
                <div className="label-icon">
                  <span>💵</span>
                  <label>Monthly Bill</label>
                </div>
                <input
                  type="number"
                  name="monthly_charges"
                  value={formData.monthly_charges}
                  onChange={handleInputChange}
                  min="0"
                  step="0.01"
                />
                <div className="helper-text">USD</div>
              </div>

              <div className="form-group">
                <div className="label-icon">
                  <span>💰</span>
                  <label>Total Paid</label>
                </div>
                <input
                  type="number"
                  name="total_charges"
                  value={formData.total_charges}
                  onChange={handleInputChange}
                  min="0"
                  step="0.01"
                />
                <div className="helper-text">USD</div>
              </div>
            </div>

            {/* Row 2: Yes/No Options */}
            <div className="form-row two-cols">
              <div className="form-group">
                <div className="label-icon">
                  <span>👫</span>
                  <label>Has Partner?</label>
                </div>
                <div className="radio-group">
                  <label className="radio-option">
                    <input
                      type="radio"
                      name="has_partner"
                      value="yes"
                      checked={formData.has_partner === 'yes'}
                      onChange={handleInputChange}
                    />
                    Yes
                  </label>
                  <label className="radio-option">
                    <input
                      type="radio"
                      name="has_partner"
                      value="no"
                      checked={formData.has_partner === 'no'}
                      onChange={handleInputChange}
                    />
                    No
                  </label>
                </div>
              </div>

              <div className="form-group">
                <div className="label-icon">
                  <span>👨‍👩‍👧‍👦</span>
                  <label>Has Dependents?</label>
                </div>
                <div className="radio-group">
                  <label className="radio-option">
                    <input
                      type="radio"
                      name="has_dependents"
                      value="yes"
                      checked={formData.has_dependents === 'yes'}
                      onChange={handleInputChange}
                    />
                    Yes
                  </label>
                  <label className="radio-option">
                    <input
                      type="radio"
                      name="has_dependents"
                      value="no"
                      checked={formData.has_dependents === 'no'}
                      onChange={handleInputChange}
                    />
                    No
                  </label>
                </div>
              </div>
            </div>

            {/* Row 3: Dropdowns */}
            <div className="form-row two-cols">
              <div className="form-group">
                <div className="label-icon">
                  <span>📡</span>
                  <label>Internet Type</label>
                </div>
                <select
                  name="internet_type"
                  value={formData.internet_type}
                  onChange={handleInputChange}
                >
                  <option value="dsl">DSL</option>
                  <option value="fiber">Fiber Optic</option>
                  <option value="no">No Internet</option>
                </select>
              </div>

              <div className="form-group">
                <div className="label-icon">
                  <span>📋</span>
                  <label>Contract Type</label>
                </div>
                <select
                  name="contract_type"
                  value={formData.contract_type}
                  onChange={handleInputChange}
                >
                  <option value="month_to_month">Month-to-Month</option>
                  <option value="one_year">One Year</option>
                  <option value="two_year">Two Years</option>
                </select>
              </div>
            </div>

            {/* BUTTONS */}
            <div className="button-group">
              <button type="submit" disabled={loading} className="btn-primary">
                🚀 {loading ? 'Predicting...' : 'Predict Churn'}
              </button>
              <button type="button" onClick={handleReset} className="btn-secondary">
                ↻ Reset
              </button>
            </div>
          </form>

          {error && (
            <div className="error-box">
              <div className="error-title">❌ Error</div>
              <div className="error-message">{error}</div>
            </div>
          )}
        </div>

        {/* RIGHT: RESULTS */}
        <div className="result-panel">
          <div className="panel-header">
            <h2>📊 Prediction Insights</h2>
            <p>AI prediction results and recommendations</p>
            {result && (
              <div className="status-badge">
                <span className="status-dot"></span>
                Analysis Complete
              </div>
            )}
          </div>

          {!result ? (
            <div className="empty-state">
              <div className="empty-state-icon">🎯</div>
              <div className="empty-state-text">
                Enter customer information and click Predict to see analysis results
              </div>
            </div>
          ) : (
            <div className="results-container">
              {/* Churn Probability */}
              <div className="result-card">
                <div className="result-card-header">
                  <div className="result-icon">📈</div>
                  <div className="result-info">
                    <div className="result-label">Churn Probability</div>
                    <div className="result-value">
                      {result.churn_probability}%
                    </div>
                  </div>
                  <div className="result-status">
                    {result.churn_probability < 25 && (
                      <span className="status-very-low">Very Low</span>
                    )}
                    {result.churn_probability >= 25 && result.churn_probability < 50 && (
                      <span className="status-low">Low</span>
                    )}
                    {result.churn_probability >= 50 && result.churn_probability < 75 && (
                      <span className="status-high">High</span>
                    )}
                    {result.churn_probability >= 75 && (
                      <span className="status-very-high">Very High</span>
                    )}
                  </div>
                </div>
              </div>

              {/* Risk Level */}
              <div className="result-card">
                <div className="result-card-header">
                  <div className="result-icon">🛡️</div>
                  <div className="result-info">
                    <div className="result-label">Risk Level</div>
                    {result.risk_level === 'HIGH' && (
                      <div className="result-value risk-high-text">HIGH RISK</div>
                    )}
                    {result.risk_level === 'MEDIUM' && (
                      <div className="result-value risk-medium-text">MEDIUM RISK</div>
                    )}
                    {result.risk_level === 'LOW' && (
                      <div className="result-value risk-low-text">LOW RISK</div>
                    )}
                  </div>
                  <div className="result-status">
                    {result.risk_level === 'HIGH' && (
                      <span className="status-dangerous">Dangerous</span>
                    )}
                    {result.risk_level === 'MEDIUM' && (
                      <span className="status-caution">Caution</span>
                    )}
                    {result.risk_level === 'LOW' && (
                      <span className="status-safe">Safe</span>
                    )}
                  </div>
                </div>
              </div>

              {/* Confidence */}
              <div className="result-card">
                <div className="result-card-header">
                  <div className="result-icon">🎯</div>
                  <div className="result-info">
                    <div className="result-label">Model Confidence</div>
                    <div className="result-value">
                      {result.confidence}%
                    </div>
                  </div>
                  <div className="result-status">
                    {result.confidence >= 90 && (
                      <span className="status-high-confidence">High Confidence</span>
                    )}
                    {result.confidence >= 75 && result.confidence < 90 && (
                      <span className="status-medium-confidence">Medium Confidence</span>
                    )}
                    {result.confidence < 75 && (
                      <span className="status-low-confidence">Low Confidence</span>
                    )}
                  </div>
                </div>
              </div>

              {/* Prediction */}
              <div className="result-card">
                <div className="result-card-header">
                  <div className="result-icon">
                    {result.prediction === 'CHURN' ? '❌' : '✓'}
                  </div>
                  <div className="result-info">
                    <div className="result-label">Prediction</div>
                    <div className={`result-value ${result.prediction === 'CHURN' ? 'prediction-churn' : 'prediction-stay'}`}>
                      {result.prediction === 'CHURN' ? 'Will CHURN' : 'Will STAY'}
                    </div>
                  </div>
                  <div className="result-status">
                    {result.prediction === 'CHURN' ? (
                      <span className="status-negative">Negative</span>
                    ) : (
                      <span className="status-positive">Positive</span>
                    )}
                  </div>
                </div>
              </div>

              {/* Recommendation */}
              <div className="result-card">
                <div className="result-card-header">
                  <div className="result-icon">💡</div>
                  <div className="result-info full-width">
                    <div className="result-label">Recommendation</div>
                    <div className="result-text">
                      {result.risk_level === 'LOW' &&
                        'No action needed - customer is satisfied'}
                      {result.risk_level === 'MEDIUM' &&
                        'Monitor customer and plan engagement strategy'}
                      {result.risk_level === 'HIGH' &&
                        'URGENT: Contact customer immediately with retention offer'}
                    </div>
                  </div>
                  <div className="result-status">
                    {result.risk_level === 'LOW' && (
                      <span className="status-required">No Action Required</span>
                    )}
                    {result.risk_level === 'MEDIUM' && (
                      <span className="status-monitor">Monitor</span>
                    )}
                    {result.risk_level === 'HIGH' && (
                      <span className="status-urgent">Urgent</span>
                    )}
                  </div>
                </div>
              </div>

            </div>
          )}
        </div>
      </div>
    </div>
  );
}