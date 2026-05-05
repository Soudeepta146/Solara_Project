import React from 'react';

export default function YieldGauge({ value }) {
  const percentage = Math.min((value / 1200) * 100, 100); // 1200 W/m² as max

  return (
    <div className="flex flex-col items-center py-10">
      <div className="relative w-48 h-24 overflow-hidden">
        {/* Semicircle Track */}
        <div className="absolute w-48 h-48 border-[16px] border-white/5 rounded-full" />
        
        {/* Value Fill */}
        <div 
          className="absolute w-48 h-48 border-[16px] border-orange-500 rounded-full transition-all duration-1000 ease-out"
          style={{ 
            clipPath: 'inset(0 0 50% 0)',
            transform: `rotate(${(percentage * 1.8) - 180}deg)` 
          }}
        />
      </div>
      
      <div className="text-center mt-[-10px]">
        <span className="text-5xl font-bold tracking-tighter">{Math.round(value)}</span>
        <span className="text-gray-500 text-lg ml-2 font-medium">W/m²</span>
      </div>
    </div>
  );
}



