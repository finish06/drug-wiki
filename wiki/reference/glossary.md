# Glossary

**NDC (National Drug Code)**
:   The FDA's 10-digit identifier printed on drug packages, in three segments:
    labeler, product and package, e.g. `0069-3150-83`. The segment widths vary
    (`4-4-2`, `5-3-2`, `5-4-1`), and an 11-digit `5-4-2` form pads one segment
    with a zero. The **product NDC** (first two segments) identifies the drug
    and strength; the package segment identifies the pack size.

**RxCUI (RxNorm Concept Unique Identifier)**
:   The ID of a drug concept in NLM's RxNorm vocabulary, e.g. `83367`
    (atorvastatin, the ingredient) or `617312` (atorvastatin 10 MG Oral Tablet,
    a product). Different levels mean different things: ingredients have no NDCs, products do.

**SPL (Structured Product Label)**
:   The FDA-approved label for a drug product (the package insert), published on
    DailyMed. Prescription labels use numbered sections: 4 Contraindications,
    5 Warnings and Precautions, 6 Adverse Reactions, 7 Drug Interactions. OTC
    "Drug Facts" labels don't.

**Set ID**
:   The stable UUID of an SPL across its versions (`setid`). Each new version of
    the label keeps the set ID and increases `spl_version`.

**Generic name**
:   The active ingredient's nonproprietary name, e.g. *atorvastatin calcium*.

**Brand name**
:   The proprietary name a manufacturer markets it under, e.g. *Lipitor*.

## Drug class types

**EPC (Established Pharmacologic Class)**
:   The clinically meaningful class, e.g. *HMG-CoA Reductase Inhibitor*.

**MoA (Mechanism of Action)**
:   How it works at the molecular level, e.g. *Hydroxymethylglutaryl-CoA Reductase Inhibitors*.

**PE (Physiologic Effect)**
:   The effect on the body, e.g. *Decreased Cholesterol*.

**CS (Chemical Structure)**
:   The chemical family, e.g. *Benzodiazepines*.

**Rate limit**
:   How many requests your key may make per minute. See [Errors and rate limits](errors.md#rate-limits).
