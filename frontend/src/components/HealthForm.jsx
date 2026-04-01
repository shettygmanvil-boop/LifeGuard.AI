import React, { useState } from 'react';

const HealthForm = () => {
  const [formData, setFormData] = useState({
    // Basic & Lifestyle
    age: "", gender: "Male", height: "", weight: "",
    sleep_duration: "", physical_activity: "Moderate", 
    stress_level: 5, diet_quality: "Average",
    sugar_intake: "Low", salt_intake: "Low",
    smoking_habit: "Non-smoker", alcohol_consumption: "None",
    pregnancies: 0,
    // Medical Fields
    glucose: 100.0, bloodPressure: 80.0, skinThickness: 20.0,
    insulin: 79.0, bmi: 25.0, dpf: 0.5
  });

  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState(null);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="max-w-4xl mx-auto mt-10 p-10 bg-slate-800/40 rounded-3xl border border-emerald-500/20 backdrop-blur-md">
      <h2 className="text-4xl font-black mb-10 text-white text-center tracking-tight">Full Health Assessment</h2>
      
      <div className="space-y-12">
        {/* SECTION 1: BASIC & LIFESTYLE */}
        <div>
          <h3 className="text-emerald-400 font-bold mb-6 flex items-center gap-2">
            <span className="bg-emerald-500/20 p-2 rounded-lg text-xs">01</span> Basic & Lifestyle
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Age */}
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-semibold">Age</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none focus:border-emerald-500" 
                value={formData.age} onChange={(e) => handleInputChange('age', e.target.value)} />
            </div>
            {/* Gender Dropdown */}
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-semibold">Gender</label>
              <select className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none focus:border-emerald-500"
                value={formData.gender} onChange={(e) => handleInputChange('gender', e.target.value)}>
                <option>Male</option><option>Female</option><option>Other</option>
              </select>
            </div>
            {/* Smoking Dropdown */}
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-semibold">Smoking Habit</label>
              <select className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none focus:border-emerald-500"
                value={formData.smoking_habit} onChange={(e) => handleInputChange('smoking_habit', e.target.value)}>
                <option>Non-smoker</option><option>Occasional</option><option>Regular</option>
              </select>
            </div>
          </div>
        </div>

        {/* SECTION 2: MEDICAL STATS (For Manvil's Model) */}
        <div>
          <h3 className="text-emerald-400 font-bold mb-6 flex items-center gap-2">
            <span className="bg-emerald-500/20 p-2 rounded-lg text-xs">02</span> Medical Parameters (AI Model)
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm">Glucose</label>
              <input type="number" step="0.1" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" 
                value={formData.glucose} onChange={(e) => handleInputChange('glucose', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm">Insulin</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" 
                value={formData.insulin} onChange={(e) => handleInputChange('insulin', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm">BMI</label>
              <input type="number" step="0.1" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" 
                value={formData.bmi} onChange={(e) => handleInputChange('bmi', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm">Pregnancies</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" 
                value={formData.pregnancies} onChange={(e) => handleInputChange('pregnancies', e.target.value)} />
            </div>
          </div>
        </div>

        <button 
          onClick={() => { setIsCalculating(true); setTimeout(() => { setIsCalculating(false); setResult("Ready for API Connection!"); }, 1500); }}
          className="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black py-5 rounded-2xl text-xl transition-all"
        >
          {isCalculating ? "AI Processing..." : "Generate Risk Profile"}
        </button>

        {result && <div className="text-center text-emerald-400 font-bold animate-pulse">{result}</div>}
      </div>
    </div>
  );
};

export default HealthForm;