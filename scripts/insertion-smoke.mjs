// Insertion Sort catalog, lesson, typography and local rendering smoke checks.
import {spawn} from 'node:child_process';
import {mkdir,writeFile} from 'node:fs/promises';
const base=(process.env.ARENA_URL || 'http://127.0.0.1:8765').replace(/\/$/,'');
const staticOnly=process.env.ARENA_STATIC_ONLY==='1';
const chrome=spawn('/usr/bin/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--autoplay-policy=document-user-activation-required','--remote-debugging-port=0','--user-data-dir=/tmp/arena-chrome-'+process.pid,'about:blank'],{stdio:['ignore','ignore','pipe']});
let ws;
const results=[];
try{
  const endpoint=await new Promise((resolve,reject)=>{
    let log=''; const timeout=setTimeout(()=>reject(new Error('Chrome startup timeout: '+log.slice(-2000))),20000);
    chrome.stderr.on('data',buf=>{log+=buf;const match=log.match(/DevTools listening on ws:\/\/127\.0\.0\.1:(\d+)\//);if(match){clearTimeout(timeout);resolve('http://127.0.0.1:'+match[1]);}});
    chrome.on('error',reject);
  });
  const target=await (await fetch(endpoint+'/json/new?'+encodeURIComponent(base+'/#/about'),{method:'PUT'})).json();
  ws=new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j;});
  let id=0;const pending=new Map(); const errors=[];
  ws.onmessage=event=>{const m=JSON.parse(event.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(new Error(JSON.stringify(m.error))):p.resolve(m.result);} if(m.method==='Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.text);};
  const send=(method,params={})=>new Promise((resolve,reject)=>{const key=++id;pending.set(key,{resolve,reject});ws.send(JSON.stringify({id:key,method,params}));});
  await send('Page.enable');await send('Runtime.enable');
  const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
  const check=async (name,fn)=>{if(!await fn())throw new Error('FAIL: '+name);results.push('PASS '+name);console.log(results.at(-1));};
  const until=async (expression,timeout=15000)=>{const start=Date.now();while(Date.now()-start<timeout){if(await evaluate(expression))return true;await new Promise(r=>setTimeout(r,200));}throw new Error('Timed out: '+expression);};
  await until('document.querySelector("h1")?.textContent.includes("thinks")');
  await send('Page.bringToFront');
  await evaluate('location.hash="/sorting"');
  await until('document.querySelectorAll(".algorithm-card").length===2');
  await check('Insertion card follows Bubble Sort',()=>evaluate('(()=>{const c=[...document.querySelectorAll(".algorithm-card")];return c[0].dataset.algorithm==="bubble" && c[1].dataset.algorithm==="insertion" && c[1].getBoundingClientRect().top>=c[0].getBoundingClientRect().bottom})()'));
  await evaluate('document.querySelector("[data-algorithm=insertion]").click()');
  await until('document.title.startsWith("Insertion Sort")');
  await until('document.querySelector("#tutorial").readyState>=1');
  await check('Insertion tutorial is a real 35–60 second film without autoplay',()=>evaluate('document.querySelector("#tutorial").duration>=35 && document.querySelector("#tutorial").duration<=60 && document.querySelector("#tutorial").videoWidth===1280 && document.querySelector("#tutorial").paused'));
  await send('DOM.enable'); await send('CSS.enable'); await evaluate('document.fonts.ready');
  const doc=await send('DOM.getDocument');
  const fonts=async selector=>{const {nodeId}=await send('DOM.querySelector',{nodeId:doc.root.nodeId,selector});return (await send('CSS.getPlatformFontsForNode',{nodeId})).fonts;};
  const heading=await fonts('h1'),body=await fonts('.lede');
  await check('Insertion headings use CMR and body uses Arial variant',async()=>heading.every(f=>f.familyName==='CMU Serif') && body.every(f=>/Arial|Liberation Sans|Helvetica/.test(f.familyName)));
  await evaluate('document.querySelector("#explain").scrollIntoView({block:"center"})');
  const point=await evaluate('(()=>{const r=document.querySelector("#explain").getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()');
  await send('Input.dispatchMouseEvent',{type:'mousePressed',button:'left',clickCount:1,...point});await send('Input.dispatchMouseEvent',{type:'mouseReleased',button:'left',clickCount:1,...point});
  await until('document.querySelector("#tutorial").currentTime>.2 && !document.querySelector("#tutorial").paused');
  await check('Insertion Explain plays actual media',()=>evaluate('document.querySelector("#tutorial").readyState>=2'));
  await evaluate('document.querySelector("#tutorial").pause()');
  if(staticOnly) {
    await check('static insertion lesson has no local-only form or setup copy',()=>evaluate('!document.querySelector("#array-form") && !/local demo|python|renderer/i.test(document.querySelector("main").textContent)'));
  } else {
    await evaluate('document.querySelector("#values").value="1.5,2";document.querySelector("#array-form").requestSubmit()');
    await check('Insertion rejects invalid custom values',()=>evaluate('document.querySelector("#values").getAttribute("aria-invalid")==="true"'));
    const start=Date.now();
    await evaluate('document.querySelector("#values").value="5,2,4,1,3";document.querySelector("#array-form").requestSubmit()');
    await until('!document.querySelector("#result").hidden',300000);
    await check('Insertion custom output has exact array and operation counts',()=>evaluate('document.querySelector("#summary").textContent.includes("Input [5, 2, 4, 1, 3] → Sorted [1, 2, 3, 4, 5] · 9 comparisons · 7 shifts · 4 key placements")'));
    await until('document.querySelector("#custom").readyState>=1');
    await check('Insertion result is a real video and waits for user play',()=>evaluate('document.querySelector("#custom").duration>=12 && document.querySelector("#custom").duration<=30 && document.querySelector("#custom").paused'));
    const job=await evaluate('(async()=>{const name=new URL(document.querySelector("#custom").src).pathname.split("/").pop().replace(".mp4","");return await(await fetch("/api/renders/"+name)).json()})()');
    await check('API identifies Insertion without a false swaps field',async()=>job.algorithm==='insertion' && job.shifts===7 && job.placements===4 && !('swaps' in job));
    await writeFile('docs/evidence/insertion/web-local-job.json',JSON.stringify({request_to_ready_seconds:(Date.now()-start)/1000,job},null,2));
    await evaluate('document.querySelector("#array-form").requestSubmit()');
    await until('document.querySelector("#status").textContent.includes("cache hit")');
    await check('Insertion repeat uses exact algorithm-specific cache',()=>evaluate('document.querySelector("#cache-label").textContent.includes("cache hit")'));
    await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
    await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true}).then(r=>writeFile('docs/evidence/insertion/web-local-result.png',Buffer.from(r.data,'base64')));
  }
  for(const width of [1440,768,390,320]) {
    await send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:width<768});
    for(const route of ['/about','/sorting','/sorting/bubble-sort','/sorting/insertion-sort']) {
      const title={'/about':'About','/sorting':'Sorting','/sorting/bubble-sort':'Bubble Sort','/sorting/insertion-sort':'Insertion Sort'}[route];
      await evaluate(`location.hash=${JSON.stringify(route)}`);
      await until(`document.title.startsWith(${JSON.stringify(title)})`);
      await evaluate('document.fonts.ready');
      await check(`${width}px ${route} fits viewport`,()=>evaluate('document.documentElement.scrollWidth<=innerWidth && document.querySelectorAll("h1").length===1'));
      if((width===1440 || width===390) && (route==='/sorting' || route.endsWith('insertion-sort'))) {
        if(route.endsWith('insertion-sort'))await until('document.querySelector("#tutorial").readyState>=1');
        const name=route==='/sorting'?'catalog':'lesson';
        await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true}).then(r=>writeFile(`docs/evidence/insertion/web-${staticOnly?'static':'local'}-${name}-${width}.png`,Buffer.from(r.data,'base64')));
      }
    }
  }
  await send('Page.reload');await until('document.querySelector("#tutorial")?.readyState>=1');
  await check('Insertion nested route reload preserves lesson',()=>evaluate('location.hash==="#/sorting/insertion-sort" && document.querySelector("#tutorial").duration>=35'));
  await check('no runtime exceptions',async()=>errors.length===0);
  await writeFile(`docs/evidence/insertion/web-${staticOnly?'static':'local'}-checks.json`,JSON.stringify({heading,body,results,errors},null,2));
} finally {ws?.close();chrome.kill('SIGTERM');}
