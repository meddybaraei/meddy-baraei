// Render motion-graphics.html to JPEG frames: node render.js <html> <outdir> <seconds> [preview]
const {chromium} = require('/opt/node-tools/node_modules/playwright');
const [, , html, outdir, secs, preview] = process.argv;
(async () => {
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport: {width: 1080, height: 1920}});
  await p.goto('file://' + html);
  await p.evaluate(() => document.fonts.ready);
  const fps = 30, n = Math.ceil(+secs * fps);
  const times = preview ? preview.split(',').map(Number) : Array.from({length: n}, (_, i) => i / fps);
  for (let i = 0; i < times.length; i++) {
    await p.evaluate(t => render(t), times[i]);
    await p.screenshot({path: `${outdir}/f${String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 92});
  }
  await b.close();
})();
