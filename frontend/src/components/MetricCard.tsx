import React from 'react'
import  type { LucideIcon } from "lucide-react"


interface MetricCardProps {
  title:string,
  value:number | string,
  icon:LucideIcon
}

export const MetricCard : React.FC<MetricCardProps> = ({ title, value, icon: Icon }) => {
  return(
    <div className='glass-panel' style={{padding:'24px',display:'flex',alignItems:'center',gap:'16px'}}>
      <div style={{backgroundColor:'var(--accent-glow)',padding:'12px',borderRadius:'12px',display:'flex'}}>
      <Icon color = 'var(--accent-color)' size={24} />
      </div>
      <div>
        <p style={{color:'var(--text-secondary)',fontSize:'0.875rem',fontWeight:500,marginBottom:'4px'}}>
            {title}
        </p>
        <h3 style={{fontSize:'1.5rem',fontWeight:600,color:'var(--text-primary)'}}>
            {value}
        </h3>
        
      </div>
    </div>
  )
}