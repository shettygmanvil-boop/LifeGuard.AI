import Navbar from "./components/Navbar";
import HealthForm from "./components/HealthForm";

function App() {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      <Navbar />
      
      {/* HERO SECTION */}
      <section className="pt-32 pb-20 px-6 text-center">
        <h1 className="text-6xl font-black tracking-tight mb-6">
          Your Personal <span className="text-emerald-400">AI Health Guard</span>
        </h1>
        <p className="text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
          Analyze your lifestyle habits and predict risks for Diabetes, Hypertension, and Obesity before they happen.
        </p>
        
        {/* 2. ADD THE FORM HERE */}
        <HealthForm /> 
      </section>

      {/* FEATURES GRID */}
      <section className="py-20 bg-slate-800/50 px-6">
        <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-8 text-center">
          <div className="p-8 bg-slate-900 border border-slate-700 rounded-3xl">
            <h3 className="text-2xl font-bold mb-4 text-emerald-400">ML Prediction</h3>
            <p className="text-slate-400">Advanced models trained on 10,000+ medical records.</p>
          </div>
          <div className="p-8 bg-slate-900 border border-slate-700 rounded-3xl">
            <h3 className="text-2xl font-bold mb-4 text-emerald-400">Instant Results</h3>
            <p className="text-slate-400">Get your risk assessment in less than 30 seconds.</p>
          </div>
          <div className="p-8 bg-slate-900 border border-slate-700 rounded-3xl">
            <h3 className="text-2xl font-bold mb-4 text-emerald-400">Health Privacy</h3>
            <p className="text-slate-400">Your data is encrypted and never shared with 3rd parties.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default App;