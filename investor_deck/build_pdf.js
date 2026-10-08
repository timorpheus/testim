// Сборка PDF из index.html: node build_pdf.js [--png]
// Нужен Playwright (глобальный модуль) и Chromium.
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const dir = __dirname;
const out = path.join(dir, 'yakorya_investor.pdf');
const withPng = process.argv.includes('--png');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(dir, 'index.html'), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);

  await page.pdf({ path: out, width: '1600px', height: '900px', printBackground: true, preferCSSPageSize: true });
  console.log('PDF:', out);

  if (withPng) {
    const pngDir = path.join(dir, 'preview');
    fs.mkdirSync(pngDir, { recursive: true });
    const slides = await page.$$('section.slide');
    for (let i = 0; i < slides.length; i++) {
      const f = path.join(pngDir, `slide_${i + 1}.png`);
      await slides[i].screenshot({ path: f });
      console.log('PNG:', f);
    }
  }
  await browser.close();
})();
