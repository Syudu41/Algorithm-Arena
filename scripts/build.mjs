import {mkdir, cp, readFile, writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root = fileURLToPath(new URL('../',import.meta.url));
await mkdir(root+'dist',{recursive:true});
await cp(root+'web',root+'dist',{recursive:true});
await mkdir(root+'dist/media',{recursive:true});
await cp(root+'media/bubble-tutorial.mp4',root+'dist/media/bubble-tutorial.mp4');
await cp(root+'media/bubble-poster.png',root+'dist/media/bubble-poster.png');
for (const name of ['algorithm-arena-intro.gif', 'algorithm-arena-intro-still.png']) {
  await cp(root+'media/'+name,root+'dist/media/'+name);
}
for (const name of ['insertion-tutorial.mp4', 'insertion-poster.png', 'merge-tutorial.mp4', 'merge-poster.png']) {
  await cp(root+'media/'+name,root+'dist/media/'+name);
}
await cp(root+'renderer/fonts',root+'dist/fonts',{recursive:true});
await writeFile(root+'dist/.nojekyll','');

let html = await readFile(root+'dist/index.html','utf8');
for (const name of ['app.js','style.css','favicon.svg','assets/algorithm-arena-logo.svg']) {
  const hash = createHash('sha256').update(await readFile(root+'dist/'+name)).digest('hex').slice(0,10);
  html = html.replace(/(?:src|srcset|href)="([^"]+)"/g, (attribute, url) =>
    url.split('?')[0] === './'+name ? attribute.replace(url, './'+name+'?v='+hash) : attribute);
}
await writeFile(root+'dist/index.html',html);
console.log('Built dist/ with relative assets and hash routes for GitHub Pages.');
