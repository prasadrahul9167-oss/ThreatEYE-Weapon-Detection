import React from 'react';
import { Activity, Crosshair, Smartphone, Clock } from 'lucide-react';

export default function StatsPanel({ stats }) {
  const statItems = [
    {
      label: 'Total Detections',
      value: stats.total_detections,
      icon: Activity,
      color: 'text-blue-500'
    },
    {
      label: 'Weapons',
      value: stats.gun_count,
      icon: Crosshair,
      color: 'text-red-500'
    },
    {
      label: 'Phones',
      value: stats.phone_count,
      icon: Smartphone,
      color: 'text-orange-500'
    },
    {
      label: 'Uptime',
      value: stats.uptime,
      icon: Clock,
      color: 'text-green-500'
    }
  ];

  return (
    <div className="border border-white/10 bg-[#0f0f11] rounded-sm" data-testid="stats-panel">
      <div className="p-4 border-b border-white/10">
        <h2 
          className="text-lg font-bold uppercase tracking-tight text-white"
          style={{ fontFamily: 'Barlow Condensed, sans-serif' }}
        >
          SYSTEM STATS
        </h2>
      </div>
      
      <div className="p-4 grid grid-cols-2 gap-4">
        {statItems.map((item, idx) => (
          <div 
            key={idx} 
            className="p-4 bg-[#18181b] border border-white/5 rounded-sm"
            data-testid={`stat-${item.label.toLowerCase().replace(' ', '-')}`}
          >
            <div className="flex items-center gap-2 mb-2">
              <item.icon className={`w-4 h-4 ${item.color}`} />
              <span className="text-xs text-white/60 uppercase tracking-widest font-mono">
                {item.label}
              </span>
            </div>
            <div 
              className="text-2xl font-mono text-white font-bold"
              style={{ fontFamily: 'JetBrains Mono, monospace' }}
            >
              {item.value}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}