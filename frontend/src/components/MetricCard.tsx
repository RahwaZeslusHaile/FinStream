import React from 'react';
import { AreaChart, Area, ResponsiveContainer } from 'recharts';

interface MetricCardProps {
  title: string;
  value: string;
  percentChange: string;
  isPositive: boolean;
  glowType: 'cyan' | 'purple';
  chartData: { val: number }[];
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  percentChange,
  isPositive,
  glowType,
  chartData,
}) => {
  const isCyan = glowType === 'cyan';
  const lineColor = isCyan ? 'var(--accent-cyan)' : 'var(--accent-purple)';

  return (
    <div className={isCyan ? "card-glow-cyan" : "card-glow-purple"} style={{ padding: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', height: '140px' }}>
      <div style={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
        <div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', fontWeight: 500, marginBottom: '8px' }}>
            {title}
          </p>
          <h3 style={{ fontSize: '1.85rem', fontWeight: 700, color: 'var(--text-primary)', letterSpacing: '-0.5px' }}>
            {value}
          </h3>
        </div>
        <p style={{ 
          color: isPositive ? 'var(--accent-green)' : 'var(--accent-red)', 
          fontSize: '0.85rem', 
          fontWeight: 600,
          margin: 0
        }}>
          {percentChange} {isPositive ? '▲' : '▼'}
        </p>
      </div>

      <div style={{ width: '120px', height: '50px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id={`glow-${glowType}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={lineColor} stopOpacity={0.4}/>
                <stop offset="95%" stopColor={lineColor} stopOpacity={0}/>
              </linearGradient>
            </defs>
            <Area 
              type="monotone" 
              dataKey="val" 
              stroke={lineColor} 
              strokeWidth={1.5} 
              fill={`url(#glow-${glowType})`} 
              dot={false}
            />
          </AreaChart>
        </ResponsiveContainer>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', textAlign: 'right', marginTop: '4px' }}>
          Mini Chart
        </span>
      </div>
    </div>
  );
};
