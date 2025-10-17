import { useState } from 'react'

export default function App(){
  const [clean,setClean]=useState('');
  const [marked,setMarked]=useState('');
  const [stats,setStats]=useState({});
  const [exps,setExps]=useState([]);
  const [docx,setDocx]=useState('#');
  const [busy,setBusy]=useState(false);

  const onFile=async(e)=>{
    const f=e.target.files?.[0];
    if(!f) return;
    setBusy(true);
    const fd=new FormData(); fd.append('file',f);
    const res=await fetch('http://localhost:8080/process',{method:'POST',body:fd});
    const data=await res.json();
    setClean(data.clean_text||'');
    setMarked(data.marked_html||'');
    setStats(data.stats||{});
    setExps(data.explanations||[]);
    setDocx(`http://localhost:8080/export/docx/${data.job_id}`);
    setBusy(false);
  };

  return (
    <div style={{padding:20,fontFamily:'system-ui, Arial'}}>
      <h1>DE PDF→Text Korrektur (React)</h1>
      <input type="file" accept="application/pdf" onChange={onFile} />
      {busy && <p>Verarbeite…</p>}
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16,marginTop:16}}>
        <div>
          <h2>Reintext (bereinigt)</h2>
          <textarea style={{width:'100%',height:280}} readOnly value={clean} />
        </div>
        <div>
          <h2>Mit Fehler‑Markierung</h2>
          <div style={{border:'1px solid #ccc',padding:12,minHeight:280,whiteSpace:'pre-wrap'}}
               dangerouslySetInnerHTML={{__html:marked}} />
        </div>
      </div>
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16,marginTop:16}}>
        <div>
          <h2>Erklärung</h2>
          <ul>{exps.map((x,i)=>(<li key={i}><b>{x.rule}</b>: {x.hint} — <i>{x.example_fix}</i></li>))}</ul>
        </div>
        <div>
          <h2>Fehlerstatistik</h2>
          <pre>{JSON.stringify(stats,null,2)}</pre>
          <a href={docx}>DOCX export</a>
        </div>
      </div>
    </div>
  );
}
