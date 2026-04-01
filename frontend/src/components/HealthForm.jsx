import React, { useState } from 'react';

const HealthForm = () => {
  const [formData, setFormData] = useState({
    // --- LIFESTYLE & BASIC (11 Params) ---
    age: "", 
    gender: "Male", 
    height: "", // Meters
    weight: "", // KG
    sleep_duration: "", 
    physical_activity: "Moderate", 
    stress_level: 5, 
    diet_quality: "Average",
    sugar_intake: "Low", 
    salt_intake: "Low",
    smoking_habit: "Non-smoker", 
    alcohol_consumption: "None",
    
    // --- MEDICAL & AI (7 Params) ---
    pregnancies: 0,
    glucose: 100.0, 
    bloodPressure: 80.0, 
    skinThickness: 20.0, 
    insulin: 79.0, 
    bmi: 25.0, 
    dpf: 0.5, // Diabetes Pedigree Function
    is_diabetic: false
  });

  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState(null);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="max-w-6xl mx-auto mt-10 p-10 bg-slate-800/40 rounded-3xl border border-emerald-500/20 backdrop-blur-md text-left">
      <h2 className="text-4xl font-black mb-10 text-white text-center tracking-tight">Comprehensive Health Profile</h2>
      
      <div className="space-y-10">
        
        {/* SECTION 1: PHYSICAL METRICS */}
        <div>
          <h3 className="text-emerald-400 font-bold mb-4 uppercase text-xs tracking-widest border-b border-emerald-500/20 pb-2">01. Physical Metrics</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Age</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white focus:border-emerald-500 outline-none" value={formData.age} onChange={(e) => handleInputChange('age', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Gender</label>
              <select className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" value={formData.gender} onChange={(e) => handleInputChange('gender', e.target.value)}>
                <option>Male</option><option>Female</option><option>Other</option>
              </select>
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Height (Meters)</label>
              <input type="number" step="0.01" placeholder="e.g. 1.75" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white focus:border-emerald-500 outline-none" value={formData.height} onChange={(e) => handleInputChange('height', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Weight (kg)</label>
              <input type="number" step="0.1" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.weight} onChange={(e) => handleInputChange('weight', e.target.value)} />
            </div>
          </div>
        </div>

        {/* SECTION 2: LIFESTYLE & HABITS */}
        <div>
          <h3 className="text-emerald-400 font-bold mb-4 uppercase text-xs tracking-widest border-b border-emerald-500/20 pb-2">02. Lifestyle & Habits</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Sleep Duration (Hrs)</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.sleep_duration} onChange={(e) => handleInputChange('sleep_duration', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Physical Activity</label>
              <select className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" value={formData.physical_activity} onChange={(e) => handleInputChange('physical_activity', e.target.value)}>
                <option>Sedentary</option><option>Moderate</option><option>Active</option>
              </select>
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Stress Level (1-10)</label>
              <input type="range" min="1" max="10" className="mt-4 accent-emerald-500" value={formData.stress_level} onChange={(e) => handleInputChange('stress_level', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Sugar Intake</label>
              <select className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" value={formData.sugar_intake} onChange={(e) => handleInputChange('sugar_intake', e.target.value)}>
                <option>Low</option><option>Medium</option><option>High</option>
              </select>
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Smoking Habit</label>
              <select className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" value={formData.smoking_habit} onChange={(e) => handleInputChange('smoking_habit', e.target.value)}>
                <option>Non-smoker</option><option>Occasional</option><option>Regular</option>
              </select>
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Alcohol Consumption</label>
              <select className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" value={formData.alcohol_consumption} onChange={(e) => handleInputChange('alcohol_consumption', e.target.value)}>
                <option>None</option><option>Occasional</option><option>Regular</option>
              </select>
            </div>
          </div>
        </div>

        {/* SECTION 3: MEDICAL DATA (AI REQUIREMENTS) */}
        <div>
          <h3 className="text-emerald-400 font-bold mb-4 uppercase text-xs tracking-widest border-b border-emerald-500/20 pb-2">03. Medical Laboratory Data</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Glucose</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.glucose} onChange={(e) => handleInputChange('glucose', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Blood Pressure</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.bloodPressure} onChange={(e) => handleInputChange('bloodPressure', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Skin Thickness (mm)</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.skinThickness} onChange={(e) => handleInputChange('skinThickness', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Insulin</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.insulin} onChange={(e) => handleInputChange('insulin', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">BMI</label>
              <input type="number" step="0.1" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.bmi} onChange={(e) => handleInputChange('bmi', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Diabetes Pedigree</label>
              <input type="number" step="0.01" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.dpf} onChange={(e) => handleInputChange('dpf', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Pregnancies</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" value={formData.pregnancies} onChange={(e) => handleInputChange('pregnancies', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2 justify-center">
              <label className="text-slate-400 text-sm font-bold mb-1">Diabetic?</label>
              <button 
                onClick={() => handleInputChange('is_diabetic', !formData.is_diabetic)}
                className={`p-3 rounded-xl font-bold transition-all border ${formData.is_diabetic ? 'bg-red-500/20 text-red-400 border-red-500' : 'bg-slate-900 border-slate-700 text-slate-500'}`}
              >
                {formData.is_diabetic ? "YES" : "NO"}
              </button>
            </div>
          </div>
        </div>

        <button 
          onClick={() => { setIsCalculating(true); setTimeout(() => { setIsCalculating(false); setResult("Analysis Complete: Dataset ready for AI Prediction."); }, 2000); }}
          className="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black py-5 rounded-2xl text-xl transition-all shadow-xl shadow-emerald-500/20"
        >
          {isCalculating ? "Syncing Full Dataset..." : "Predict Health Risk"}
        </button>

        {result && <div className="p-4 bg-emerald-500/10 border border-emerald-500/40 rounded-xl text-emerald-400 text-center font-bold animate-pulse">{result}</div>}
      </div>
    </div>
  );
};

export default HealthForm;