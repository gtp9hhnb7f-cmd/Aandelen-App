'use client'
import {useEffect,useState} from 'react';import {getScenario} from '../../components/api';
export default function S(){const [rows,setRows]=useState<any[]>([]);useEffect(()=>{getScenario().then(setRows)},[]);return <div><h2>Niet verkocht scenario</h2><table><thead><tr><th>Asset</th><th>Verkoopwaarde</th><th>Theoretische actuele waarde</th><th>Extra P/L indien aangehouden</th></tr></thead><tbody>{rows.map((r,i)=><tr key={i}><td>{r.asset_name}</td><td>{r.sold_value}</td><td>{r.theoretical_current_value}</td><td>{r.extra_pnl_if_held}</td></tr>)}</tbody></table></div>}
