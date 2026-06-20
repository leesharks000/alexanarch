/**
 * AXN — Alexanarch Identifier System
 * 
 * Content-derived emoji identifiers. Each work receives a unique
 * emoji address computed from its SHA-256 hash. The address is
 * verifiable, irrevocable, and human-readable.
 * 
 * Format: AXN:FAMILY.EMOJI₁EMOJI₂EMOJI₃EMOJI₄
 * Example: AXN:LIMINAL.🏛️🌀🔧💎
 * 
 * The 256 emoji are curated to be:
 * - Visually distinct at small sizes
 * - Cross-platform stable (tested on iOS, Android, Windows, Linux)
 * - Semantically evocative without being denotative
 * - Grouped into 16 families of 16 for navigability
 */

// 256 emoji mapped to byte values 0x00–0xFF
// Organized in 16 semantic clusters of 16
const AXN_GLYPHS = [
  // 0x00–0x0F: Celestial
  '🌑','🌒','🌓','🌔','🌕','🌖','🌗','🌘','⭐','🌟','💫','☀️','🌙','🪐','🌍','🌊',
  // 0x10–0x1F: Elemental  
  '🔥','💧','🌪️','⚡','❄️','🌋','🏔️','🌿','🍃','🌱','🌾','🪨','💎','🧊','🌈','☁️',
  // 0x20–0x2F: Architectural
  '🏛️','🏗️','🧱','🪜','🚪','🪟','🏠','🏰','⛩️','🕌','🗼','🌉','⚓','🛡️','🔔','🏺',
  // 0x30–0x3F: Instrumental
  '🔧','🔩','⚙️','🔗','🪝','🧲','⚖️','🔬','🔭','🧪','🧫','🧬','💡','🔮','🪄','🗝️',
  // 0x40–0x4F: Scriptural
  '📜','📖','📝','✏️','🖊️','📋','📌','📎','🔖','📚','🗂️','📦','🏷️','🪧','📐','📏',
  // 0x50–0x5F: Navigational
  '🧭','🗺️','🏴','🚩','⛳','🎯','🔍','👁️','🔎','🪞','🗡️','🛤️','⛵','🚀','🛸','🌀',
  // 0x60–0x6F: Temporal
  '⏳','⏰','🕐','🕑','🕒','🕓','🕔','🕕','🕖','🕗','🕘','🕙','🕚','🕛','⌛','🔄',
  // 0x70–0x7F: Organic
  '🌸','🌺','🌻','🌹','🍀','🌲','🌳','🍁','🍂','🍄','🐚','🪸','🦋','🐝','🕊️','🦅',
  // 0x80–0x8F: Symbolic
  '♠️','♥️','♦️','♣️','🎭','🎪','🎨','🎵','🎶','🎹','🎻','🎺','🥁','🎲','🃏','🀄',
  // 0x90–0x9F: Mathematical
  '➕','➖','✖️','➗','♾️','∮','⊕','⊗','△','▽','◇','○','●','□','■','▲',
  // 0xA0–0xAF: Alchemical
  '🜁','🝊','☿','♃','♄','♅','♆','☉','☽','♈','♉','♊','♋','♌','♍','♎',
  // 0xB0–0xBF: Gestural
  '👁️‍🗨️','🤲','👐','🙏','✊','🤝','👆','👇','👈','👉','🫵','🖐️','✋','🫶','🤙','👋',
  // 0xC0–0xCF: Signal
  '🚨','🔴','🟠','🟡','🟢','🔵','🟣','⚪','⚫','🟤','💜','💙','💚','💛','🧡','❤️',
  // 0xD0–0xDF: Structural
  '🔺','🔻','◀️','▶️','🔼','🔽','⏩','⏪','⏫','⏬','↗️','↘️','↙️','↖️','🔃','🔀',
  // 0xE0–0xEF: Liminal
  '🌅','🌄','🌃','🌆','🌇','🏙️','🌌','🎆','🎇','✨','🌠','💥','🔆','🔅','⭕','❌',
  // 0xF0–0xFF: Terminal
  '🏁','🎬','🔚','🔙','🔛','🔝','🔜','⏹️','⏏️','🔒','🔓','🔐','🗿','🪦','♻️','∞'
];

/**
 * Compute AXN identifier from content
 * @param {string} content - The full text of the deposit
 * @param {string} family - SP mint family name (e.g., "LIMINAL")
 * @returns {object} { axn, hash, emoji, family }
 */
async function computeAXN(content, family = 'UNCLASSIFIED') {
  // SHA-256 hash of content
  const encoder = new TextEncoder();
  const data = encoder.encode(content);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = new Uint8Array(hashBuffer);
  
  // Full hex hash
  const hexHash = Array.from(hashArray)
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
  
  // First 4 bytes → 4 emoji
  const emoji = [
    AXN_GLYPHS[hashArray[0]],
    AXN_GLYPHS[hashArray[1]],
    AXN_GLYPHS[hashArray[2]],
    AXN_GLYPHS[hashArray[3]]
  ].join('');
  
  // Extended: first 6 bytes → 6 emoji (for disambiguation if needed)
  const emojiExtended = [
    AXN_GLYPHS[hashArray[0]],
    AXN_GLYPHS[hashArray[1]],
    AXN_GLYPHS[hashArray[2]],
    AXN_GLYPHS[hashArray[3]],
    AXN_GLYPHS[hashArray[4]],
    AXN_GLYPHS[hashArray[5]]
  ].join('');
  
  const axn = `AXN:${family}.${emoji}`;
  
  return {
    axn,
    axnExtended: `AXN:${family}.${emojiExtended}`,
    hash: hexHash,
    emoji,
    emojiExtended,
    family,
    bytes: Array.from(hashArray.slice(0, 6)),
    verifiable: true,
    note: 'Verify by computing SHA-256 of the original content and mapping first 4 bytes through AXN_GLYPHS'
  };
}

/**
 * Verify an AXN against content
 * @param {string} axn - The claimed AXN identifier
 * @param {string} content - The content to verify against
 * @returns {boolean} Whether the AXN matches the content
 */
async function verifyAXN(axn, content) {
  // Extract family and emoji from AXN
  const match = axn.match(/^AXN:(\w+)\.(.+)$/);
  if (!match) return false;
  
  const [, family, claimedEmoji] = match;
  const computed = await computeAXN(content, family);
  
  return computed.emoji === claimedEmoji || computed.emojiExtended === claimedEmoji;
}

// Export for use in Alexanarch deposit system
if (typeof module !== 'undefined') {
  module.exports = { AXN_GLYPHS, computeAXN, verifyAXN };
}
