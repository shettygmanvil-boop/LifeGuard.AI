import React, { useState } from 'react';

const HealthForm = () => {
  // 'useState' is how React remembers what you type in a box
  const [age, setAge] = useState("");

  return (
    <div className="max-w-xl mx-auto mt-10 p-8 bg-slate-800 rounded-3xl border border-slate-700">
      <h2 className="text-2xl font-bold mb-6">Enter Your Details</h2>
      <div className="flex flex-col gap-4">
        <label className="text-slate-300">Your Age</label>
        <input 
          type="number" 
          className="bg-slate-900 border border-slate-700 p-4 rounded-xl text-white outline-none focus:border-emerald-500"
          value={age}
          onChange={(e) => setAge(e.target.value)} // Update the 'remembered' age
          placeholder="e.g. 25"
        />
        <button className="mt-4 bg-emerald-500 text-slate-950 font-bold py-3 rounded-xl hover:bg-emerald-400 transition-all">
          Analyze Risk
        </button>
      </div>
    </div>
  );
};

export default HealthForm;