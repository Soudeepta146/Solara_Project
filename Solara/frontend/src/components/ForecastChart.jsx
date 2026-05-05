import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function ForecastChart({ data, labels }) {
  // Mapping API data to chart format
  const chartData = data.map((val, i) => ({
    time: labels[i] ? labels[i].split(' ')[1] : i,
    ghi: val,
  }));

  return (
    <div className="h-[250px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData}>
          <defs>
            <linearGradient id="colorGhi" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#f97316" stopOpacity={0.4}/>
              <stop offset="95%" stopColor="#f97316" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
          <XAxis 
            dataKey="time" 
            stroke="#4b5563" 
            fontSize={10} 
            tickLine={false} 
            axisLine={false}
            interval={Math.floor(chartData.length / 6)} 
          />
          <YAxis hide domain={[0, 1200]} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#111827', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '12px' }}
            itemStyle={{ color: '#f97316' }}
          />
          <Area 
            type="monotone" 
            dataKey="ghi" 
            stroke="#f97316" 
            strokeWidth={3}
            fillOpacity={1} 
            fill="url(#colorGhi)" 
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}



