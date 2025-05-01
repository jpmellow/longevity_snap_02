import React, { useState } from 'react';


const HealthCoachInterface = () => {
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState('gpt-4');
  const [coachResponse, setCoachResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleStartChat = async () => {
    setIsLoading(true);
    setError('');
    setCoachResponse('');

    const assessment = {
      age: 42,
      gender: 'male',
      sleep_hours: 7,
      nutrition_score: 85,
      stress_level: 'moderate',
      exercise_minutes_week: 150,
      daily_water_liters: 2.5
    };

    const prompt = `Based on my health metrics, what specific actions should I take to improve my longevity and overall well-being?`;

    try {
      const response = await fetch('http://localhost:8000/chat-coach/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          assessment,
          prompt,
          api_key: apiKey,
          llm_model: model,
        }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to get coaching advice');
      }
      
      if (data.error) {
        setError(`Note: ${data.note} (${data.error})`);
      }
      
      setCoachResponse(data.response);
    } catch (error) {
      setError('Oops! The coach is taking a break. Please try again in a moment.');
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="health-coach-container">
      <div className="input-section">
        <div className="api-input">
          <label htmlFor="apiKey">Enter your API Key:</label>
          <input
            type="password"
            id="apiKey"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />
        </div>
        
        <div className="model-select">
          <label htmlFor="model">Select LLM Model:</label>
          <select
            id="model"
            value={model}
            onChange={(e) => setModel(e.target.value)}
          >
            <option value="gpt-4">OpenAI GPT-4</option>
            <option value="gpt-3.5-turbo">OpenAI GPT-3.5 Turbo</option>
            <option value="claude-3">Anthropic Claude 3</option>
          </select>
        </div>

        <button 
          onClick={handleStartChat}
          disabled={isLoading || !apiKey}
          className={isLoading ? 'loading' : ''}
        >
          {isLoading ? 'Getting Advice...' : 'Start Chat'}
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {coachResponse && (
        <div className="coach-response">
          <h3>Coach says:</h3>
          <div className="response-content">
            {coachResponse.split('\n').map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default HealthCoachInterface;
