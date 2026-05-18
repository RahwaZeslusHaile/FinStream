import React from 'react';
import type { Position } from '../api';

interface PositionTableProps {
  positions: Position[];
}

export const PositionTable: React.FC<PositionTableProps> = ({ positions }) => {
  return (
    <div className="glass-panel" style={{ padding: '24px', overflowX: 'auto' }}>
      <h2 style={{ fontSize: '1.25rem', fontWeight: 600, marginBottom: '16px', color: 'var(--text-primary)' }}>
        Holdings Breakdown
      </h2>
      <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid var(--glass-border)', color: 'var(--text-secondary)' }}>
            <th style={{ padding: '12px 16px', fontWeight: 500 }}>Ticker</th>
            <th style={{ padding: '12px 16px', fontWeight: 500 }}>Broker</th>
            <th style={{ padding: '12px 16px', fontWeight: 500 }}>Quantity</th>
            <th style={{ padding: '12px 16px', fontWeight: 500 }}>Market Value</th>
          </tr>
        </thead>
        <tbody>
          {positions.map((pos, index) => (
            <tr key={index} style={{ borderBottom: '1px solid var(--glass-border)' }}>
              <td style={{ padding: '16px', fontWeight: 600, color: 'var(--accent-color)' }}>{pos.ticker}</td>
              <td style={{ padding: '16px', color: 'var(--text-primary)' }}>
                <span style={{ backgroundColor: 'var(--glass-border)', padding: '4px 8px', borderRadius: '4px', fontSize: '0.875rem' }}>
                  {pos.broker.replace('_', ' ')}
                </span>
              </td>
              <td style={{ padding: '16px', color: 'var(--text-primary)' }}>{pos.quantity}</td>
              <td style={{ padding: '16px', color: 'var(--text-primary)' }}>
                ${pos.market_value.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
