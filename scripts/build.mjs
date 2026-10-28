import {mkdir, cp, writeFile} from 'node:fs/promises';
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
for (const name of ['insertion-tutorial.mp4', 'insertion-poster.png']) {
  await cp(root+'media/'+name,root+'dist/media/'+name);
}
await cp(root+'renderer/fonts',root+'dist/fonts',{recursive:true});
await writeFile(root+'dist/.nojekyll','');
console.log('Built dist/ with relative assets and hash routes for GitHub Pages.');
