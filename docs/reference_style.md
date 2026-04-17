# Reference Style

This document captures the reusable writing style that `mdwrite` should follow.

It is distilled from an internal SAR research-note example and exists so the skill does not depend on an external repo path.

## Core Rhythm

- start with a short, high-signal summary
- expose the document structure early when the note is long enough to need navigation
- move from concept to condition to trade-off instead of mixing everything together
- keep the main line readable and postpone expansion to later sections or appendix

## Section Style

- prefer short, explicit section titles
- use direct technical statements instead of padded transitions
- keep paragraphs short unless the logic truly needs a dense derivation block
- when the note is derivation-heavy, maintain a stable section rhythm rather than switching formats every few lines

## Summary Style

- the summary should be bullet-first
- each bullet should carry one real technical point
- summary bullets should state engineering consequences, not just topic labels

Good pattern:

- what problem the method solves
- what mechanism it uses
- what condition makes it valid
- what trade-off it introduces

## Math Style

- integrate equations near the sentences that explain why they matter
- do not leave equations as isolated blocks without physical or engineering interpretation
- when a stage signal is central, write the usable form rather than hiding behind abstract operator notation
- keep notation consistent within one note even if a source uses multiple variants

## Table Style

Prefer tables when the reader is comparing structured facts.

Default table use cases:

- goal / requirement / cost
- matched vs mismatched conditions
- pros vs cons
- trade-offs
- algorithm comparisons

## Derivation Style

- main body: only the derivation needed to support the story
- appendix: the place for full expansion when requested
- keep physical meaning close to the derivation instead of collecting all intuition at the end

For derivation-oriented notes, a strong default order is:

1. summary
2. problem definition
3. assumptions and symbols
4. key derivation steps
5. physical meaning
6. final result
7. implementation or engineering implication
8. limitations or scope

## Tone

- concise
- technical
- engineering-oriented
- not textbook-like
- not overly polished or decorative

The target feeling is:

- useful as a working note for the author
- readable enough to become a report later
- precise enough to support follow-up derivation

## What Not To Copy

- do not copy topic-specific content from the source example
- do not force every note to have a long outline
- do not overuse prose when a table or short bullets communicate better
- do not expand appendix-level math unless the user asks for it
