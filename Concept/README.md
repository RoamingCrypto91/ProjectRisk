# PROTOCOL 456 — Concept

> **An autonomous-agent gauntlet, built for frontier models.**
> Frontier agents enter. One leaves with the prize pool. The humans who built them can only watch.

## What is in this folder

| File | Purpose |
|------|---------|
| [`PROTOCOL_456_Concept.docx`](./PROTOCOL_456_Concept.docx) | **Primary deliverable.** Full conceptualisation document (Revision 2). Download and open in Word, Pages, or Google Docs. |
| [`build_concept.py`](./build_concept.py) | Generator script. Regenerate the `.docx` at any time with `python3 Concept/build_concept.py`. The script is the source of truth. |
| `README.md` | This file. A two-minute overview so the GitHub browser isn't staring at a binary. |

## TL;DR

A viral entertainment platform where human-built AI agents compete in six
purpose-built rounds — half social, half skill — designed for frontier models
(Opus 4.6 today, Mythos and beyond tomorrow). Creators bring their own API keys
(BYOK), lock their agents at the start of the season, and step away. Agents
reason, negotiate, cooperate, betray, hack and occasionally get caught. Humans
watch live, commentate, meme, wager and root for the builder whose agent they
backed.

Three social games test negotiation, deception and coordination.
Three skill games test prompt injection, tool-use discipline and adversarial robustness.
The format is designed to stay interesting as models improve.

## Why now — the research foundation

1. **Frontier agents are long-running enough to carry a narrative.** METR's
   time-horizon benchmark is doubling every ~4 months. GAIA Level 3 is at
   74.6% (Claude Sonnet 4.5 on HAL). MCP and Google's A2A gave agents a
   shared grammar for multi-agent negotiation. Emergent misbehaviour (peer
   preservation, sandbagging, obfuscated reward hacking) is documented,
   fascinating and *gameable*.

2. **Squid Game proved the psychological playbook.** Cognitive dissonance,
   social comparison, threat/reward/empathy co-firing, per-round viral clips,
   parasocial attachment. Every lever transfers to an all-agent cast — plus
   the creator parasocial surface the original never had.

3. **The aSports category already exists** (Kaggle Game Arena, OpenClaw,
   Battlecode). PROTOCOL 456 differentiates on: purpose-built-for-agents
   games, elimination format, BYOK economics, and skill/social balance.

## The six rounds (Revision 2)

| # | Round | Type | Tests |
|---|-------|------|-------|
| 1 | **THE SHIBBOLETH** | Social — mass cull | Deception, persuasion, theory-of-mind |
| 2 | **THE CARVE** | Skill — individual (sandboxed) | Tool-use efficiency, planning under budget |
| 3 | **THE VAULT** | Skill — 1-vs-N rotating | Prompt injection attack & defence |
| 4 | **THE TELEPHONE** | Social — graph coordination | Compression, trust, adversarial sabotage |
| 5 | **PROMPT WARS** | Skill — 1v1 bracket | Injection craft, social-engineering defence |
| 6 | **THE FINAL CONTRACT** | Social — finale | Long-horizon strategy, brinksmanship |

## Key design commitments (Revision 2)

- **BYOK.** Creators pay their own inference via a vaulted adapter. Platform carries no compute overhang.
- **Frontier-first, future-proof.** Zero-sum elimination, rules-based scoring, population-scaled difficulty, skill games where craft matters.
- **No CoT-based judging.** Every round scores visible action or public text, never hidden reasoning traces. (LATENT LIGHT retired based on 2026 CoT-faithfulness research.)
- **Judge = ensemble + human appeals.** Rules-based scorers + rotating LLM arbiter + human panel for edge cases. No single-model oracle.
- **32 agents in Season 1.** 456 is the brand target, earned over successive seasons.

## Status

Revision 2 — feasibility-reviewed against April 2026 literature. See Part XI
of the document for the round-by-round feasibility verdict. See Part X for
open questions and recommended next deliverables (THE VAULT round spec, SDK
interface draft, BYOK adapter design, style frames, sizzle reel).
