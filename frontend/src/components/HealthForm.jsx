import React, { useState } from 'react';

const HealthForm = () => {
  // 1. STATE: These are the "memory cells" of your component
  const [formData, setFormData] = useState({
    age: "",
    bmi: "",
    smoker: "no"
  });
  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState(null);

  // 2. THE HANDLER: This runs when the user clicks the button
  const handleAnalyze = () => {
    setIsCalculating(true);
    
    // Simulate the AI "thinking" for 2 seconds
    setTimeout(() => {
      setIsCalculating(false);
      setResult("Low Risk (Demo Mode)");
    }, 2000);
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-10 bg-slate-800/50 rounded-3xl border border-emerald-500/20 backdrop-blur-sm">
      <h2 className="text-3xl font-bold mb-8 text-white">Health Assessment</h2>
      
      <div className="space-y-6">
        {/* Input for Age */}
        <div className="flex flex-col gap-2">
          <label className="text-slate-400 font-medium">What is your Age?</label>
          <input 
            type="number" 
            placeholder="e.g. 21"
            className="bg-slate-900 border border-slate-700 p-4 rounded-xl text-white focus:border-emerald-500 outline-none transition-all"
            value={formData.age}
            onChange={(e) => setFormData({...formData, age: e.target.value})}
          />
        </div>

        {/* Input for BMI */}
        <div className="flex flex-col gap-2">
          <label className="text-slate-400 font-medium">Your BMI Score</label>
          <input 
            type="number" 
            placeholder="e.g. 24.5"
            className="bg-slate-900 border border-slate-700 p-4 rounded-xl text-white focus:border-emerald-500 outline-none transition-all"
            value={formData.bmi}
            onChange={(e) => setFormData({...formData, bmi: e.target.value})}
          />
        </div>

        {/* The Action Button */}
        <button 
          onClick={handleAnalyze}
          disabled={isCalculating}
          className="w-full bg-emerald-500 hover:bg-emerald-400 disabled:bg-slate-700 text-slate-950 font-black py-4 rounded-2xl text-lg transition-all"
        >
          {isCalculating ? "AI is Analyzing..." : "Predict My Risk"}
        </button>

        {/* 3. CONDITIONAL RENDERING: Shows the result only if it exists */}
        {result && (
          <div className="mt-6 p-4 bg-emerald-500/10 border border-emerald-500/50 rounded-xl text-emerald-400 text-center font-bold">
            Result: {result}
          </div>
        )}
      </div>
    </div>
  );
};

export default HealthForm;