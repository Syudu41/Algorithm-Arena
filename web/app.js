import { parseValues } from './validation.js';
const main = document.querySelector('main');
let cleanup = () => {};
const player = (id, src, title, poster = id === 'tutorial' ? './media/bubble-poster.png' : null) => `
  <div class="player">
    <video id="${id}" controls preload="metadata" playsinline
      ${poster ? `poster="${poster}"` : ''}
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
      <p class="lede">Understand how algorithms work through clear, step-by-step animations.</p>
      <a class="button" href="#/sorting">Explore sorting <span aria-hidden="true">↗</span></a>
      <p class="hero-note"><span aria-hidden="true"></span>One decision at a time.</p>
    </div>
    <figure class="intro-art">
      <img id="about-intro" src="./media/algorithm-arena-intro.gif"
        alt="Algorithm Arena, framed by a coral circle and a rotating cyan arc"
        width="720" height="720" fetchpriority="high" decoding="async">
    </figure>
  </section>
  <section class="about-grid" aria-label="About the project">
    <div>
      <p class="eyebrow">See each step</p><h2>Motion that explains.</h2>
      <p>Highlights show which values are being compared. Movement reveals how their order changes. Follow each value from the first comparison to its final position.</p>
    </div>
    <div>
      <p class="eyebrow">At your pace</p><h2>Take a closer look.</h2>
      <p>Pause the video at a comparison, replay a move, or slow the animation down. Follow each decision until the next step feels clear.</p>
    </div>
  </section>`;

const sorting = () => `
  <section class="page-intro">
    <p class="eyebrow">Explore / Sorting</p>
    <h1>Order, from <em>small decisions.</em></h1>
    <p class="lede">Sorting puts values in order. Follow the comparisons that guide each step.</p>
  </section>
  <section class="catalog" aria-labelledby="catalog-title">
    <div class="catalog-heading"><h2 id="catalog-title">Start with the fundamentals.</h2></div>
    <a class="algorithm-card" data-algorithm="bubble" href="#/sorting/bubble-sort">
      <div class="card-copy">
        <p class="eyebrow">Adjacent comparisons</p><h2>Bubble Sort</h2>
        <p>Follow neighbouring values as the largest remaining value moves to the end.</p>
        <ul class="card-facts" aria-label="Algorithm properties"><li>Stable</li><li>In place</li><li>O(n²) average time</li></ul>
        <span class="card-action">Explore Bubble Sort <span aria-hidden="true">↗</span></span>
      </div>
      <div class="tile-diagram" aria-hidden="true"><span>5</span><span class="pair">2</span><span class="pair">4</span><span class="done">6<small>✓</small></span></div>
    </a>
    <a class="algorithm-card" data-algorithm="insertion" href="#/sorting/insertion-sort">
      <div class="card-copy">
        <p class="eyebrow">An ordered prefix</p><h2>Insertion Sort</h2>
        <p>Take the next value, make room, and place it in order. Grow a sorted prefix one value at a time.</p>
        <ul class="card-facts" aria-label="Algorithm properties"><li>Stable</li><li>In place</li><li>O(n²) average time</li></ul>
        <span class="card-action">Explore Insertion Sort <span aria-hidden="true">↗</span></span>
      </div>
      <div class="tile-diagram insertion-diagram" aria-hidden="true"><span class="ordered">2</span><span class="ordered">4</span><span class="ordered">5</span><span class="key">1</span></div>
    </a>
    <a class="algorithm-card" data-algorithm="merge" href="#/sorting/merge-sort">
      <div class="card-copy">
        <p class="eyebrow">Divide and conquer</p><h2>Merge Sort</h2>
        <p>Split the array into smaller groups, then merge ordered runs into one sorted whole.</p>
        <ul class="card-facts" aria-label="Algorithm properties"><li>Stable</li><li>O(n) extra space</li><li>O(n log n) time</li></ul>
        <span class="card-action">Explore Merge Sort <span aria-hidden="true">↗</span></span>
      </div>
      <div class="tile-diagram" aria-hidden="true"><span class="pair">2</span><span>5</span><span class="pair">1</span><span>4</span></div>
    </a>
  </section>`;

const customInput = (name = 'Bubble Sort', operations = 'comparison and swap') => `
  <section class="try-section" aria-labelledby="try-title">
    <div class="try-intro"><p class="eyebrow">Try it yourself</p><h2 id="try-title">Try your own array.</h2><p>Follow every ${operations} for your values.</p><p class="quiet">2–10 integers, from −99 to 99. Negatives, duplicates, and zero welcome.</p></div>
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
    <div class="section-heading"><div><p class="eyebrow">Your result</p><h2 id="result-title">Your sorted array.</h2></div><span id="cache-label" class="availability"></span></div>
    <p id="summary"></p>
    ${player('custom', '', `Your custom ${name} animation`)}
    <details class="render-details"><summary>Video details</summary><p id="render-meta" class="quiet"></p></details>
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
      <div><p class="eyebrow">Watch · 38 seconds</p><h2 id="learn-title">Follow the reasoning.</h2></div>
      <button id="explain" class="button">Explain <span aria-hidden="true">▶</span></button>
    </div>
    ${player('tutorial', './media/bubble-tutorial.mp4', 'Bubble Sort explanation')}
    <ul class="legend" aria-label="Animation key"><li><i class="focus" aria-hidden="true"></i> Compare neighbours</li><li><i class="swap" aria-hidden="true"></i> Exchange positions</li><li><i class="done" aria-hidden="true"></i> ✓ Fixed in place</li></ul>
    <details><summary>How Bubble Sort works</summary>
      <div class="explanation-copy"><p>The film starts with [4, 1, 6, 2, 5, 3]. The first comparison, 4 &gt; 1, triggers a swap. The comparison 4 &lt; 6 keeps both values in place. After the first pass, 6 is fixed at the end. Each pass works on a shorter prefix. A pass with no swaps ends the algorithm early.</p>
      <p>A comparison counts one adjacent value comparison. A swap counts one exchange of two values. Already sorted input needs n − 1 comparisons and no swaps.</p>
      <p>The sorting algorithm needs only a fixed amount of extra space. Equal values never swap with each other, so their original order is preserved.</p></div>
    </details>
  </section>
  ${typeof window.ARENA_CONFIG?.renderApi === 'string' ? customInput() : ''}`;

const insertion = () => `
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="#/sorting">Sorting</a><span aria-hidden="true">/</span><span aria-current="page">Insertion Sort</span></nav>
  <section class="detail-heading">
    <div><p class="eyebrow">Sorting / Insertion Sort</p><h1>Insertion Sort<span>Make room for the next value.</span></h1></div>
    <p class="lede">Take the next value, shift larger values to the right, and place it in the gap. Repeat to grow an ordered prefix, one value at a time.</p>
  </section>
  <dl class="complexity-strip" aria-label="Algorithm complexity">
    <div><dt>Average &amp; worst time</dt><dd>O(n²)</dd></div>
    <div><dt>Already sorted</dt><dd>O(n)</dd></div>
    <div><dt>Sorting space</dt><dd>O(1)</dd></div>
    <div><dt>Equal values</dt><dd>Order preserved</dd></div>
  </dl>
  <section class="lesson-section" aria-labelledby="learn-title">
    <div class="section-heading">
      <div><p class="eyebrow">Watch · 41 seconds</p><h2 id="learn-title">Find the key’s place.</h2></div>
      <button id="explain" class="button">Explain <span aria-hidden="true">▶</span></button>
    </div>
    ${player('tutorial', './media/insertion-tutorial.mp4', 'Insertion Sort explanation', './media/insertion-poster.png')}
    <ul class="legend" aria-label="Animation key"><li><i class="focus" aria-hidden="true"></i> Compare with the key</li><li><i class="swap" aria-hidden="true"></i> Shift right</li><li><i class="prefix" aria-hidden="true"></i> Ordered prefix</li></ul>
    <details><summary>How Insertion Sort works</summary>
      <div class="explanation-copy"><p>The values before the key are already in order. Larger values shift one position right to make a gap for the key. The ordered prefix grows after each insertion, though its values may move again on later steps.</p>
      <p>A comparison counts one value-to-key comparison. A shift moves one value one position right. A key placement puts the key back into the array, even when its position stays the same.</p>
      <p>Already sorted input needs n − 1 comparisons and no shifts. Equal values are never shifted past one another, preserving their original order. The sorting algorithm uses a fixed amount of extra space.</p></div>
    </details>
  </section>
  ${typeof window.ARENA_CONFIG?.renderApi === 'string' ? customInput('Insertion Sort', 'comparison, shift, and key placement') : ''}`;


const merge = () => `
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="#/sorting">Sorting</a><span aria-hidden="true">/</span><span aria-current="page">Merge Sort</span></nav>
  <section class="detail-heading">
    <div><p class="eyebrow">Sorting / Merge Sort</p><h1>Merge Sort<span>Split apart. Bring order together.</span></h1></div>
    <p class="lede">Divide the array until each group holds one value. Merge neighbouring sorted runs, choosing the smaller front value each time.</p>
  </section>
  <dl class="complexity-strip" aria-label="Algorithm complexity">
    <div><dt>Average &amp; worst time</dt><dd>O(n log n)</dd></div>
    <div><dt>Already sorted</dt><dd>O(n log n)</dd></div>
    <div><dt>Extra sorting space</dt><dd>O(n)</dd></div>
    <div><dt>Equal values</dt><dd>Order preserved</dd></div>
  </dl>
  <section class="lesson-section" aria-labelledby="learn-title">
    <div class="section-heading">
      <div><p class="eyebrow">Watch · under a minute</p><h2 id="learn-title">Build order from smaller runs.</h2></div>
      <button id="explain" class="button">Explain <span aria-hidden="true">▶</span></button>
    </div>
    ${player('tutorial', './media/merge-tutorial.mp4', 'Merge Sort explanation', './media/merge-poster.png')}
    <ul class="legend" aria-label="Animation key"><li><i class="focus" aria-hidden="true"></i> Compare front values</li><li><i class="swap" aria-hidden="true"></i> Place into the merged run</li><li><i class="done" aria-hidden="true"></i> Fully sorted</li></ul>
    <details><summary>How Merge Sort works</summary>
      <div class="explanation-copy"><p>A single value is already sorted. Split each larger group in two, sort both halves, then merge them. Only the front value of each sorted run can be its next smallest value. Choose the smaller front value and repeat; when one run is empty, place the remaining values in order.</p>
      <p>A comparison counts one front-to-front value comparison. A write counts one placement into a merged output run, including remaining values after one input run empties. Buffer allocation and copy-back bookkeeping are excluded from this counter. These are writes, not swaps.</p>
      <p>When front values are equal, choose the left one first to preserve their original order. This version always splits and merges, including already sorted input, so its time is O(n log n). The merge buffer needs O(n) extra space.</p>
      <p>Reference: <a href="https://algs4.cs.princeton.edu/22mergesort/index.php" target="_blank" rel="noopener noreferrer">Princeton Algorithms · Mergesort</a>.</p></div>
    </details>
  </section>
  ${typeof window.ARENA_CONFIG?.renderApi === 'string' ? customInput('Merge Sort', 'comparison and merged placement') : ''}`;

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
function wireLesson() {
  const tutorial = document.querySelector('#tutorial');
  document.querySelector('#explain').addEventListener('click', () => {
    tutorial.scrollIntoView({ block: 'center', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
    tutorial.play().catch(() => {});
  });
}
function wireExplore(algorithm = 'bubble') {
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
      let job = await request('/api/renders', {method:'POST', headers:{'Content-Type':'application/json'},body:JSON.stringify({algorithm,values})});
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
      if (job.algorithm !== algorithm || JSON.stringify(job.initial) !== JSON.stringify(values) || !/^\/api\/videos\/[a-f0-9]{32}\.mp4$/.test(job.video_url)) throw new Error('The server returned a mismatched render. Please retry.');
      const operations = algorithm === 'merge' ? `${job.writes} writes` : algorithm === 'insertion' ? `${job.shifts} shifts · ${job.placements} key placements` : `${job.swaps} swaps`;
      document.querySelector('#summary').textContent = `Input [${job.initial.join(', ')}] → Sorted [${job.final.join(', ')}] · ${job.comparisons} comparisons · ${operations}`;
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
  const pages = {'/about':about, '/sorting':sorting, '/sorting/bubble-sort':bubble, '/sorting/insertion-sort':insertion, '/sorting/merge-sort':merge};
  main.innerHTML = (pages[route] || (() => '<section class="page-intro"><p class="eyebrow">Page not found</p><h1>Let’s find your next step.</h1><p class="lede">This page isn’t available. Explore our sorting lesson to continue.</p><a class="button" href="#/sorting">Explore sorting <span aria-hidden="true">↗</span></a></section>'))();
  document.querySelectorAll('header nav a').forEach(a => {
    const active = route === a.hash.slice(1) || (a.hash === '#/sorting' && route.startsWith('/sorting/'));
    if (active) a.setAttribute('aria-current','page'); else a.removeAttribute('aria-current');
  });
  const title = {'/about': 'About', '/sorting': 'Sorting', '/sorting/bubble-sort': 'Bubble Sort', '/sorting/insertion-sort': 'Insertion Sort', '/sorting/merge-sort': 'Merge Sort'}[route] || 'Page not found';
  document.title = `${title} · Algorithm Arena`;
  wirePlayers(); if (route === '/about') wireAbout();
  if (route === '/sorting/bubble-sort' || route === '/sorting/insertion-sort' || route === '/sorting/merge-sort') {
    wireLesson();
    if (document.querySelector('#array-form')) wireExplore(route.endsWith('merge-sort') ? 'merge' : route.endsWith('insertion-sort') ? 'insertion' : 'bubble');
  }
  main.focus({preventScroll:true}); window.scrollTo(0,0);
}
document.querySelector('.skip').addEventListener('click', event => { event.preventDefault(); main.focus(); });
window.addEventListener('hashchange', render);
render();
