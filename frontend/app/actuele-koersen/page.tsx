'use client'
import {useEffect,useState} from 'react';import {getQuotes} from '../../components/api';
export default function Q(){const [q,setQ]=useState<any>({});useEffect(()=>{getQuotes().then(setQ)},[]);return <div><h2>Actuele koersen</h2><table><thead><tr><th>Asset</th><th>Koers</th><th>Valuta</th><th>Update</th><th>Dag%</th></tr></thead><tbody>{Object.entries(q).map(([k,v]:any)=><tr key={k}><td>{k}</td><td>{v.price}</td><td>{v.currency}</td><td>{v.timestamp}</td><td>{v.day_change}</td></tr>)}</tbody></table></div>}
