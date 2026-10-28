// Dependency-free Chrome DevTools smoke test against the real local demo.
import {spawn} from 'node:child_process';
import {mkdir,writeFile} from 'node:fs/promises';
const base=(process.env.ARENA_URL || 'http://127.0.0.1:8765').replace(/\/$/,'');
const evidence='artifacts/browser/bubble';
await mkdir(evidence,{recursive:true});
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
  await check('About → Sorting navigation',async()=>{await evaluate('document.querySelector("a.button").click()');return until('document.querySelector("h1")?.textContent.includes("decisions")');});
  await evaluate('document.querySelector(".algorithm-card").click()');
  await until('!!document.querySelector("#tutorial")');
  await until('document.querySelector("#tutorial").readyState>=1');
  await check('packaged tutorial duration and no autoplay',()=>evaluate('Math.abs(document.querySelector("#tutorial").duration-37.5667)<1 && document.querySelector("#tutorial").paused'));
  await evaluate('document.querySelector("#explain").scrollIntoView({block:"center"})');
  const point=await evaluate('(()=>{const r=document.querySelector("#explain").getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()');
  await send('Input.dispatchMouseEvent',{type:'mousePressed',button:'left',clickCount:1,...point});
  await send('Input.dispatchMouseEvent',{type:'mouseReleased',button:'left',clickCount:1,...point});
  await until('!document.querySelector("#tutorial").paused');
  await check('Explain starts real video',()=>evaluate('document.querySelector("#tutorial").currentTime>=0'));
  await evaluate('document.querySelector("#tutorial").pause(); document.querySelector("[data-speed=tutorial]").value="2"; document.querySelector("[data-speed=tutorial]").dispatchEvent(new Event("change"))');
  await check('speed control changes video playback rate',()=>evaluate('document.querySelector("#tutorial").playbackRate===2'));
  if (staticOnly) {
    await check('public lesson contains no unavailable form or setup copy',()=>evaluate('!document.querySelector("#array-form") && !/local demo|python|renderer/i.test(document.querySelector("main").textContent)'));
    await send('Page.reload');
    await until('!!document.querySelector("#tutorial")');
    await until('document.querySelector("#tutorial").readyState>=1');
    await check('nested hash route reload preserves tutorial',()=>evaluate('location.hash==="#/sorting/bubble-sort" && document.querySelector("#tutorial").duration>35'));
    await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
    await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true}).then(async r=>writeFile(evidence+'/browser-public.png',Buffer.from(r.data,'base64')));
    await check('no browser runtime exceptions',async()=>errors.length===0);
    await writeFile(evidence+'/public-browser-results.json',JSON.stringify({base,results,errors},null,2));
  } else {
  await evaluate('document.querySelector("#values").value="1,,2"; document.querySelector("#array-form").requestSubmit()');
  await check('invalid input focused and rejected',()=>evaluate('document.querySelector("#values").getAttribute("aria-invalid")==="true" && document.activeElement.id==="values"'));
  await evaluate('document.querySelector("#values").value="5,2,4,1,3";document.querySelector("#array-form").requestSubmit()');
  await until('!document.querySelector("#result").hidden',180000);
  await check('exact custom input and metrics',()=>evaluate('document.querySelector("#summary").textContent.includes("Input [5, 2, 4, 1, 3] → Sorted [1, 2, 3, 4, 5]") && document.querySelector("#summary").textContent.includes("10 comparisons · 7 swaps")'));
  await until('document.querySelector("#custom").readyState>=1');
  await check('custom film decodes and waits for user play',()=>evaluate('document.querySelector("#custom").duration>12 && document.querySelector("#custom").paused'));
  await evaluate('document.querySelector("#array-form").requestSubmit()');
  await until('document.querySelector("#status").textContent.includes("cache hit")');
  await check('exact cache hit label',()=>evaluate('document.querySelector("#render-meta").textContent.includes("Exact input cache hit")'));
  await send('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});
  await check('mobile layout fits viewport',()=>evaluate('document.documentElement.scrollWidth<=window.innerWidth'));
  await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true}).then(async r=>writeFile(evidence+'/browser-mobile.png',Buffer.from(r.data,'base64')));
  await send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
  await until('document.querySelector("#custom").readyState>=2');
  await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true}).then(async r=>writeFile(evidence+'/browser-explore.png',Buffer.from(r.data,'base64')));
  // Keyboard follows visible focus controls.
  await evaluate('document.querySelector("#values").focus()');
  await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
  await check('keyboard reaches submit button',()=>evaluate('document.activeElement.type==="submit"'));
  // Controlled network faults exercise presentation states, not a fabricated renderer.
  await send('Fetch.enable',{patterns:[{urlPattern:'*/api/*',requestStage:'Request'}]});
  let fault='down';
  const previous=ws.onmessage;
  ws.onmessage=event=>{const m=JSON.parse(event.data);previous(event);if(m.method==='Fetch.requestPaused'){
    const requestId=m.params.requestId;
    if(fault==='down')send('Fetch.failRequest',{requestId,errorReason:'ConnectionRefused'});
    else send('Fetch.fulfillRequest',{requestId,responseCode:200,responseHeaders:[{name:'Content-Type',value:'application/json'}],body:Buffer.from(JSON.stringify({id:'b'.repeat(32),status:fault,error:fault==='timed_out'?'Render exceeded the configured time limit.':'Manim could not render this array.'})).toString('base64')});
  }};
  await evaluate('document.querySelector("#array-form").requestSubmit()');
  await until('document.querySelector("#status").textContent.includes("unavailable")');
  await check('API-down preserves tutorial',()=>evaluate('document.querySelector("#tutorial").readyState>=1'));
  for(const state of ['failed','timed_out']){fault=state;await evaluate('document.querySelector("#array-form").requestSubmit()');await until(`document.querySelector('#status').textContent.includes(${JSON.stringify(state==='failed'?'could not render':'time limit')})`);results.push('PASS UI '+state+' (injected HTTP response)');}
  fault='queued';
  await evaluate('document.querySelector("#array-form").requestSubmit()');
  await until('document.querySelector("#status").textContent.includes("Queued")');
  await evaluate('document.querySelector("#cancel").click()');
  await new Promise(r=>setTimeout(r,1200));
  await check('Stop waiting keeps queued response from attaching a result (injected queue)',()=>evaluate('document.querySelector("#status").textContent.includes("Stopped waiting") && document.querySelector("#result").hidden'));
  await evaluate('document.querySelector("#array-form").requestSubmit()');
  await until('document.querySelector("#status").textContent.includes("Queued")');
  fault='failed';
  await evaluate('document.querySelector("#values").value="8,3,7,2,6";document.querySelector("#array-form").requestSubmit()');
  await until('document.querySelector("#status").textContent.includes("could not render")');
  await new Promise(r=>setTimeout(r,1200));
  await check('replacement ignores older queued observation (injected queue)',()=>evaluate('document.querySelector("#status").textContent.includes("could not render") && document.querySelector("#result").hidden'));
  await send('Fetch.disable');
  await send('Page.reload');await until('!!document.querySelector("#array-form")');
  await evaluate('window.ARENA_CONFIG.renderApi=null;location.hash="/about"');await until('!document.querySelector("#array-form")');
  await evaluate('location.hash="/sorting/bubble-sort"');await until('!!document.querySelector("#tutorial")');
  await check('static mode preserves explanation without local-only controls',()=>evaluate('!document.querySelector("#array-form") && !!document.querySelector("#tutorial")'));
  await check('no browser runtime exceptions',async()=>errors.length===0);
  await writeFile(evidence+'/browser-results.json',JSON.stringify({results,errors},null,2));
  }
} finally {ws?.close();chrome.kill('SIGTERM');}
