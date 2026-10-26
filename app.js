import { parseValues } from './validation.js';
const main = document.querySelector('main');
let cleanup = () => {};
const player = (id, src, title) => `<div class="player"><video id="${id}" controls preload="metadata" playsinline ${id === 'tutorial' ? 'poster="./media/bubble-poster.png"' : ''} aria-label="${title}" ${src ? `src="${src}"` : ''}></video><div class="player-tools"><span>Silent film · follow the on-screen reasoning</span><button type="button" data-replay="${id}">Replay</button><label>Speed <select data-speed="${id}" aria-label="${title} playback speed"><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="1.5">1.5×</option><option value="2">2×</option></select></label></div></div>`;
const about = () => `<section class="hero"><p class="eyebrow">A visual study of algorithms</p><h1>What if we could see<br>how an algorithm <em>thinks?</em></h1><p class="lede">Make the invisible steps visible. Follow a comparison, watch two values trade places, and discover why an algorithm works.</p><a class="button" href="#/sorting">Explore sorting <span aria-hidden="true">↗</span></a><div class="visual-note"><span class="line"></span><span>One decision at a time.</span></div></section><section class="about-grid"><div><p class="eyebrow">01 / The idea</p><h2>Motion that explains.</h2><p>A highlighted pair asks a question. A physical swap shows the answer. Every number stays attached to its tile, so you can follow the reasoning all the way to a sorted array.</p></div><div><p class="eyebrow">02 / The making</p><h2>Built with human judgment.</h2><p>This project explores AI-assisted application development for MIS 7623. A coding agent assisted with implementation and testing. People define the requirements and review the visual quality, correctness, and release.</p><p>The application uses a deterministic sorting trace and genuine Manim videos. It has no chatbot or runtime AI.</p></div></section>`;
const sorting = () => `<section class="page-intro"><p class="eyebrow">Explore / Sorting</p><h1>Order, from<br><em>small decisions.</em></h1><p class="lede">Sorting brings a collection into sequence. Start with the simplest question: are these two neighbours in the right order?</p></section><a class="algorithm-card" href="#/sorting/bubble-sort"><div><p class="eyebrow">01 / Adjacent comparisons</p><h2>Bubble Sort <span aria-hidden="true">↗</span></h2><p>Compare. Swap. Repeat.<br>Watch the largest value find its place.</p><span class="tag">Manim explanation + local custom input</span></div><div class="tile-diagram" aria-hidden="true"><span>5</span><span class="pair">2</span><span class="pair">4</span><span class="done">6<small>✓</small></span></div></a><p class="quiet">Begin with one algorithm. Understand every step.</p>`;
const bubble = () => `<a class="breadcrumb" href="#/sorting">← Sorting</a><section class="detail-heading"><div><p class="eyebrow">01 / Bubble Sort</p><h1>A little closer.<br><em>Every pass.</em></h1></div><p class="lede">Compare adjacent values. Swap when the left is larger. After each pass, the largest remaining value is fixed at the end. Repeat until a pass makes no swaps.</p></section><section aria-labelledby="learn-title"><div class="section-heading"><div><p class="eyebrow">Learn / 38 seconds</p><h2 id="learn-title">Follow the reasoning.</h2></div><button id="explain" class="button">Explain <span aria-hidden="true">▶</span></button></div>${player('tutorial', './media/bubble-tutorial.mp4', 'Bubble Sort explanation')}<div class="legend"><span><i class="focus"></i> Compare neighbours</span><span><i class="swap"></i> Exchange positions</span><span><i class="done"></i> ✓ Fixed in place</span></div><details><summary>Read the explanation and complexity</summary><p>The film starts with [4, 1, 6, 2, 5, 3]. The first comparison, 4 &gt; 1, triggers a swap. The comparison 4 &lt; 6 keeps both values in place. After the first pass, 6 is fixed at the end. Each pass works on a shorter prefix. A pass with no swaps ends the algorithm early.</p><p>This implementation is stable and uses O(1) auxiliary space for sorting (the educational trace uses extra storage). Worst and average time: O(n²). Already sorted input: O(n), because of early exit. A comparison counts one adjacent value comparison; a swap counts one exchange of two values.</p></details></section><section class="try-section" aria-labelledby="try-title"><div><p class="eyebrow">Explore / Your turn</p><h2 id="try-title">Give it an array.</h2><p>Same visual language.<br>Your values, every step.</p><p class="quiet">2–10 integers · −99 to 99<br>Negatives, duplicates, and zero welcome.</p></div><div><form id="array-form" novalidate><label for="values">Values, separated by commas</label><input id="values" name="values" value="5,2,4,1,3" maxlength="200" autocomplete="off" spellcheck="false" aria-describedby="input-help status"><p id="input-help" class="quiet">Try 5,2,4,1,3 or 8,3,7,2,6.</p><div class="form-actions"><button class="button" type="submit">Animate my array <span aria-hidden="true">↗</span></button><button id="cancel" type="button" hidden>Stop waiting</button></div></form><p id="status" role="status" aria-live="polite"></p><p class="quiet">A typical five-value film plays for 12–30 seconds. Rendering takes additional time. Playback speed changes viewing pace only.</p></div></section><section id="result" hidden aria-labelledby="result-title"><p class="eyebrow">Your Manim film</p><h2 id="result-title">Every step accounted for.</h2><p id="summary"></p>${player('custom', '', 'Your custom Bubble Sort animation')}<p id="render-meta" class="quiet"></p></section>`;
function wirePlayers() {
  document.querySelectorAll('[data-speed]').forEach(select => select.addEventListener('change', () => {
    document.getElementById(select.dataset.speed).playbackRate = Number(select.value);
  }));
  document.querySelectorAll('[data-replay]').forEach(button => button.addEventListener('click', () => {
    const video = document.getElementById(button.dataset.replay);
    if (!video.getAttribute('src')) return;
    video.currentTime = 0;
    video.play().catch(() => {});
  }));
  document.querySelectorAll('video').forEach(v => v.addEventListener('error', () => {
    let notice = v.parentElement.querySelector('.media-error');
    if (!notice) { notice = document.createElement('p'); notice.className = 'media-error'; v.after(notice); }
    notice.textContent = 'The video could not be loaded. Check that the MP4 was included in the site build.';
  }));
}
function wireExplore() {
  const tutorial = document.querySelector('#tutorial');
  document.querySelector('#explain').addEventListener('click', () => {
    tutorial.scrollIntoView({ block: 'center', behavior: 'smooth' });
    tutorial.play().catch(() => {});
  });
  const status = document.querySelector('#status');
  const input = document.querySelector('#values');
  const cancel = document.querySelector('#cancel');
  const result = document.querySelector('#result');
  const api = window.ARENA_CONFIG?.renderApi;
  const local = typeof api === 'string';
  status.textContent = local ? 'Local Manim rendering is configured. Submit an array to begin.' : 'Custom rendering is available in the local demo. This static site includes the full explanation above; it has no Python rendering service.';
  let generation = 0, controller;
  const stop = () => { generation++; controller?.abort(); cancel.hidden = true; };
  cleanup = stop;
  cancel.addEventListener('click', () => { stop(); status.textContent = 'Stopped waiting. An already queued render may finish and be cached. Submit again when ready.'; });
  document.querySelector('#array-form').addEventListener('submit', async event => {
    event.preventDefault(); stop();
    result.hidden = true;
    const old = document.querySelector('#custom'); old.pause(); old.removeAttribute('src'); old.load();
    status.textContent = 'Validating…'; input.removeAttribute('aria-invalid');
    let values;
    try { values = parseValues(input.value); }
    catch (error) { status.textContent = error.message; input.setAttribute('aria-invalid', 'true'); input.focus(); return; }
    if (!local) { status.textContent = 'Valid array. To render it, run the local Python demo server. The public site serves the explanation film only.'; return; }
    controller = new AbortController(); const current = generation;
    const signal = controller.signal;
    cancel.hidden = false;
    const request = async (path, options = {}) => {
      const response = await fetch(api + path, {...options, signal: AbortSignal.any([signal, AbortSignal.timeout(8000)])});
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || `Server returned ${response.status}`);
      return data;
    };
    try {
      status.textContent = `Submitting [${values.join(', ')}]…`;
      let job = await request('/api/renders', {method:'POST', headers:{'Content-Type':'application/json'},body:JSON.stringify({algorithm:'bubble',values})});
      const started = Date.now();
      while (current === generation && (job.status === 'queued' || job.status === 'rendering')) {
        status.textContent = `${job.status === 'queued' ? 'Queued' : 'Rendering with Manim'}: [${values.join(', ')}]. This can take a minute or more; the page remains available.`;
        await new Promise((resolve, reject) => {
          const abort = () => { clearTimeout(timer); reject(new DOMException('Aborted','AbortError')); };
          const timer = setTimeout(() => { signal.removeEventListener('abort', abort); resolve(); }, 1000);
          signal.addEventListener('abort', abort, {once:true});
        });
        if (Date.now() - started > 1_500_000) throw new Error('Stopped waiting after 25 minutes. Check the local renderer.');
        job = await request(`/api/renders/${encodeURIComponent(job.id)}`);
      }
      if (current !== generation) return;
      if (job.status !== 'ready') throw new Error(job.error || `Render ${job.status}`);
      if (JSON.stringify(job.initial) !== JSON.stringify(values) || !/^\/api\/videos\/[a-f0-9]{32}\.mp4$/.test(job.video_url)) throw new Error('The server returned a mismatched render. Please retry.');
      document.querySelector('#summary').textContent = `Input [${job.initial.join(', ')}] → Sorted [${job.final.join(', ')}] · ${job.comparisons} comparisons · ${job.swaps} swaps`;
      document.querySelector('#custom').src = api + job.video_url;
      document.querySelector('#render-meta').textContent = `${job.duration_seconds} s playback · ${job.wall_seconds} s original render wall time · ${(job.bytes/1e6).toFixed(2)} MB · ${job.width}×${job.height} / ${job.fps} fps · ${job.cached ? 'Exact input cache hit' : 'New Manim render'}`;
      result.hidden = false;
      status.textContent = `Ready${job.cached ? ' · exact input cache hit' : ''}. Press Play to watch your array.`;
    } catch (error) {
      if (current !== generation) return;
      status.textContent = error.name === 'TypeError' || error.name === 'TimeoutError' ? 'Local renderer unavailable or not responding. Start the Python service and retry. The explanation remains playable.' : error.message;
    } finally { if (current === generation) cancel.hidden = true; }
  });
}
function render() {
  cleanup();
  document.querySelectorAll('video').forEach(v => v.pause());
  const route = location.hash.slice(1) || '/about';
  const pages = {'/about':about, '/sorting':sorting, '/sorting/bubble-sort':bubble};
  main.innerHTML = (pages[route] || (() => '<h1>Page not found.</h1><a href="#/sorting">Explore sorting</a>'))();
  document.querySelectorAll('nav a').forEach(a => {
    const active = route === a.hash.slice(1) || (a.hash === '#/sorting' && route.startsWith('/sorting/'));
    if (active) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
  });
  document.title = `${route.endsWith('bubble-sort') ? 'Bubble Sort' : route === '/sorting' ? 'Sorting' : 'About'} · Algorithm Arena`;
  wirePlayers(); if (route === '/sorting/bubble-sort') wireExplore();
  main.focus({preventScroll:true}); window.scrollTo(0,0);
}
window.addEventListener('hashchange', () => { if (location.hash === '#main') main.focus(); else render(); });
render();
