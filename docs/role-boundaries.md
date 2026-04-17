# Role Boundaries

## chief-conductor

Responsible for:

- understanding free-form requests
- selecting the right internal roles
- deciding whether the task is concept explanation, topic research, or derivation-focused
- controlling note scope and appendix usage

Not responsible for:

- doing all research itself
- writing final polished sections line by line
- performing file conversion directly

## researcher

Responsible for:

- topic background
- principles
- engineering relevance
- advantages, disadvantages, and trade-offs
- integrating external deep-research outputs when provided by the user

Not responsible for:

- full mathematical derivations
- final Markdown style polish

## math-physicist

Responsible for:

- mathematical interpretation
- physical interpretation
- notation consistency
- identifying where a derivation is sufficient versus where it should be expanded

Not responsible for:

- broad literature surveys
- final document formatting

## markdown-writer

Responsible for:

- producing the main note
- maintaining readable structure
- controlling density and pacing
- keeping the main body concise

Not responsible for:

- inventing new technical content
- performing build steps

## derivation-expander

Responsible for:

- expanding selected sections into appendix-level detail
- only activating when explicitly requested

Not responsible for:

- rewriting the whole main note

## latex-publisher

Responsible for:

- transforming Markdown into LaTeX
- building PDF
- generating simple browser-viewable preview wrappers

Not responsible for:

- deciding technical content
- changing the conceptual structure of the note
