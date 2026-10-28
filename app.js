import { parseValues } from './validation.js';
const main = document.querySelector('main');
let cleanup = () => {};
const player = (id, src, title) => `
  <div class="player">
    <video id="${id}" controls preload="metadata" playsinline
      ${id === 'tutorial' ? 'poster="./media/bubble-poster.png"' : ''}
      aria-label="${title}" ${src ? `src="${src}"` : ''}></video>
    <div class="player-tools">
      <span>Visual explanation · no audio</span>
      <button type="button" data-replay="${id}">Replay</button>
      <label>Playback speed
        <select data-speed="${id}" aria-label="${title} playback speed">
          <option value="0.5">0.5×</option><option value="1" selected>1×</option>
          <option value="1.5">1.5×</option><option value="2">2×</option>
        </select>
      </label>
    </div>
  </div>`;

const about = () => `
  <section class="hero about-hero" aria-labelledby="about-title">
    <div class="about-hero-copy">
      <p class="eyebrow">A visual study of algorithms</p>
      <h1 id="about-title">What if we could see how an algorithm <em>thinks?</em></h1>
      <p class="lede">Follow a comparison. Watch two values trade places. See why an algorithm works, one decision at a time.</p>
      <a class="button" href="#/sorting">Explore sorting <span aria-hidden="true">↗</span></a>
      <p class="hero-note"><span aria-hidden="true"></span>Small steps. Clear understanding.</p>
    </div>
    <figure class="intro-art">
      <img id="about-intro" src="./media/algorithm-arena-intro.gif"
        alt="Algorithm Arena, framed by a coral circle and a rotating cyan arc"
        width="720" height="720" fetchpriority="high" decoding="async">
    </figure>
  </section>
  <section class="about-grid" aria-label="About the project">
    <div>
      <p class="eyebrow">Our approach</p><h2>Motion that explains.</h2>
      <p>A highlighted pair asks a question. A swap shows the answer. Each value stays attached to its tile, so you can follow the reasoning from the first comparison to the final position.</p>
    </div>
    <div>
      <p class="eyebrow">Behind the project</p><h2>Built with human judgment.</h2>
      <p>Algorithm Arena began as a case study in AI-assisted software development for MIS 7623. Coding agents assist with implementation and testing; people guide the requirements, review the work, and make the final decisions.</p>
      <p>Original animations are rendered with Manim Community Edition.</p>
    </div>
  </section>`;

const sorting = () => `
  <section class="page-intro">
    <p class="eyebrow">Explore / Sorting</p>
    <h1>Order, from <em>small decisions.</em></h1>
    <p class="lede">Bring a collection into sequence. Start with a simple question: are these two neighbours in the right order?</p>
  </section>
  <section class="catalog" aria-labelledby="catalog-title">
    <div class="catalog-heading"><h2 id="catalog-title">Start with the fundamentals.</h2><span>1 guided lesson</span></div>
    <a class="algorithm-card" href="#/sorting/bubble-sort">
      <div class="card-copy">
        <p class="eyebrow">Adjacent comparisons</p><h2>Bubble Sort</h2>
        <p>Compare, swap, and repeat. Watch the largest remaining value find its place.</p>
        <ul class="card-facts" aria-label="Algorithm properties"><li>Stable</li><li>In place</li><li>O(n²) average time</li></ul>
        <span class="card-action">Explore Bubble Sort <span aria-hidden="true">↗</span></span>
      </div>
      <div class="tile-diagram" aria-hidden="true"><span>5</span><span class="pair">2</span><span class="pair">4</span><span class="done">6<small>✓</small></span></div>
    </a>
  </section>`;

const bubble = () => `
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="#/sorting">Sorting</a><span aria-hidden="true">/</span><span aria-current="page">Bubble Sort</span></nav>
  <section class="detail-heading">
    <div><p class="eyebrow">Sorting / Bubble Sort</p><h1>Bubble Sort<span>One pair at a time.</span></h1></div>
    <p class="lede">Compare adjacent values. Swap when the left is larger. Each pass fixes the largest remaining value at the end. Stop when a pass makes no swaps.</p>
  </section>
  <dl class="complexity-strip" aria-label="Algorithm complexity">
    <div><dt>Average &amp; worst time</dt><dd>O(n²)</dd></div>
    <div><dt>Already sorted</dt><dd>O(n)</dd></div>
    <div><dt>Sorting space</dt><dd>O(1)</dd></div>
    <div><dt>Equal values</dt><dd>Order preserved</dd></div>
  </dl>
  <section class="lesson-section" aria-labelledby="learn-title">
    <div class="section-heading">
      <div><p class="eyebrow">01 / Watch · 38 seconds</p><h2 id="learn-title">Follow the reasoning.</h2></div>
      <button id="explain" class="button">Explain <span aria-hidden="true">▶</span></button>
    </div>
    ${player('tutorial', './media/bubble-tutorial.mp4', 'Bubble Sort explanation')}
    <ul class="legend" aria-label="Animation key"><li><i class="focus" aria-hidden="true"></i> Compare neighbours</li><li><i class="swap" aria-hidden="true"></i> Exchange positions</li><li><i class="done" aria-hidden="true"></i> ✓ Fixed in place</li></ul>
    <details><summary>Read the explanation &amp; counting rules</summary>
      <div class="explanation-copy"><p>The film starts with [4, 1, 6, 2, 5, 3]. The first comparison, 4 &gt; 1, triggers a swap. The comparison 4 &lt; 6 keeps both values in place. After the first pass, 6 is fixed at the end. Each pass works on a shorter prefix. A pass with no swaps ends the algorithm early.</p>
      <p>A comparison counts one adjacent value comparison. A swap counts one exchange of two values. Already sorted input needs n − 1 comparisons and no swaps.</p>
      <p>The sorting algorithm uses constant auxiliary space. Saving the educational animation trace requires additional storage. Equal values never swap with each other, preserving their original order.</p></div>
    </details>
  </section>
  <section class="try-section" aria-labelledby="try-title">
    <div class="try-intro"><p class="eyebrow">02 / Explore</p><h2 id="try-title">Give it an array.</h2><p>Your values, with every comparison and swap shown.</p><p class="quiet">2–10 integers, from −99 to 99. Negatives, duplicates, and zero welcome.</p></div>
    <div class="input-panel">
      <p id="render-availability" class="availability"></p>
      <form id="array-form" novalidate>
        <label for="values">Values, separated by commas</label>
        <input id="values" name="values" value="5,2,4,1,3" maxlength="200" autocomplete="off" spellcheck="false" aria-describedby="input-help status">
        <p id="input-help" class="quiet">Example: 5,2,4,1,3</p>
        <div class="form-actions"><button id="animate-submit" class="button" type="submit">Animate my array <span aria-hidden="true">↗</span></button><button id="cancel" type="button" hidden>Stop waiting</button></div>
      </form>
      <p id="status" role="status" aria-live="polite" aria-atomic="true"></p>
      <p class="render-note">Five-value animations usually play for 12–30 seconds. Rendering takes additional time; playback speed only changes the viewing pace.</p>
    </div>
  </section>
  <section id="result" hidden aria-labelledby="result-title">
    <div class="section-heading"><div><p class="eyebrow">Your animation</p><h2 id="result-title">Every step accounted for.</h2></div><span id="cache-label" class="availability"></span></div>
    <p id="summary"></p>
    ${player('custom', '', 'Your custom Bubble Sort animation')}
    <details class="render-details"><summary>Animation details</summary><p id="render-meta" class="quiet"></p></details>
  </section>`;

function wireAbout() {
  const image = document.querySelector('#about-intro');
  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const update = () => {
    image.src = preference.matches ? './media/algorithm-arena-intro-still.png' : './media/algorithm-arena-intro.gif';
  };
  preference.addEventListener('change', update);
  cleanup = () => preference.removeEventListener('change', update);
  update();
}
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
    notice.setAttribute('role', 'status');
    notice.textContent = 'This video is unavailable. Please refresh the page and try again.';
  }));
}
function wireExplore() {
  const tutorial = document.querySelector('#tutorial');
  document.querySelector('#explain').addEventListener('click', () => {
    tutorial.scrollIntoView({ block: 'center', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
    tutorial.play().catch(() => {});
  });
  const status = document.querySelector('#status');
  const input = document.querySelector('#values');
  const cancel = document.querySelector('#cancel');
  const result = document.querySelector('#result');
  const api = window.ARENA_CONFIG?.renderApi;
  const local = typeof api === 'string';
  document.querySelector('#render-availability').textContent = local ? 'Local rendering available' : 'Available in the local demo';
  const submit = document.querySelector('#animate-submit');
  submit.disabled = !local;
  if (!local) submit.textContent = 'Local demo required';
  status.textContent = local ? 'Ready for your array.' : 'Custom animations require the local demo. This static site includes the full explanation above.';
  const setStatus = (message, state = 'info') => { status.textContent = message; status.dataset.state = state; };
  let generation = 0, controller;
  const stop = () => { generation++; controller?.abort(); cancel.hidden = true; document.querySelector('#array-form')?.removeAttribute('aria-busy'); };
  cleanup = stop;
  cancel.addEventListener('click', () => { stop(); setStatus('Stopped waiting. Your render may still finish and be cached. Submit again when ready.'); });
  document.querySelector('#array-form').addEventListener('submit', async event => {
    event.preventDefault(); stop();
    result.hidden = true;
    const old = document.querySelector('#custom'); old.pause(); old.removeAttribute('src'); old.load();
    setStatus('Validating…'); input.removeAttribute('aria-invalid');
    let values;
    try { values = parseValues(input.value); }
    catch (error) { setStatus(error.message, 'error'); input.setAttribute('aria-invalid', 'true'); input.focus(); return; }
    if (!local) { setStatus('Valid array. Custom animations are available in the local demo; the explanation above is ready to watch.'); return; }
    controller = new AbortController(); const current = generation;
    const signal = controller.signal;
    cancel.hidden = false;
    document.querySelector('#array-form').setAttribute('aria-busy', 'true');
    const request = async (path, options = {}) => {
      const response = await fetch(api + path, {...options, signal: AbortSignal.any([signal, AbortSignal.timeout(8000)])});
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || `Server returned ${response.status}`);
      return data;
    };
    try {
      setStatus(`Submitting [${values.join(', ')}]…`, 'working');
      let job = await request('/api/renders', {method:'POST', headers:{'Content-Type':'application/json'},body:JSON.stringify({algorithm:'bubble',values})});
      const started = Date.now();
      while (current === generation && (job.status === 'queued' || job.status === 'rendering')) {
        setStatus(`${job.status === 'queued' ? 'Queued' : 'Rendering'}: [${values.join(', ')}]. This may take a minute or more.`, 'working');
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
      document.querySelector('#cache-label').textContent = job.cached ? 'Exact input cache hit' : 'New animation';
      result.hidden = false;
      setStatus(`Ready${job.cached ? ' · exact input cache hit' : ''}. Press Play below to watch your array.`, 'ready');
    } catch (error) {
      if (current !== generation) return;
      setStatus(error.name === 'TypeError' || error.name === 'TimeoutError' ? 'Local renderer unavailable. Start the local demo and retry; the explanation remains ready to watch.' : error.message, 'error');
    } finally { if (current === generation) { cancel.hidden = true; document.querySelector('#array-form').removeAttribute('aria-busy'); } }
  });
}
function render() {
  cleanup();
  cleanup = () => {};
  document.querySelectorAll('video').forEach(v => v.pause());
  const route = location.hash.slice(1) || '/about';
  const pages = {'/about':about, '/sorting':sorting, '/sorting/bubble-sort':bubble};
  main.innerHTML = (pages[route] || (() => '<section class="page-intro"><p class="eyebrow">Page not found</p><h1>Let’s find your next step.</h1><p class="lede">This page isn’t available. Explore our sorting lesson to continue.</p><a class="button" href="#/sorting">Explore sorting <span aria-hidden="true">↗</span></a></section>'))();
  document.querySelectorAll('header nav a').forEach(a => {
    const active = route === a.hash.slice(1) || (a.hash === '#/sorting' && route.startsWith('/sorting/'));
    if (active) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
  });
  const title = {'/about': 'About', '/sorting': 'Sorting', '/sorting/bubble-sort': 'Bubble Sort'}[route] || 'Page not found';
  document.title = `${title} · Algorithm Arena`;
  wirePlayers(); if (route === '/about') wireAbout();
  if (route === '/sorting/bubble-sort') wireExplore();
  main.focus({preventScroll:true}); window.scrollTo(0,0);
}
document.querySelector('.skip').addEventListener('click', event => { event.preventDefault(); main.focus(); });
window.addEventListener('hashchange', render);
render();
