import React from 'react';

export default function SunHero({ value }) {
  return (
    <div className="flex flex-col items-center text-center">
      <div className="w-56 h-56 rounded-full sun-glow flex items-center justify-center border-[12px] border-white/20 mb-10 transition-transform hover:scale-105 duration-500">
        <div className="text-center">
            <span className="block text-6xl font-black text-white">{value}</span>
            <span className="text-[10px] font-black text-white/60 tracking-widest">W/M²</span>
        </div>
      </div>
      <h2 className="text-4xl font-serif italic text-[#635345] mb-2">Perfect solar day.</h2>
      <p className="text-sm font-bold text-gray-400">40% above average · <span className="text-orange-400">91% AI confidence</span></p>
    </div>
  );
}