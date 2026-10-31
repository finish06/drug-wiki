# How the system fits together

The API you call is the front of three services. Each has one job.

<div class="dg-wrap">
<svg class="dg" viewBox="0 0 960 380" role="img" aria-labelledby="dg-sys-t dg-sys-d" xmlns="http://www.w3.org/2000/svg">
<title id="dg-sys-t">How the drug-data stack fits together</title>
<desc id="dg-sys-d">Your app calls drug-gate, the only public service, with an API key. drug-gate calls cash-drugs, an internal caching proxy. cash-drugs fetches from FDA DailyMed, openFDA and NLM RxNorm, and from rx-dag, an internal NDC database that loads FDA bulk downloads nightly.</desc>
<defs>
<marker id="dg-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="dg-head" d="M0,0 L10,5 L0,10 z"/></marker>
<marker id="dg-arrow-key" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="dg-head-key" d="M0,0 L10,5 L0,10 z"/></marker>
</defs>
<rect class="dg-zone" x="190" y="34" width="430" height="326" rx="14"/>
<text class="dg-zone-label" x="206" y="56">The drug-data stack</text>
<rect class="dg-app" x="20" y="126" width="110" height="48" rx="24"/>
<text class="dg-title" x="75" y="155" text-anchor="middle">Your app</text>
<path class="dg-edge dg-edge-key" d="M130,150 H214" marker-end="url(#dg-arrow-key)"/>
<text class="dg-label" x="174" y="140" text-anchor="middle">X-API-Key</text>
<rect class="dg-box dg-box-public" x="218" y="104" width="160" height="92" rx="10"/>
<text class="dg-tag dg-tag-public" x="298" y="124" text-anchor="middle">PUBLIC</text>
<text class="dg-title" x="298" y="146" text-anchor="middle">drug-gate</text>
<text class="dg-sub" x="298" y="166" text-anchor="middle">REST API</text>
<text class="dg-sub" x="298" y="183" text-anchor="middle">keys · limits · shaping</text>
<path class="dg-edge" d="M378,150 H426" marker-end="url(#dg-arrow)"/>
<rect class="dg-box" x="430" y="104" width="160" height="92" rx="10"/>
<text class="dg-tag dg-tag-internal" x="510" y="124" text-anchor="middle">INTERNAL</text>
<text class="dg-title" x="510" y="146" text-anchor="middle">cash-drugs</text>
<text class="dg-sub" x="510" y="166" text-anchor="middle">caching proxy</text>
<text class="dg-sub" x="510" y="183" text-anchor="middle">one copy per source</text>
<path class="dg-edge" d="M510,196 V254" marker-end="url(#dg-arrow)"/>
<rect class="dg-box" x="430" y="258" width="160" height="92" rx="10"/>
<text class="dg-tag dg-tag-internal" x="510" y="278" text-anchor="middle">INTERNAL</text>
<text class="dg-title" x="510" y="300" text-anchor="middle">rx-dag</text>
<text class="dg-sub" x="510" y="320" text-anchor="middle">NDC database</text>
<text class="dg-sub" x="510" y="337" text-anchor="middle">reloaded nightly</text>
<path class="dg-edge" d="M590,150 H660 M660,70 V230"/>
<path class="dg-edge" d="M660,70 H716" marker-end="url(#dg-arrow)"/>
<path class="dg-edge" d="M660,150 H716" marker-end="url(#dg-arrow)"/>
<path class="dg-edge" d="M660,230 H716" marker-end="url(#dg-arrow)"/>
<rect class="dg-src" x="720" y="40" width="220" height="60" rx="10"/>
<text class="dg-title" x="830" y="65" text-anchor="middle">FDA DailyMed</text>
<text class="dg-sub" x="830" y="85" text-anchor="middle">names · classes · labels</text>
<rect class="dg-src" x="720" y="120" width="220" height="60" rx="10"/>
<text class="dg-title" x="830" y="145" text-anchor="middle">openFDA</text>
<text class="dg-sub" x="830" y="165" text-anchor="middle">labels · recalls · shortages</text>
<rect class="dg-src" x="720" y="200" width="220" height="60" rx="10"/>
<text class="dg-title" x="830" y="225" text-anchor="middle">NLM RxNorm</text>
<text class="dg-sub" x="830" y="245" text-anchor="middle">IDs · generics · related</text>
<path class="dg-edge" d="M590,304 H716" marker-end="url(#dg-arrow)"/>
<path class="dg-src" d="M720,286 a110,10 0 0 1 220,0 V326 a110,10 0 0 1 -220,0 Z"/>
<path class="dg-src" d="M720,286 a110,10 0 0 0 220,0" fill="none"/>
<text class="dg-title" x="830" y="311" text-anchor="middle">FDA bulk downloads</text>
<text class="dg-sub" x="830" y="330" text-anchor="middle">NDC Directory · Drugs@FDA</text>
<text class="dg-label" x="830" y="22" text-anchor="middle">Government sources</text>
</svg>
</div>

| Service | Job | Who calls it |
|---|---|---|
| [**drug-gate**](drug-gate.md) | The public REST API: API keys, rate limits, CORS, input normalization, and turning raw source data into clean JSON | You |
| [**cash-drugs**](cash-drugs.md) | An internal caching proxy: fetches every government API once, stores it, refreshes it on a schedule, and keeps serving it when a source is down | drug-gate (internal only) |
| [**rx-dag**](rx-dag.md) | An internal NDC database: downloads the FDA's full NDC Directory and Drugs@FDA files every night and serves fast NDC lookups and search | cash-drugs (internal only) |

Only drug-gate is reachable from the internet. cash-drugs and rx-dag have no public address.

## A request, step by step

Take `GET /v1/drugs/info?ndc=0069-3150` (drug info for a Lipitor package):

1. **drug-gate checks the key** (`X-API-Key`), the key's per-minute limit and the caller's origin.
2. **drug-gate normalizes the NDC** (`0069-3150` and `00069-3150` are the same product) and looks in its own cache.
3. On a miss it asks **cash-drugs** for the product. cash-drugs answers from its store, or asks **rx-dag**, which looks the NDC up in tonight's copy of the FDA NDC Directory. The answer is the generic name, *atorvastatin calcium*.
4. drug-gate asks cash-drugs for the **newest FDA label** for that name and its XML. cash-drugs answers from its store, or fetches from **DailyMed** and keeps a copy.
5. drug-gate **parses the label** into interactions, contraindications, warnings and adverse reactions, caches the result, and returns JSON.

A repeat of the same request is answered from drug-gate's cache in a few milliseconds. The first one usually takes well under a second.

## Why three services

- **Government APIs are slow, rate-limited and sometimes down.** cash-drugs absorbs that: it calls each source once, paces itself to stay under rate limits, and keeps serving its last good copy during an outage.
- **The NDC Directory is too big and too important to query live.** rx-dag keeps the whole thing in a local database, so NDC lookups don't depend on openFDA.
- **The public API should be small and stable.** drug-gate is the only thing with keys, limits and a versioned contract (`/v1`); the plumbing behind it can change freely.

## Read more

- [drug-gate](drug-gate.md) · [cash-drugs](cash-drugs.md) · [rx-dag](rx-dag.md)
- [Data freshness](data-freshness.md): how old each kind of data can be.
- [Reliability](reliability.md): what happens when a source fails.
