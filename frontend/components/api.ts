const API=process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000';
export const getReporting=()=>fetch(`${API}/reporting`).then(r=>r.json())
export const getQuotes=()=>fetch(`${API}/quotes`).then(r=>r.json())
export const getScenario=()=>fetch(`${API}/scenario/not-sold`).then(r=>r.json())
