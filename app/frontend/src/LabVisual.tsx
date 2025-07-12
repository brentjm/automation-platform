import React from 'react';

interface InstrumentProps {
  x: number;
  y: number;
  name: string;
  isActive: boolean;
}

const Instrument: React.FC<InstrumentProps> = ({ x, y, name, isActive }) => (
  <g transform={`translate(${x}, ${y})`}>
    <rect width="100" height="60" rx="5" fill={isActive ? '#61dafb' : '#ccc'} stroke="#333" strokeWidth="2" />
    <text x="50" y="35" textAnchor="middle" fill="#000">{name}</text>
  </g>
);

interface LabVisualProps {
  activeInstruments: string[];
}

const LabVisual: React.FC<LabVisualProps> = ({ activeInstruments }) => {
  return (
    <svg viewBox="0 0 400 200" className="lab-svg">
      <Instrument x={50} y={50} name="Instrument A" isActive={activeInstruments.includes('instrument-a')} />
      <Instrument x={250} y={50} name="Instrument B" isActive={activeInstruments.includes('instrument-b')} />
      <line x1="150" y1="80" x2="250" y2="80" stroke="#666" strokeWidth="2" strokeDasharray="5,5" />
    </svg>
  );
};

export default LabVisual;
