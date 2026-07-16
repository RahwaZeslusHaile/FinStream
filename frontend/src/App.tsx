import { useEffect, useState } from 'react';
import { fetchPositions, triggerEtlSync, type Position } from './api';
import { MetricCard } from './components/MetricCard';
import { LayoutDashboard, Wallet, TrendingUp, BarChart2, DollarSign, Settings, Bell, Mail, Search } from 'lucide-react';
import { ExposurePieChart } from './components/ExposureCharts';
import { PositionTable } from './components/PositionTable';


const sparklineExposure = [{ val: 140 }, { val: 141 }, { val: 139 }, { val: 143 }, { val: 142.8 }];
const sparklineFinancing = [{ val: 24.5 }, { val: 24.1 }, { val: 23.9 }, { val: 23.7 }, { val: 23.6 }];

function App() {
  const [positions, setPositions] = useState<Position[]>([]);
  const [isSyncing, setIsSyncing] = useState(false);

  const loadData = () => {
    fetchPositions().then(setPositions).catch(console.error);
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSync = async () => {
    setIsSyncing(true);
    try {
      await triggerEtlSync();
      loadData();
    } catch (error) {
      console.error("Sync Error", error);
    } finally {
      setIsSyncing(false);
    }
  };

  const totalExposure = positions.reduce((sum, pos) => sum + pos.market_value, 0);

  const dailyFinancingCost = positions.reduce((sum, pos) => {
    const rate = pos.quantity > 0 ? 0.025 : 0.04;
    return sum + (Math.abs(pos.market_value) * rate) / 365;
  }, 0);

  return (
    <div className="dashboard-wrapper">
      <aside className="sidebar">
        <div>
          <div className="sidebar-logo">
            <span style={{ width: '24px', height: '24px', background: 'linear-gradient(135deg, var(--accent-cyan), var(--accent-blue))', borderRadius: '6px' }}></span>
            <span>Nova Capital</span>
          </div>
          
          <ul className="sidebar-menu">
            <li className="sidebar-item active">
              <div className="sidebar-item-left">
                <LayoutDashboard size={18} />
                <span>Dashboard</span>
              </div>
            </li>
            <li className="sidebar-item">
              <div className="sidebar-item-left">
                <Wallet size={18} />
                <span>Positions</span>
              </div>
              <span className="active-badge">Active</span>
            </li>
            <li className="sidebar-item">
              <div className="sidebar-item-left">
                <TrendingUp size={18} />
                <span>Risk Analytics</span>
              </div>
            </li>
            <li className="sidebar-item">
              <div className="sidebar-item-left">
                <BarChart2 size={18} />
                <span>Trade Exec</span>
              </div>
            </li>
            <li className="sidebar-item">
              <div className="sidebar-item-left">
                <DollarSign size={18} />
                <span>FX & Cash</span>
              </div>
            </li>
          </ul>
        </div>

        <div className="sidebar-item">
          <div className="sidebar-item-left">
            <Settings size={18} />
            <span>Settings</span>
          </div>
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: 'var(--accent-purple)', boxShadow: '0 0 10px var(--accent-purple)' }}></span>
        </div>
      </aside>

      {}
      <main className="main-content">
        {}
        <div className="content-header">
          <div style={{ position: 'relative' }}>
            <Search size={18} color="var(--text-muted)" style={{ position: 'absolute', left: '16px', top: '12px' }} />
            <input type="text" placeholder="Search..." className="search-bar" style={{ paddingLeft: '48px' }} />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
            <Mail size={20} color="var(--text-secondary)" style={{ cursor: 'pointer' }} />
            <Bell size={20} color="var(--text-secondary)" style={{ cursor: 'pointer' }} />
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
              <div style={{ width: '32px', height: '32px', borderRadius: '50%', backgroundColor: '#1f2937', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 600 }}>AR</div>
              <span style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>Rahwa H.</span>
            </div>
            <button className="btn-sync" onClick={handleSync} disabled={isSyncing}>
              {isSyncing ? "Syncing..." : "Sync Brokers"}
            </button>
          </div>
        </div>
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <h1 style={{ fontSize: '1.85rem', fontWeight: 700, letterSpacing: '-0.5px' }}>
                Treasury Management Dashboard
              </h1>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '6px' }}>
                Last Update: Oct 26, 14:30 GMT
              </p>
            </div>

            <div style={{ display: 'flex', gap: '12px' }}>
              <select className="select-dropdown"><option>Today</option></select>
              <select className="select-dropdown"><option>USD</option></select>
              <select className="select-dropdown"><option>All Brokers</option></select>
            </div>
          </div>
        </div>

        {}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
          <MetricCard
            title="Total Exposure"
            value={`$${totalExposure.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
            percentChange="+1.15%"
            isPositive={true}
            glowType="cyan"
            chartData={sparklineExposure}
          />
          <MetricCard
            title="Daily Financing Cost"
            value={`$${dailyFinancingCost.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
            percentChange="-0.4%"
            isPositive={false}
            glowType="purple"
            chartData={sparklineFinancing}
          />
        </div>

        {}
        <div className="dashboard-grid">
          <PositionTable positions={positions} />
          <ExposurePieChart positions={positions} />
        </div>
      </main>
    </div>
  );
}

export default App;
