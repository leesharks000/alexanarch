/* check_gallery_js.js — a RUNTIME gate for the capture gallery's inline script.
 *
 * WHY THIS EXISTS. On 2026-08-13 the v9.6 fallback was removed by deleting the
 * line that listed the candidate URLs. Both URLs sat on that line, so the
 * deletion also removed `var CAPTURE_SOURCES`, and the loader iterated an
 * undefined array. Every count and every filter is built from that fetch, so
 * all three filter rows and the record count rendered EMPTY.
 *
 * `node --check` passed the whole time. It is a SYNTAX check: an undefined
 * identifier is legal syntax and fails only when executed. Three consecutive
 * "JS clean" reports were true and useless.
 *
 * This executes the script against a stub DOM and a stub fetch and fails on any
 * throw — ReferenceError included.
 */
const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync(process.argv[2] || 'captures/index.html', 'utf8');
const scripts = [...html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)]
  .filter(m => !/ld\+json/.test(m[1])).map(m => m[2]);

const el = () => ({
  innerHTML: '', textContent: '', value: '', style: {}, dataset: {}, classList:
    { add(){}, remove(){}, toggle(){}, contains(){ return false; } },
  addEventListener(){}, appendChild(){}, removeChild(){}, closest(){ return null; },
  querySelector(){ return null; }, querySelectorAll(){ return []; },
  scrollIntoView(){}, setAttribute(){}, select(){}, focus(){},
  get parentNode(){ return el(); },
});
const doc = {
  getElementById(){ return el(); }, querySelector(){ return el(); },
  querySelectorAll(){ return []; }, createElement(){ return el(); },
  addEventListener(){}, body: el(), documentElement: el(),
};
const sandbox = {
  document: doc, console,
  window: { addEventListener(){}, location: { hash: '', href: '' }, open(){} },
  location: { hash: '', href: '' },
  history: { replaceState(){} },
  navigator: { clipboard: { writeText: () => Promise.resolve() } },
  fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve(
    { entries: [], total_captures: 0, address_count: 0, observation_count: 0 }) }),
  requestAnimationFrame: f => f(),
  setTimeout: (f) => { try { f(); } catch (e) {} return 0; },
  Promise, JSON, Math, Date, RegExp, Object, Array, String, Number, Set, Map,
  /* The sandbox must carry every global the page legitimately uses, or the gate
     reports the harness's own gaps as page defects. URLSearchParams was missing
     and surfaced as a ReferenceError from the page's own query-param handling. */
  URLSearchParams, URL, TextDecoder, encodeURIComponent, decodeURIComponent,
  clearTimeout: () => {}, setInterval: () => 0, clearInterval: () => {},
};
sandbox.globalThis = sandbox;
sandbox.window.document = doc;

/* ONE CONTEXT FOR ALL BLOCKS. The page's script tags share global scope in a
   browser; running each in a fresh context made block 2 fail on a function
   block 1 defines globally — a false positive that would have sent me chasing a
   page bug that did not exist. The harness must model the runtime it gates. */
const ctx = vm.createContext(sandbox);
let failed = 0;
scripts.forEach((src, i) => {
  try {
    vm.runInContext(src, ctx, { timeout: 5000 });
    // A block that defines nothing global is a block that did not run: catch the
    // silent case where an early throw leaves later blocks referencing absent
    // functions, which is exactly how the CAPTURE_SOURCES fault stayed hidden.
  } catch (e) {
    failed++;
    console.error(`  BLOCK ${i + 1} THREW: ${e.name}: ${e.message}`);
  }
});
if (failed) {
  console.error(`RUNTIME GATE FAILED — ${failed} of ${scripts.length} script blocks threw.`);
  process.exit(1);
}
console.log(`runtime gate: ${scripts.length} script blocks executed, none threw`);
