'use client'
import {useState} from 'react';
const API=process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000';
export default function I(){const [m,setM]=useState('');const onFile=async(e:any)=>{const f=e.target.files[0];const fd=new FormData();fd.append('file',f);const r=await fetch(`${API}/import/bux`,{method:'POST',body:fd});setM(JSON.stringify(await r.json()));};return <div><h2>Data import</h2><input type='file' onChange={onFile}/><p>{m}</p></div>}
