import React from 'react';
import { PieChart, Pie, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import type { Position } from '../api';

interface ExposureChartProps {
  positions: Position[];
}

const COLORS = ['#00f2fe', '#0072ff', '#8b5cf6', '#ec4899', '#f59e0b'];

const formatCompactValue = (value: number) => {
  const absVal = Math.abs(value);
  const sign = value < 0 ? '-' : '';
  if (absVal >= 1000000) {
    return `${sign}$${(absVal / 1000000).toFixed(1)}M`;
  }
  if (absVal >= 1000) {
    return `${sign}$${(absVal / 1000).toFixed(1)}K`;
  }
  return `${sign}$${absVal.toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
};

export const ExposurePieChart: React.FC<ExposureChartProps> = ({ positions }) => {
  const dataMap = positions.reduce((acc, pos) => {
    acc[pos.broker] = (acc[pos.broker] || 0) + pos.market_value;
    return acc;
  }, {} as Record<string, number>);

  const data = Object.keys(dataMap).map(key => ({
    name: key.replace('_', ' '),
    value: dataMap[key]
  }));

  const totalValue = data.reduce((sum, item) => sum + item.value, 0);

  return (
    <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', height: '420px', position: 'relative' }}>
      <h2 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '16px', color: 'var(--text-primary)' }}>
        Exposure by Broker
      </h2>
      
      <div style={{ flexGrow: 1, position: 'relative' }}>
        <ResponsiveContainer width="100%" height="90%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={75}
              outerRadius={95}
              paddingAngle={3}
              dataKey="value"
              stroke="none"
            >
              {data.map((_, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              formatter={(value: any) => `$${Number(value).toLocaleString(undefined, { maximumFractionDigits: 0 })}`}
              contentStyle={{ backgroundColor: '#0a0b12', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '10px' }}
            />
          </PieChart>
        </ResponsiveContainer>

        <div className="donut-center">
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.75rem', fontWeight: 500, margin: 0 }}>
            Exposure
          </p>
          <p style={{ fontSize: '1.25rem', fontWeight: 700, color: 'var(--text-primary)', margin: '2px 0 0 0' }}>
            {formatCompactValue(totalValue)}
          </p>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.7rem', margin: 0 }}>
            Total
          </p>
        </div>
      </div>

      {}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px 16px', fontSize: '0.8rem', marginTop: '-10px' }}>
        {data.map((item, index) => {
          const percentage = ((item.value / totalValue) * 100).toFixed(0);
          return (
            <div key={item.name} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: COLORS[index % COLORS.length] }}></span>
                <span style={{ color: 'var(--text-secondary)' }}>{item.name}</span>
              </div>
              <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{percentage}%</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
