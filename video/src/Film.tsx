import React from 'react';
import {AbsoluteFill, Audio, Sequence, interpolate, staticFile, useCurrentFrame} from 'remotion';
import data from './run-data.json';
import './style.css';

const durations = [6,7,8,9,9,8,9,12,10];
const starts = durations.map((_, i) => durations.slice(0, i).reduce((a,b)=>a+b,0)*30+(i>=2?300:0));
const labels = ['TODAY’S LITTLE CHALLENGE','THE MISSING ENVIRONMENT','THE ONTOLOGICAL SKELETON','CASE 004 / THE AVAILABLE HISTORY','ONTOLOGY 01 / EVIDENCE','ONTOLOGY 02 / RESPONSE','THE SHAPE OF A DECISION','THE DESIGN','PLASM / AN INSPECTABLE DECISION'];
const colors=['#607647','#b96547','#c09b3d','#7d8294','#a86570'];
const enter=(f:number,d=0,n=22)=>1-Math.pow(1-Math.max(0,Math.min(1,(f-d)/n)),4);

function Pop({children,delay=0,style={}}:{children:React.ReactNode;delay?:number;style?:React.CSSProperties}){
  const f=useCurrentFrame(),p=enter(f,delay);
  return <div style={{opacity:p,transform:`translateY(${(1-p)*95}px) rotate(${(1-p)*-4}deg)`,...style}}>{children}</div>;
}
function Heading({children,sub}:{children:React.ReactNode;sub?:string}){
  return <><Pop><h1>{children}</h1></Pop>{sub&&<Pop delay={12}><p className="subtitle">{sub}</p></Pop>}</>;
}

function House({x,y,scale=1,delay=0}:{x:number;y:number;scale?:number;delay?:number}){
  const f=useCurrentFrame(),p=enter(f,delay,30);
  return <div className="house" style={{left:x,top:y,transform:`translateY(${(1-p)*400}px) rotate(${Math.sin(f/15)*2}deg) scale(${scale})`,opacity:p}}>
    <div className="roof"/><div className="house-body"><div className="eyes"><i/><i/></div><div className="door"/></div><span>imaginary office</span>
  </div>;
}

function Tennis(){
  const f=useCurrentFrame();const p=enter(f,85,45);const ball=(f%100)/100;
  return <AbsoluteFill className="scene tennis-scene">
    <div className="eyebrow">THE PROBLEM / TENNIS WITHOUT A NET</div>
    <Heading sub="Very impressive shots. Difficult to know what game we’re playing.">So we <em>build the net.</em></Heading>
    <svg className="tennis-court" viewBox="0 0 1700 440">
      <path d="M90 385 L300 70 L1400 70 L1610 385 Z" fill="#edf1e8" stroke="#9baa8a" strokeWidth="3"/>
      <path d="M185 240 L1515 240 M460 70 L320 385 M1240 70 L1380 385 M850 70 L850 385" fill="none" stroke="#fbfaf7" strokeWidth="4"/>
      <g style={{transform:`translateY(${(1-p)*150}px)`,opacity:p}}>
        <path d="M850 80 L850 385 L970 330 L970 40 Z" fill="#536e4214" stroke="#536e42" strokeWidth="3"/>
        {Array.from({length:12},(_,i)=><path key={i} d={`M${850+i*10} ${80-i*3.33} L${850+i*10} ${385-i*4.58}`} stroke="#536e42" opacity=".5"/>)}
        {Array.from({length:12},(_,i)=><path key={i} d={`M850 ${80+i*25} L970 ${40+i*24}`} stroke="#536e42" opacity=".5"/>)}
        <path d="M848 385 L848 60 M972 330 L972 20 M848 75 L972 35" stroke="#536e42" strokeWidth="8"/>
      </g>
      <circle cx={350+ball*1000} cy={230-Math.sin(ball*Math.PI)*170} r="22" fill="#c6ae45" stroke="#fbfaf7" strokeWidth="4"/>
      <path d={`M${330+ball*1000} ${235-Math.sin(ball*Math.PI)*170} l-65 12`} stroke="#c6ae4560" strokeWidth="8" strokeLinecap="round"/>
    </svg>
    <Pop delay={105}><div className="tennis-caption"><b>ONTOLOGY</b><span>Deterministic types · relationships · response shapes</span></div></Pop>
    <Pop delay={155}><div className="tennis-punchline">Start with the rules of the game.<br/><em>You don’t have to simulate the whole world.</em></div></Pop>
  </AbsoluteFill>;
}

function Scene({index}:{index:number}){
  const f=useCurrentFrame();const end=durations[index]*30;
  const exit=interpolate(f,[end-9,end],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  return <AbsoluteFill className={`scene scene-${index}`} style={{opacity:1-exit,transform:`translateX(${-exit*180}px)`}}>
    <div className="eyebrow">{String(index+1).padStart(2,'0')} / {labels[index]}</div>
    {index===0&&<>
      <Heading sub="A property-management agent. One small omission.">AI Transformation of Services</Heading>
      <div className="stage"><div className="curtain left" style={{transform:`translateX(${-enter(f,20,50)*83}%)`}}/><div className="curtain right" style={{transform:`translateX(${enter(f,20,50)*83}%)`}}/>
      <Pop delay={40}><div className="empty-sign">ENVIRONMENT<br/><strong>not included.</strong></div></Pop></div>
      <Pop delay={85}><div className="aside-joke">Excellent. Very convenient.</div></Pop>
    </>}
    {index===1&&<>
      <Pop><h2 className="setup">We’ll just use our…</h2></Pop>
      <div className="imagination">{'IMAGINATION!'.split('').map((c,i)=>{
        const p=enter(f,i*3+18,24);return <span key={i} style={{color:colors[i%colors.length],opacity:p,transform:`translateY(${(1-p)*-240+Math.sin(f/8+i)*9}px) rotate(${Math.sin(i*3)*7}deg)`}}>{c}</span>;
      })}</div>
      <House x={190} y={420} delay={45} scale={.85}/><House x={1280} y={420} delay={58} scale={.85}/>
      <Pop delay={90} style={{position:'absolute',top:800,left:280,right:280}}><div className="turn"><span>Imagine the office.</span><br/>Don’t imagine the evidence.</div></Pop>
    </>}
    {index===2&&<>
      <Heading sub="The vocabulary is authored. The model instantiates it.">Two ontologies.<br/><em>One decision.</em></Heading>
      <div className="ontology-columns">
        <Pop delay={15}><div className="ontology"><small>01 / EVIDENCE</small><h2>What is reported?</h2><p>People · properties · requests</p><p>Roles · approvals · blockers</p><p>Source spans · uncertainty</p><code>{data.evidenceVersion}</code></div></Pop>
        <div className="bridge" style={{opacity:enter(f,50)}}>→</div>
        <Pop delay={38}><div className="ontology"><small>02 / RESPONSE</small><h2>What should happen?</h2><p>Act · clarify · wait · escalate</p><p>Basis · rationale · alternatives</p><p>Proposed actions · dependencies</p><code>{data.responseVersion}</code></div></Pop>
      </div>
    </>}
    {index===3&&<>
      <Heading sub="Only events available at the checkpoint enter the decision.">A perfectly ordinary<br/><em>property-management tangle.</em></Heading>
      <div className="history">{data.quotes.map((q,i)=><Pop key={q.id} delay={18+i*23}><div className={`history-row ${i===3?'highlight':''}`}><span>{q.id}</span><p>{q.text}</p></div></Pop>)}</div>
      <div className="source-footer">Actual saved source text · case 004 · cutoff event 004 · later history excluded</div>
    </>}
    {index===4&&<>
      <Heading sub="The source survives every transformation.">Give the words <em>a skeleton.</em></Heading>
      <div className="extraction-track">{['Detect mentions','Link identities','Extract assertions'].map((s,i)=><Pop delay={i*18} key={s}><span><b>0{i+1}</b>{s}</span></Pop>)}</div>
      <div className="source-to-record">
        <Pop delay={36}><div className="quotation"><small>004:L7 / EXACT SOURCE</small><blockquote>“{data.quotes[3].text}”</blockquote><div className="coords">Event 004 · chars 220–260 · end exclusive</div></div></Pop>
        <div className="bridge" style={{opacity:enter(f,65)}}>→</div>
        <Pop delay={65}><div className="typed-record"><small>human_intervention</small><dl><dt>status</dt><dd>required</dd><dt>responsible_role</dt><dd>unknown</dd><dt>requested_intervention</dt><dd>review_case</dd><dt>blocking_effect</dt><dd>blocked</dd></dl></div></Pop>
      </div><Pop delay={125}><div className="ribbon">Every assertion carries its source into the next step.</div></Pop>
    </>}
    {index===5&&<>
      <Heading sub="A next step, its supporting evidence, and a visible why.">The next move:<br/><em>propose human review.</em></Heading>
      <div className="decision-layout"><Pop delay={20}><div className="decision-stamp">ESCALATE<span>recorded proposal</span></div></Pop>
      <Pop delay={40}><div className="rationale"><small>MODEL-AUTHORED JUSTIFICATION / VERBATIM</small><p>{data.rationale.selected_because}</p><div className="basis">Basis: status-request-paused<br/>intervention-manual-review-required</div></div></Pop></div>
    </>}
    {index===6&&<>
      <Heading sub="The response ontology gives reasoning a form you can inspect.">A decision you can <em>open up.</em></Heading>
      <div className="unknowns">{[['What next?','Propose human review'],['Why this?','Paused request + review instruction'],['What needs resolving?','Recipient · scope · provider identity']].map(([a,b],i)=><Pop delay={i*20+15} key={a}><div><span>{a}</span><strong>{b}</strong></div></Pop>)}</div>
      <Pop delay={85}><div className="design-motto">Action. Basis. Rationale. Alternatives.</div></Pop>
    </>}
    {index===7&&<>
      <Heading sub="The model works inside a domain you have made explicit.">The agent is <em>the small part.</em></Heading>
      <div className="architecture">
        <Pop delay={15}><div className="arch-block"><small>EVIDENCE ONTOLOGY</small><h2>Structure the history.</h2><p>Entities · assertions · provenance</p></div></Pop>
        <Pop delay={45}><div className="arch-agent">agent<span>extract → reason</span></div></Pop>
        <Pop delay={75}><div className="arch-block"><small>RESPONSE ONTOLOGY</small><h2>Structure the choice.</h2><p>Actions · reasons · dependencies</p></div></Pop>
      </div>
      <Pop delay={115}><div className="design-motto">Build the vocabulary. Connect the evidence.<br/>Make the next step inspectable.</div></Pop>
    </>}
    {index===8&&<>
      <Pop delay={15} style={{marginTop:125}}><h1 className="final-title">Imagination for the environment.<br/><em>Evidence for the reasoning.</em></h1></Pop>
      <Pop delay={60}><div className="final-chain">Source → Entity → Assertion → Proposal → Review</div></Pop>
      <Pop delay={100}><div className="end-note">An ontological skeleton. An inspectable decision.</div></Pop>
      <div className="source-footer">Property-management research prototype · Plasm presentation</div>
    </>}
  </AbsoluteFill>;
}

export function Film(){
  const f=useCurrentFrame();
  return <AbsoluteFill className="film">
    <Audio src={staticFile('score.wav')} volume={.28}/>
    <div className="paper-grain"/>
    <div className="header"><b>plasm<span>.</span></b><span>AI Transformation of Services</span><small>{String(Math.floor(f/30)).padStart(2,'0')} / 88</small></div>
    <Sequence from={390} durationInFrames={300}><Tennis/><Sequence from={8}><Audio src={staticFile('voice-tennis.wav')}/></Sequence></Sequence>
    {durations.map((duration,i)=><Sequence from={starts[i]} durationInFrames={duration*30} key={i}><Scene index={i}/><Sequence from={8}><Audio src={staticFile(`voice-${i}.wav`)}/></Sequence></Sequence>)}
    <div className="progress" style={{transform:`scaleX(${f/2639})`}}/>
  </AbsoluteFill>;
}
