import React, { useState } from 'react';

const HealthForm = () => {
  const [formData, setFormData] = useState({
    // Basic & Lifestyle
    age: "", gender: "Male", height_m: "", weight_kg: "",
    sleep_duration: "", physical_activity: "Moderate", 
    stress_level: 5, diet_quality: "Average",
    sugar_intake: "Low", salt_intake: "Low",
    smoking_habit: "Non-smoker", alcohol_consumption: "None",
    pregnancies: 0,
    // Medical Fields (AI Requirements)
    glucose: 100.0, bloodPressure: 80.0, skinThickness: 20.0,
    insulin: 79.0, bmi: 25.0, dpf: 0.5, is_diabetic: false
  });

  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState(null);

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="max-w-5xl mx-auto mt-10 p-10 bg-slate-800/40 rounded-3xl border border-emerald-500/20 backdrop-blur-md">
      <h2 className="text-4xl font-black mb-10 text-white text-center tracking-tight">Full Health Assessment</h2>
      
      <div className="space-y-12 text-left">
        {/* 1. PHYSICAL & BASIC */}
        <div>
          <h3 className="text-emerald-400 font-bold mb-6 flex items-center gap-2">Physical Metrics</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Height (Meters)</label>
              <input type="number" step="0.01" placeholder="e.g. 1.75" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none focus:border-emerald-500" 
                value={formData.height_m} onChange={(e) => handleInputChange('height_m', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Weight (kg)</label>
              <input type="number" step="0.1" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" 
                value={formData.weight_kg} onChange={(e) => handleInputChange('weight_kg', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Age</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" 
                value={formData.age} onChange={(e) => handleInputChange('age', e.target.value)} />
            </div>
             <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm font-bold">Sleep (Hrs)</label>
              <input type="number" step="0.5" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white outline-none" 
                value={formData.sleep_duration} onChange={(e) => handleInputChange('sleep_duration', e.target.value)} />
            </div>
          </div>
        </div>

        {/* 2. MEDICAL FIELDS (Manvil's AI Model) */}
        <div className="pt-6 border-t border-slate-700/50">
          <h3 className="text-emerald-400 font-bold mb-6 italic">Medical Parameters (AI Specific)</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm">Blood Pressure (mm Hg)</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" 
                value={formData.bloodPressure} onChange={(e) => handleInputChange('bloodPressure', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm">Skin Thickness (mm)</label>
              <input type="number" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" 
                value={formData.skinThickness} onChange={(e) => handleInputChange('skinThickness', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm">BMI</label>
              <input type="number" step="0.1" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" 
                value={formData.bmi} onChange={(e) => handleInputChange('bmi', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-slate-400 text-sm">Diabetes Pedigree Function</label>
              <input type="number" step="0.01" className="bg-slate-900 border border-slate-700 p-3 rounded-xl text-white" 
                value={formData.dpf} onChange={(e) => handleInputChange('dpf', e.target.value)} />
            </div>
            <div className="flex flex-col gap-2 justify-center">
              <label className="text-slate-400 text-sm mb-2">Already Diabetic?</label>
              <button 
                onClick={() => handleInputChange('is_diabetic', !formData.is_diabetic)}
                className={`p-3 rounded-xl font-bold transition-all ${formData.is_diabetic ? 'bg-red-500/20 text-red-400 border border-red-500' : 'bg-slate-900 border border-slate-700 text-slate-400'}`}
              >
                {formData.is_diabetic ? "YES" : "NO"}
              </button>
            </div>
          </div>
        </div>

        <button 
          onClick={() => { setIsCalculating(true); setTimeout(() => { setIsCalculating(false); setResult("Data Finalized. Ready for AI Sync!"); }, 2000); }}
          className="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black py-5 rounded-2xl text-xl transition-all shadow-lg shadow-emerald-500/20"
        >
          {isCalculating ? "Syncing with AI Model..." : "Analyze Full Profile"}
        </button>

        {result && <div className="p-4 bg-emerald-500/20 border border-emerald-500 rounded-xl text-emerald-400 text-center font-bold">{result}</div>}
      </div>
    </div>
  );
};

export default HealthForm;