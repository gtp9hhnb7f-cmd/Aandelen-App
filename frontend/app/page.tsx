import Link from 'next/link'
export default function Home(){return <main><h1>Aandelenbeheer</h1><ul><li><Link href='/rapportage'>Rapportage</Link></li><li><Link href='/actuele-koersen'>Actuele koersen</Link></li><li><Link href='/niet-verkocht-scenario'>Niet verkocht scenario</Link></li><li><Link href='/data-import'>Data import</Link></li></ul></main>}
