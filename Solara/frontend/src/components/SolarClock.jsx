import React from 'react';

export default function SolarClock({ windows = [] }) {
    // Find the best window
    const best = windows.find(w => w.quality.includes("PEAK")) || windows[0];

    return (
        <div className="flex flex-col items-center">
            <div className="relative w-56 h-56 flex items-center justify-center">
                {/* Circular Track */}
                <svg className="absolute w-full h-full rotate-[-90deg]">
                    <circle cx="112" cy="112" r="100" fill="transparent" stroke="rgba(255,255,255,0.05)" strokeWidth="12" />
                    {/* Highlight Peak Area */}
                    <circle 
                        cx="112" cy="112" r="100" fill="transparent" stroke="#f97316" strokeWidth="12"
                        strokeDasharray="150 628" strokeDashoffset="-120" strokeLinecap="round"
                        className="opacity-50 blur-[1px]"
                    />
                </svg>
                <div className="text-center z-10">
                    <p className="text-[10px] text-gray-500 uppercase tracking-widest font-bold mb-1">Peak Window</p>
                    <p className="text-3xl font-bold text-orange-400">{best?.start || "--:--"}</p>
                    <p className="text-xs text-gray-400">until {best?.end || "--:--"}</p>
                </div>
            </div>
            <div className="mt-8 flex gap-6">
                <div className="text-center">
                    <p className="text-[10px] text-gray-500 font-bold uppercase mb-1">Status</p>
                    <p className="text-sm font-bold text-green-400">OPTIMAL</p>
                </div>
                <div className="w-px h-8 bg-white/10" />
                <div className="text-center">
                    <p className="text-[10px] text-gray-500 font-bold uppercase mb-1">Yield</p>
                    <p className="text-sm font-bold">MAX</p>
                </div>
            </div>
        </div>
    );
}




