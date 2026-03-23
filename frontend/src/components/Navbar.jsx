import React from 'react';

const Navbar = () => {
  return (
    <nav className="bg-slate-900 border-b border-slate-800 px-6 py-4 flex justify-between items-center sticky top-0 z-50">
      {/* 1. LOGO SECTION */}
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-emerald-500 rounded-lg flex items-center justify-center font-bold text-white italic">
          L
        </div>
        <span className="text-xl font-bold text-white">
          LifeGuard <span className="text-emerald-400">AI</span>
        </span>
      </div>
      
      {/* 2. LINKS SECTION */}
      <div className="hidden md:flex gap-8 text-slate-300 font-medium">
        <a href="#" className="hover:text-emerald-400 transition-colors">Home</a>
        <a href="#" className="hover:text-emerald-400 transition-colors">Features</a>
        <a href="#" className="hover:text-emerald-400 transition-colors">About</a>
      </div>

      {/* 3. BUTTON SECTION */}
      <button className="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold py-2 px-5 rounded-full transition-all text-sm">
        Google Login
      </button>
    </nav>
  );
};

export default Navbar;