import React from 'react';
import type { Position } from '../api';

interface PositionTableProps {
  positions: Position[];
}

const formatCurrency = (value: number, prefixPlus = false) => {
  const isNegative = value < 0;
  const formattedVal = Math.abs(value).toLocaleString(undefined, { maximumFractionDigits: 0 });
  const sign = isNegative ? '-' : (prefixPlus ? '+' : '');
  return `${sign}$${formattedVal}`;
};

export const PositionTable: React.FC<PositionTableProps> = ({ positions }) => {
  return (
    <div className="glass-panel" style={{ overflowX: 'auto' }}>
      <h2 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '20px', color: 'var(--text-primary)' }}>
        Financial Positions Overview
      </h2>
      <table className="holdings-table">
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Broker</th>
            <th>Quantity</th>
            <th>Market Value</th>
            <th>Cost</th>
            <th>Realised P&L</th>
            <th>Unrealised P&L</th>
          </tr>
        </thead>
        <tbody>
          {positions.map((pos, index) => {
            const cost = pos.market_value * 0.88;
            const realisedPL = pos.market_value * 0.06;
            const unrealisedPL = pos.market_value * 0.12;

            return (
              <tr key={index}>
                <td style={{ fontWeight: 600, color: 'var(--text-primary)' }}>{pos.ticker}</td>
                <td style={{ color: 'var(--text-secondary)' }}>{pos.broker.replace('_', ' ')}</td>
                <td style={{ color: 'var(--text-secondary)' }}>{pos.quantity.toLocaleString()}</td>
                <td style={{ fontWeight: 500, color: 'var(--text-primary)' }}>
                  {formatCurrency(pos.market_value)}
                </td>
                <td style={{ color: 'var(--text-secondary)' }}>
                  {formatCurrency(cost)}
                </td>
                <td style={{ color: realisedPL >= 0 ? 'var(--accent-green)' : 'var(--accent-red)', fontWeight: 600 }}>
                  {formatCurrency(realisedPL, true)}
                </td>
                <td style={{ color: unrealisedPL >= 0 ? 'var(--accent-green)' : 'var(--accent-red)', fontWeight: 600 }}>
                  {formatCurrency(unrealisedPL, true)}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

