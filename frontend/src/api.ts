
export interface Position{
  ticker:string,
  quantity:number,
  broker:string,
  market_value:number,
  
}

export const fetchPositions = async ():Promise<Position[]> => {
  const res = await fetch("/api/positions")
  if(!res.ok){
    throw new Error('Failed to fetch positions')
  }
  return res.json()
}
  