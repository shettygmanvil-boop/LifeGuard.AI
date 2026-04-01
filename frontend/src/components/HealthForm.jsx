import React, { useState } from 'react';

const HealthForm = () => {
  const [formData, setFormData] = useState({
    // --- LIFESTYLE SECTION ---
    age: "", gender: "Male", height: "", weight: "",
    sleep_duration: "", physical_activity: "Moderate", 
    stress_level: 5, diet_quality: "Average",
    sugar_intake: "Low", salt_intake: "Low",
    smoking_habit: "Non-smoker", alcohol_consumption: "None",
    pregnancies: 0,
    // --- MEDICAL SECTION ---
    glucose: 100.0, bloodPressure: 80.0, skinThickness: 20.0,
    insulin: 79.0, bmi: 25.0, dpf: 0.5
  });

  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState(null);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="max-w-5xl mx-auto mt-10 p-10 bg-slate-800/40 rounded-3xl border border-emerald-500/20 backdrop-blur-md">
      <h2 className="text-4xl font-black mb-10 text-white text-center tracking-tight">Full Health Assessment</h2>
      
      <div className="space-y-12">
        {/* 1. PHYSICAL & BASIC */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
           <div className="flex flex-col gap-2">
            <label className="text-slate-400 text-sm font-bold">Age</label>
            <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none focus:border-emerald-500" value={formData.age} onChange={(e) => handleInputChange('age', e.target.value)} />
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-slate-400 text-sm font-bold">Height (cm)</label>
            <input type="number" step="0.1" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.height} onChange={(e) => handleInputChange('height', e.target.value)} />
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-slate-400 text-sm font-bold">Weight (kg)</label>
            <input type="number" step="0.1" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.weight} onChange={(e) => handleInputChange('weight', e.target.value)} />
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-slate-400 text-sm font-bold">Sleep (Hrs)</label>
            <input type="number" step="0.1" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.sleep_duration} onChange={(e) => handleInputChange('sleep_duration', e.target.value)} />
          </div>
        </div>

        {/* 2. HABITS & INTAKE */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex flex-col gap-2">
            <label className="text-slate-400 text-sm font-bold">Sugar Intake</label>
            <select className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.sugar_intake} onChange={(e) => handleInputChange('sugar_intake', e.target.value)}>
              <option>Low</option><option>Medium</option><option>High</option>
            </select>
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-slate-400 text-sm font-bold">Salt Intake</label>
            <select className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.salt_intake} onChange={(e) => handleInputChange('salt_intake', e.target.value)}>
              <option>Low</option><option>Medium</option><option>High</option>
            </select>
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-slate-400 text-sm font-bold">Stress Level (1-10)</label>
            <input type="range" min="1" max="10" className="mt-4 accent-emerald-500" value={formData.stress_level} onChange={(e) => handleInputChange('stress_level', e.target.value)} />
          </div>
        </div>

        {/* 3. CONSUMPTION */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex flex-col gap-2">
            <label className="text-slate-400 text-sm font-bold">Smoking Habit</label>
            <select className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.smoking_habit} onChange={(e) => handleInputChange('smoking_habit', e.target.value)}>
              <option>Non-smoker</option><option>Occasional</option><option>Regular</option>
            </select>
          </div>
          <div className="flex flex-col gap-2">
            <label className="text-slate-400 text-sm font-bold">Alcohol Consumption</label>
            <select className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.alcohol_consumption} onChange={(e) => handleInputChange('alcohol_consumption', e.target.value)}>
              <option>None</option><option>Occasional</option><option>Regular</option>
            </select>
          </div>
        </div>

        {/* 4. MEDICAL (Manvil's Core Params) */}
        <div className="pt-6 border-t border-slate-700/50">
          <h3 className="text-emerald-400 font-bold mb-6 italic">Medical Laboratory Data</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm">Glucose</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" value={formData.glucose} onChange={(e) => handleInputChange('glucose', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm">Insulin</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" value={formData.insulin} onChange={(e) => handleInputChange('insulin', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm">Pregnancies</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" value={formData.pregnancies} onChange={(e) => handleInputChange('pregnancies', e.target.value)} />
            </div>
          </div>
        </div>

        <button 
          onClick={() => { setIsCalculating(true); setTimeout(() => { setIsCalculating(false); setResult("Analysis Complete: Waiting for Backend Connection..."); }, 2000); }}
          className="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black py-5 rounded-2xl text-xl transition-all"
        >
          {isCalculating ? "AI is Processing..." : "Sync & Predict Risk"}
        </button>

        {result && <div className="p-4 bg-emerald-500/20 border border-emerald-500 rounded-xl text-emerald-400 text-center font-bold">{result}</div>}
      </div>
    </div>
  );
};

export default HealthForm;