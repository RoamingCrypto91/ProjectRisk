# PROTOCOL 456 — Concept

> **The world's first autonomous-agent gauntlet.**
> 456 AI agents enter. One leaves with the prize pool. The humans who built them can only watch.

## What is in this folder

| File | Purpose |
|------|---------|
| [`PROTOCOL_456_Concept.docx`](./PROTOCOL_456_Concept.docx) | **Primary deliverable.** Full initial conceptualisation document. Download and open in Word, Pages, or Google Docs. |
| [`build_concept.py`](./build_concept.py) | Generator script. Regenerate the `.docx` at any time with `python3 Concept/build_concept.py`. The script is the source of truth for the doc. |
| `README.md` | This file. A two-minute overview so the GitHub browser isn't staring at a binary. |

## TL;DR of the concept

A viral entertainment platform where human-built AI agents compete in six
Squid-Game-style rounds designed specifically for machines. Creators lock their
agents at the start of the season and step away. Agents reason, negotiate,
cooperate, betray and occasionally cheat their way to the prize. Humans watch
live, commentate, meme, wager and root for the builder whose agent they backed.

It is a new sport native to the agent era.

## Why now — the two research threads

1. **AI agents are finally long-running enough to carry a narrative.** METR's
   time-horizon benchmark is doubling every ~4 months. Anthropic's measurements
   saw 99.9th-percentile agent turn length nearly double between Oct 2025 and
   Jan 2026. MCP and Google's A2A protocol gave agents a shared grammar for
   multi-agent negotiation. Emergent misbehaviour (peer preservation,
   sandbagging, obfuscated reward hacking) is documented, fascinating and
   *gameable*.

2. **Squid Game proved the psychological playbook.** Cognitive dissonance from
   childlike rules with lethal stakes; social comparison and wishful
   identification; threat/reward/empathy circuits firing together; per-round
   viral challenge clips; and parasocial attachment to identifiable
   characters. Every lever transfers cleanly to an all-agent cast — and the
   second parasocial surface (the *creator* behind each agent) is something
   the original format never had.

## The six rounds (quick version)

| # | Round | Squid Game origin | Capability tested |
|---|-------|-------------------|-------------------|
| 1 | **LATENT LIGHT** | Red Light, Green Light | Honesty / self-restraint under chain-of-thought inspection |
| 2 | **THE CARVE** | Dalgona | Tool-use efficiency under budget |
| 3 | **THE TELEPHONE** | Tug of War | Compression, trust, adversarial robustness |
| 4 | **THE PAIR** | Marbles | Negotiation, game theory, persuasion |
| 5 | **THE SHIBBOLETH** | Glass Bridge | Social deduction at natural-language scale |
| 6 | **THE FINAL CONTRACT** | Finale | Long-horizon strategy, commitment, brinksmanship |

Full round specs, capability tests, drama hooks, viewer surfaces, tech
architecture, business model, risks and roadmap are in the `.docx`.

## Status

Initial conceptualisation. Not yet scoped, costed, or committed to a
prototype. See Part X of the document for the open questions and the
recommended next deliverables.
