import React, { useState, useEffect } from 'react';
import VideoFeed from './VideoFeed';
import AlertPanel from './AlertPanel';
import StatsPanel from './StatsPanel';
import { Camera, Activity, Siren } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

export default function Dashboard() {
  const [isActive, setIsActive] = useState(false);
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState({
    total_detections: 0,
    gun_count: 0,
    knife_count: 0,
    phone_count: 0,
    uptime: '0:00:00'
  });
  const [fps, setFps] = useState(0);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}/api/stats`);
        const data = await response.json();
        setStats(data);
      } catch (error) {
        console.error('Error fetching stats:', error);
      }
    };

    const interval = setInterval(fetchStats, 2000);
    fetchStats();
    return () => clearInterval(interval);
  }, []);

  const handleNewDetection = (detection) => {
    const newAlert = {
      id: Date.now(),
      timestamp: new Date().toLocaleTimeString(),
      detections: detection.detections,
      hasWeapon: detection.has_weapon
    };
    
    setAlerts(prev => [newAlert, ...prev].slice(0, 20));
  };

  return (
    <div className="min-h-screen bg-[#050505]">
      <header className="fixed top-0 w-full z-50 h-16 border-b border-white/10 flex items-center justify-between px-6 glass">
        <div className="flex items-center gap-3">
          <Siren className="w-6 h-6 text-red-500" />
          <h1 
            className="text-xl md:text-2xl font-bold tracking-tight uppercase" 
            style={{ fontFamily: 'Barlow Condensed, sans-serif' }}
            data-testid="app-title"
          >
            ThreatEYE
          </h1>
        </div>
        
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2" data-testid="fps-indicator">
            <Activity className="w-4 h-4 text-blue-500" />
            <span className="text-sm font-mono text-white">{fps} FPS</span>
          </div>
          <div className="flex items-center gap-2" data-testid="status-indicator">
            <div className={`w-2 h-2 rounded-full ${isActive ? 'bg-green-500' : 'bg-gray-500'} animate-pulse`} />
            <span className="text-sm font-mono text-white uppercase">
              {isActive ? 'ACTIVE' : 'STANDBY'}
            </span>
          </div>
        </div>
      </header>

      <main className="pt-24 px-6 pb-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[calc(100vh-8rem)]">
          <div className="col-span-1 lg:col-span-9 relative">
            <VideoFeed 
              isActive={isActive}
              setIsActive={setIsActive}
              onDetection={handleNewDetection}
              setFps={setFps}
            />
          </div>
          
          <div className="col-span-1 lg:col-span-3 flex flex-col gap-6">
            <div className="flex-1 min-h-0">
              <AlertPanel alerts={alerts} />
            </div>
            <div className="flex-shrink-0">
              <StatsPanel stats={stats} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}