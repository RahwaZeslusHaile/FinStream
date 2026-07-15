
export interface Position{
  ticker:string,
  quantity:number,
  broker:string,
  market_value:number,
  
}

export const fetchPositions = async ():Promise<Position[]> => {
  const res = await fetch("https://3ars6wvzxa.execute-api.us-east-1.amazonaws.com/api/positions")
  if(!res.ok){
    throw new Error('Failed to fetch positions')
  }
  const data = await res.json()
  return data.map((pos: any) => ({
    ...pos,
    quantity: Number(pos.quantity),
    market_value: Number(pos.market_value),
  }))
}

export const triggerEtlSync = async():Promise<{message:string,positions_added:number}> =>{
  const res = await fetch("https://3ars6wvzxa.execute-api.us-east-1.amazonaws.com/api/etl-sync",{
    method:"POST"
  })
  if(!res.ok){
    throw new Error('Failed to trigger ETL sync')
  }
  return res.json()
}