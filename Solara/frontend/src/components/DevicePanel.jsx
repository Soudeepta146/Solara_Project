import React from 'react';
import { Car, Home, Watch, Battery } from 'lucide-react';

export default function DevicePanel({ devices, status }) {
  const icons = {
    "solar_car": <Car size={20} />,
    "ev": <Car size={20} />,
    "powerwall": <Home size={20} />,
    "solar_light": <Watch size={20} />
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {Object.entries(devices || {}).map(([key, config]) => (
        <div key={key} className="p-4 rounded-3xl bg-white/5 border border-white/10 flex items-center justify-between group hover:border-orange-500/30 transition-all">
          <div className="flex items-center gap-4">
            <div className="p-3 bg-white/5 rounded-2xl text-gray-400 group-hover:text-orange-500 transition-colors">
              {icons[key] || <Battery size={20} />}
            </div>
            <div>
              <p className="text-sm font-bold uppercase tracking-wider">{key.replace('_', ' ')}</p>
              <p className="text-xs text-gray-500">{config.efficiency * 100}% Efficiency Curve</p>
            </div>
          </div>
          <div className="text-right">
            <p className="text-xs font-medium text-orange-400">{config.threshold} W/m²</p>
            <p className="text-[10px] text-gray-600">THRESHOLD</p>
          </div>
        </div>
      ))}
    </div>
  );
}



