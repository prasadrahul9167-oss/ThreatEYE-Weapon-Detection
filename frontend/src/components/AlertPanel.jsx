import React from 'react';
import { ScrollText, AlertTriangle, Info } from 'lucide-react';

export default function AlertPanel({ alerts }) {
  return (
    <div className="h-full border border-white/10 bg-[#0f0f11] rounded-sm flex flex-col" data-testid="alert-panel">
      <div className="p-4 border-b border-white/10 flex items-center gap-2">
        <ScrollText className="w-5 h-5 text-blue-500" />
        <h2 
          className="text-lg font-bold uppercase tracking-tight text-white"
          style={{ fontFamily: 'Barlow Condensed, sans-serif' }}
        >
          DETECTION LOG
        </h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {alerts.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-white/30">
            <Info className="w-8 h-8 mb-2" />
            <p className="text-sm font-mono">No detections yet</p>
          </div>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className={`p-3 rounded-sm border-l-2 ${
                alert.hasWeapon
                  ? 'bg-red-950/30 border-red-500'
                  : 'bg-blue-950/30 border-blue-500'
              }`}
              data-testid="alert-item"
            >
              <div className="flex items-start gap-2">
                <AlertTriangle 
                  className={`w-4 h-4 mt-1 flex-shrink-0 ${
                    alert.hasWeapon ? 'text-red-500' : 'text-blue-500'
                  }`}
                />
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between items-start mb-1">
                    <span 
                      className={`text-xs font-mono ${
                        alert.hasWeapon ? 'text-red-200' : 'text-blue-200'
                      }`}
                    >
                      {alert.timestamp}
                    </span>
                  </div>
                  <div className="space-y-1">
                    {alert.detections.map((det, idx) => (
                      <div key={idx} className="text-xs font-mono text-white/80">
                        {det.class_name} ({Math.round(det.confidence * 100)}%)
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}