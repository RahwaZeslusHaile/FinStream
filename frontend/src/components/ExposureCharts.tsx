import React from 'react'
import {PieChart, Pie, Tooltip, ResponsiveContainer, Cell,Legend} from 'recharts'
import type {Position} from '../api'

interface ExposureChartProps {
    positions:Position[]
}

const COLORS = ['#38bdf8', '#8b5cf6', '#10b981', '#f59e0b']

export const ExposurePieChart:React.FC<ExposureChartProps> = ({positions}) => {
const dataMap = positions.reduce((acc, pos) => {
    acc[pos.broker] = (acc[pos.broker] || 0) + pos.market_value;
    return acc;
  }, {} as Record<string, number>);
  const data = Object.keys(dataMap).map(key => ({
    name: key.replace('_', ' '),
    value: dataMap[key]
  }));
  return (
    <div className="glass-panel" style={{ padding: '24px', height: '400px', display: 'flex', flexDirection: 'column' }}>
      <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '16px', color: 'var(--text-primary)' }}>
        Exposure by Broker
      </h2>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={80} 
            outerRadius={120}
            paddingAngle={5}
            dataKey="value"
            stroke="none"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip 
            formatter={(value: number) => `$${value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
            contentStyle={{ backgroundColor: 'var(--glass-bg)', border: '1px solid var(--glass-border)', borderRadius: '8px', color: 'var(--text-primary)' }}
          />
          <Legend wrapperStyle={{ color: 'var(--text-secondary)' }} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};