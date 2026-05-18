import { useEffect, useState } from 'react';
import {fetchPositions, type Position} from './api';
import { MetricCard } from './components/MetricCard';
import {DollarSign, Wallet} from 'lucide-react';
import {ExposurePieChart} from './components/ExposureCharts';
import {PositionTable} from './components/PositionTable';

function App(){
  const[positions,setPositions] = useState<Position[]>([])

  useEffect(()=>{
    fetchPositions().then((data)=>{
      setPositions(data)
    }).catch((console.error))
  },[])

  const totalExposure = positions.reduce((sum,pos)=>sum+pos.market_value,0);
  const totalQuantity = positions.reduce((sum,pos)=>sum+pos.quantity,0)

return (
    <div style={{ padding: '40px', maxWidth: '1200px', margin: '0 auto' }}>
      
      {}
      <div style={{ marginBottom: '40px' }}>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>
          Treasury Dashboard
        </h1>
        <p style={{ color: 'var(--text-secondary)' }}>
          Live Prime Broker Aggregation
        </p>
      </div>
      {}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px', marginBottom: '40px' }}>
        <MetricCard 
          title="Total Market Exposure" 
          value={`$${totalExposure.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`} 
          icon={DollarSign} 
        />
        <MetricCard 
          title="Total Units Held" 
          value={totalQuantity.toLocaleString()} 
          icon={Wallet} 
        />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '40px' }}>
        <ExposurePieChart positions={positions} />
        <PositionTable positions={positions} />
      </div>
    </div>
  );
}
export default App;