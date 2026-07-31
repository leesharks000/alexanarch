// api/oai.js — OAI-PMH 2.0 endpoint for Alexanarch.
//
// Implements the six verbs against data/oai-index.json (compiled by
// scripts/build_oai_index.py). Supports selective harvesting by datestamp
// (from/until) and by set, with resumption tokens — which is what OpenAIRE,
// BASE, CORE and Invenio-based harvesters such as CDS actually use for
// incremental updates.
//
// deletedRecord = persistent. The repository undertakes to disseminate a
// status="deleted" header rather than dropping a record silently, permanently.
// For an archive whose subject is the difference between removed and never
// written, that is the protocol-level form of the same commitment.

const fs = require('fs');
const path = require('path');

let IDX = null;
function index() {
  if (!IDX) {
    const p = path.join(process.cwd(), 'data', 'oai-index.json');
    IDX = JSON.parse(fs.readFileSync(p, 'utf8'));
  }
  return IDX;
}

const esc = (s) =>
  String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&apos;')
    // strip characters XML 1.0 forbids, rather than emitting invalid XML
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '');

const nowISO = () => new Date().toISOString().replace(/\.\d+Z$/, 'Z');
const PAGE = 100;

function envelope(reqAttrs, body) {
  const attrs = Object.entries(reqAttrs)
    .filter(([, v]) => v != null && v !== '')
    .map(([k, v]) => ` ${k}="${esc(v)}"`).join('');
  return `<?xml version="1.0" encoding="UTF-8"?>
<OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
  <responseDate>${nowISO()}</responseDate>
  <request${attrs}>${esc(index().baseURL)}</request>
${body}
</OAI-PMH>`;
}

function oaiError(reqAttrs, code, msg) {
  return envelope(reqAttrs, `  <error code="${esc(code)}">${esc(msg)}</error>`);
}

function header(r) {
  const sets = (r.sets || []).map((s) => `      <setSpec>${esc(s)}</setSpec>`).join('\n');
  const status = r.deleted ? ' status="deleted"' : '';
  return `    <header${status}>
      <identifier>oai:alexanarch.org:${r.id}</identifier>
      <datestamp>${esc(r.datestamp)}</datestamp>
${sets}
    </header>`;
}

function dcRecord(r) {
  if (r.deleted) return `  <record>\n${header(r)}\n  </record>`;
  const subj = (r.subjects || [])
    .map((s) => `      <dc:subject>${esc(s)}</dc:subject>`).join('\n');
  const creatorId = r.orcid
    ? `      <dc:creator>${esc(r.creator)} (ORCID ${esc(r.orcid)})</dc:creator>`
    : `      <dc:creator>${esc(r.creator)}</dc:creator>`;
  return `  <record>
${header(r)}
    <metadata>
      <oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/"
                 xmlns:dc="http://purl.org/dc/elements/1.1/"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
      <dc:title>${esc(r.title)}</dc:title>
${creatorId}
      <dc:date>${esc(r.date)}</dc:date>
      <dc:type>${esc(r.type)}</dc:type>
      <dc:rights>${esc(r.rights)}</dc:rights>
      <dc:identifier>https://www.alexanarch.org/s/records/${r.id}/</dc:identifier>
      <dc:identifier>${esc(r.axn)}</dc:identifier>
      <dc:description>${esc(r.description)}</dc:description>
      <dc:publisher>Alexanarch — Crimson Hexagonal Archive</dc:publisher>
      <dc:language>eng</dc:language>
${subj}
      </oai_dc:dc>
    </metadata>
  </record>`;
}

function selectRecords(q) {
  const idx = index();
  let rs = idx.records;
  if (q.set) rs = rs.filter((r) => (r.sets || []).includes(q.set));
  if (q.from) rs = rs.filter((r) => r.datestamp && r.datestamp >= q.from);
  if (q.until) rs = rs.filter((r) => r.datestamp && r.datestamp <= q.until);
  return rs;
}

// Resumption tokens encode the query plus a cursor; opaque to the harvester,
// stateless for us, which is what a static archive needs.
const encTok = (o) => Buffer.from(JSON.stringify(o)).toString('base64url');
function decTok(t) {
  try { return JSON.parse(Buffer.from(t, 'base64url').toString('utf8')); }
  catch (e) { return null; }
}

const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

module.exports = (req, res) => {
  const url = new URL(req.url, `https://${req.headers.host || 'www.alexanarch.org'}`);
  const p = Object.fromEntries(url.searchParams.entries());
  const verb = p.verb || '';
  const reqAttrs = { verb, identifier: p.identifier, metadataPrefix: p.metadataPrefix,
                     from: p.from, until: p.until, set: p.set };
  res.setHeader('Content-Type', 'text/xml; charset=utf-8');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'public, max-age=900');

  const idx = index();
  const send = (xml, code = 200) => { res.statusCode = code; res.end(xml); };

  for (const k of ['from', 'until']) {
    if (p[k] && !DATE_RE.test(p[k])) {
      return send(oaiError(reqAttrs, 'badArgument', `${k} must be YYYY-MM-DD`));
    }
  }
  if (p.metadataPrefix && p.metadataPrefix !== 'oai_dc') {
    return send(oaiError(reqAttrs, 'cannotDisseminateFormat',
      'This repository disseminates oai_dc.'));
  }

  if (verb === 'Identify') {
    return send(envelope(reqAttrs, `  <Identify>
    <repositoryName>${esc(idx.repositoryName)}</repositoryName>
    <baseURL>${esc(idx.baseURL)}</baseURL>
    <protocolVersion>2.0</protocolVersion>
    <adminEmail>${esc(idx.adminEmail)}</adminEmail>
    <earliestDatestamp>${esc(idx.earliestDatestamp)}</earliestDatestamp>
    <deletedRecord>persistent</deletedRecord>
    <granularity>YYYY-MM-DD</granularity>
    <description>
      <toolkit xmlns="http://www.openarchives.org/OAI/2.0/toolkit">
        <title>Alexanarch static OAI-PMH</title>
        <author><name>Lee Sharks</name><email>leesharks00@gmail.com</email></author>
      </toolkit>
    </description>
  </Identify>`));
  }

  if (verb === 'ListMetadataFormats') {
    return send(envelope(reqAttrs, `  <ListMetadataFormats>
    <metadataFormat>
      <metadataPrefix>oai_dc</metadataPrefix>
      <schema>http://www.openarchives.org/OAI/2.0/oai_dc.xsd</schema>
      <metadataNamespace>http://www.openarchives.org/OAI/2.0/oai_dc/</metadataNamespace>
    </metadataFormat>
  </ListMetadataFormats>`));
  }

  if (verb === 'ListSets') {
    const sets = idx.sets.map((s) =>
      `    <set>\n      <setSpec>${esc(s)}</setSpec>\n      <setName>${esc(s)}</setName>\n    </set>`
    ).join('\n');
    return send(envelope(reqAttrs, `  <ListSets>\n${sets}\n  </ListSets>`));
  }

  if (verb === 'GetRecord') {
    if (!p.identifier || !p.metadataPrefix) {
      return send(oaiError(reqAttrs, 'badArgument',
        'GetRecord requires identifier and metadataPrefix.'));
    }
    const m = /^oai:alexanarch\.org:(\d+)$/.exec(p.identifier);
    const r = m && idx.records.find((x) => x.id === Number(m[1]));
    if (!r) return send(oaiError(reqAttrs, 'idDoesNotExist', 'Unknown identifier.'));
    return send(envelope(reqAttrs, `  <GetRecord>\n${dcRecord(r)}\n  </GetRecord>`));
  }

  if (verb === 'ListIdentifiers' || verb === 'ListRecords') {
    let q = { from: p.from, until: p.until, set: p.set }, cursor = 0;
    if (p.resumptionToken) {
      const t = decTok(p.resumptionToken);
      if (!t) return send(oaiError(reqAttrs, 'badResumptionToken', 'Malformed token.'));
      q = { from: t.f, until: t.u, set: t.s }; cursor = t.c || 0;
    } else if (!p.metadataPrefix) {
      return send(oaiError(reqAttrs, 'badArgument', 'metadataPrefix is required.'));
    }
    const all = selectRecords(q);
    if (!all.length) {
      return send(oaiError(reqAttrs, 'noRecordsMatch',
        'No records match the specified criteria.'));
    }
    const page = all.slice(cursor, cursor + PAGE);
    const next = cursor + PAGE;
    const body = page.map((r) =>
      verb === 'ListRecords' ? dcRecord(r) : `  ${header(r).trim()}`).join('\n');
    const token = next < all.length
      ? `  <resumptionToken completeListSize="${all.length}" cursor="${cursor}">` +
        `${encTok({ f: q.from, u: q.until, s: q.set, c: next })}</resumptionToken>`
      : `  <resumptionToken completeListSize="${all.length}" cursor="${cursor}"></resumptionToken>`;
    return send(envelope(reqAttrs, `  <${verb}>\n${body}\n${token}\n  </${verb}>`));
  }

  return send(oaiError(reqAttrs, 'badVerb',
    'Value of the verb argument is not a legal OAI-PMH verb.'));
};
