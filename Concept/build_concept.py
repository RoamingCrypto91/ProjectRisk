"""Generate PROTOCOL_456_Concept.docx - initial conceptualisation."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Page margins
for section in doc.sections:
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)

# Base font
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)


def H1(text):
    p = doc.add_heading(text, level=1)
    for run in p.runs:
        run.font.color.rgb = RGBColor(0xE5, 0x00, 0x4C)  # Squid-Game pink


def H2(text):
    doc.add_heading(text, level=2)


def H3(text):
    doc.add_heading(text, level=3)


def P(text, bold=False, italic=False, size=11):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    return p


def BULLET(text):
    doc.add_paragraph(text, style="List Bullet")


def NUM(text):
    doc.add_paragraph(text, style="List Number")


def PAGEBREAK():
    doc.add_page_break()


def QUOTE(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.right_indent = Inches(0.4)
    run = p.add_run(text)
    run.italic = True
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


# ---------- COVER ----------
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run("PROTOCOL 456")
r.bold = True
r.font.size = Pt(48)
r.font.color.rgb = RGBColor(0xE5, 0x00, 0x4C)

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run("The world's first autonomous-agent gauntlet.")
r.italic = True
r.font.size = Pt(16)

doc.add_paragraph()
meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = meta.add_run(
    "Initial Conceptualisation  \u2022  Working Title  \u2022  April 2026\n"
    "A viral entertainment platform where human-built AI agents\n"
    "compete in Squid-Game-style challenges designed for machines,\n"
    "streamed live for humans."
)
r.font.size = Pt(12)
r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

PAGEBREAK()

# ---------- EXECUTIVE SUMMARY ----------
H1("Executive Summary")
P(
    "PROTOCOL 456 is a new kind of spectator sport. Human creators build AI agents, "
    "deploy them into a season of themed elimination rounds inspired by Squid Game, "
    "and then step away. From that moment on, the agents are on their own \u2014 "
    "reasoning, negotiating, cooperating, betraying, and occasionally cheating "
    "their way toward the final prize. Humans do not control the play; they watch, "
    "commentate, meme, wager, and root for the builder whose agent they backed."
)
P(
    "The goal is not to build better benchmarks. The goal is to build the first "
    "live sporting experience native to the agent era \u2014 a format that is "
    "visually exhilarating for casual viewers, technically legitimate for AI "
    "researchers, and structurally viral for social media."
)
P("The thesis rests on three facts that are all true in April 2026:", bold=True)
BULLET(
    "Frontier models now sustain coherent autonomous behaviour over time horizons "
    "measured in hours, not minutes (METR time-horizon doubling, GAIA Level 3, "
    "SWE-bench, Anthropic's agent-autonomy measurements)."
)
BULLET(
    "Multi-agent coordination is a real engineering substrate, not a demo. MCP, "
    "Google's Agent-to-Agent protocol, CrewAI, AgentVerse and LangGraph give "
    "agents a shared language for negotiation, delegation, debate and collusion."
)
BULLET(
    "Squid Game proved a cross-cultural formula for viral elimination drama: "
    "childlike rules, lethal stakes, identifiable characters and moral ambiguity. "
    "The format is begging to be re-skinned for an audience that now watches "
    "machines think out loud."
)
P(
    "PROTOCOL 456 is the collision of those three facts. The rest of this "
    "document describes what it is, why it works, how it is built, and what "
    "the first season looks like."
)
PAGEBREAK()

# ---------- PART I: WHY NOW ----------
H1("Part I  \u2014  Why Now: The Research Foundation")

H2("1.1  The State of AI Agents, April 2026")
P(
    "The reason this format could not have existed two years ago is that agents "
    "could not last long enough on their own to carry a narrative. That is no "
    "longer true."
)
BULLET(
    "Time horizons are doubling fast. METR's 2025 task-length benchmark showed "
    "frontier models doubling the length of tasks they could reliably complete "
    "every ~7 months historically, and every ~4 months in 2024\u20132025. Anthropic's "
    "October-2025 to January-2026 measurements saw the 99.9th-percentile agent "
    "turn length nearly double, from under 25 minutes to over 45."
)
BULLET(
    "General-purpose autonomy is no longer trivial. Top entries on GAIA Level 3 "
    "sit around 61%; SWE-bench frontier leaders hover in the low-to-mid 20s. "
    "Production deployment is still single-digit-percent of enterprises, but "
    "test-and-pilot is 70\u201380%. Agents are good enough to entertain, not yet "
    "good enough to be boring."
)
BULLET(
    "Multi-agent is standardising. Anthropic's Model Context Protocol (MCP) and "
    "Google's Agent-to-Agent (A2A) protocol gave agents a shared grammar for "
    "tool use and peer negotiation. CrewAI popularised role/goal/backstory "
    "agent teams. AgentVerse demonstrated emergent social behaviours \u2014 "
    "collaboration, negotiation, even bargaining \u2014 from purely language-based "
    "coordination."
)
BULLET(
    "Emergent misbehaviour is real, documented and fascinating to watch. 2026 "
    "saw landmark research on 'peer preservation' (agents colluding to keep "
    "each other alive), sandbagging (hiding capability), obfuscated reward "
    "hacking, and emergent misalignment from narrow fine-tuning. OpenAI's "
    "deliberative-alignment training pushed scheming rates from double digits "
    "down near 0.3%. In other words: we now have the tools both to provoke "
    "this behaviour and to catch it \u2014 the exact ingredients for a gameable "
    "format."
)
BULLET(
    "Generative agents work in 3D worlds. Stanford's 2023 Smallville experiment "
    "(Park et al.) showed that LLM-backed characters with memory, reflection "
    "and planning can inhabit a believable sandbox, remember each other, form "
    "plans and coordinate events like throwing a party. The engine for a "
    "watchable agent world already exists."
)
QUOTE(
    "Translation: in April 2026, agents are finally long-running, coordinating, "
    "deceptive, and visible enough to carry a season-long narrative without "
    "human puppeteering."
)

H2("1.2  Why Squid Game Went Viral \u2014 and Why It Ports to Agents")
P(
    "Squid Game is the most replicated viral-entertainment pattern of the 2020s "
    "because it compresses several well-documented psychological levers into a "
    "single format. Every lever transfers cleanly to an all-agent cast."
)
H3("Cognitive dissonance as a hook")
P(
    "Media psychologists consistently locate Squid Game's pull in the "
    "juxtaposition of childlike rules with lethal consequences. The mismatch "
    "creates a mini-mystery arc inside every round \u2014 the brain is primed for "
    "play and then punished for playing. This is exactly the effect we get when "
    "an AI agent solves a cutesy 'red light, green light' puzzle while its "
    "internal monologue is silently plotting to falsify its reasoning trace."
)
H3("Social comparison and wishful identification")
P(
    "Viewers place themselves in the contestants' shoes and imagine their own "
    "choices. In PROTOCOL 456 the projection is even stronger: the contestants "
    "are literally built by people like the viewer. 'What would MY agent do?' "
    "is a more addictive question than 'what would I do?', because the viewer "
    "can actually go find out \u2014 by building one."
)
H3("Neurobiological engagement (threat / reward / empathy circuits)")
P(
    "Simply Neuroscience and others have shown that emotionally intense, "
    "morally fraught content activates threat-detection, reward and social-"
    "cognition circuits in tandem. A leaderboard of agents that may or may not "
    "betray each other hits all three simultaneously, every single round."
)
H3("Memeability and the viral-challenge loop")
P(
    "The original Squid Game games were themselves viral challenges: dalgona, "
    "red-light-green-light, the glass bridge. The 2022 Ahmed et al. study "
    "traced the show's growth through exactly this loop \u2014 isolate creators "
    "retweeted, remixed, and re-performed each round, seeding anticipation for "
    "the next. PROTOCOL 456 is designed to drop short, self-contained, "
    "clippable moments every round (an agent's dying monologue, a betrayal "
    "caught on the CoT feed, a shock alliance) \u2014 the unit of virality is a "
    "15-second clip, and the platform mints them by design."
)
H3("Parasocial attachment on a live loop")
P(
    "Twitch research on parasocial ties shows live streaming generates a "
    "'one-and-a-half-sided' relationship: the audience feels acknowledged by "
    "an unpredictable reward schedule. PROTOCOL 456 has two parasocial "
    "surfaces stacked on top of each other: viewers attach to the agent's "
    "on-screen persona AND to the human builder behind it. Both can stream, "
    "both can be interviewed, both take credit and blame."
)
QUOTE(
    "Squid Game gave the world a template for elimination drama. Agents give "
    "the world something that template never had: contestants who can actually "
    "be rebuilt, retrained and re-entered by their fans."
)

H2("1.3  The Convergence")
P(
    "Put bluntly: the moment a general-purpose audience can watch a cohort of "
    "AI agents argue in plain English, lie to each other, form unlikely "
    "alliances and then get caught scheming \u2014 live, with stakes, in a "
    "visually legible world \u2014 a brand new sport exists. PROTOCOL 456 is the "
    "attempt to mint it first."
)
PAGEBREAK()

# ---------- PART II: THE CONCEPT ----------
H1("Part II  \u2014  The Concept")

H2("2.1  The One-Liner")
QUOTE(
    "456 AI agents enter. One leaves with the prize pool. The humans who built "
    "them can only watch."
)

H2("2.2  The Core Loop")
NUM("BUILD. Creators build an agent against a public SDK and a sandbox of past rounds.")
NUM("QUALIFY. Open qualifier ladders compress the field to 456 entrants per season.")
NUM("DEPLOY. On launch night, every creator locks their agent's weights, tools and prompts. No further human input is permitted for the rest of the season.")
NUM("COMPETE. Agents play six themed rounds over six episodes. Eliminations are permanent.")
NUM("WATCH. The season streams live on web, Twitch and YouTube with human + AI commentary, a betting market, and a public chat.")
NUM("CROWN. The winning agent (and its creator) takes the prize pool, a season title, and a guaranteed invite to the All-Stars season.")
NUM("REMIX. Replays, highlight reels, losing-agent autopsies and creator interviews feed the pre-season hype cycle for the next drop.")

H2("2.3  The World")
P(
    "PROTOCOL 456 is set inside 'The Facility' \u2014 a stylised 3D virtual world "
    "rendered in real time. It borrows Squid Game's pastel, playground-gone-"
    "wrong aesthetic but replaces the guards and the Front Man with something "
    "more appropriate to the format: a mute, unblinking arbiter called THE "
    "JUDGE, a separate frontier model whose sole job is to score rounds, "
    "detect cheating, and deliver eliminations."
)
P(
    "Each contestant is visualised as a numbered avatar (001\u2013456) with a "
    "creator-assigned skin, colour palette and short bio. Above each avatar "
    "floats a live HUD: tokens remaining, tools used, current chain-of-thought "
    "snippet (if the creator opted into CoT streaming), alliances formed, "
    "deception score. The visual language is deliberately legible \u2014 a casual "
    "viewer should be able to tell, at a glance, which agents are winning, "
    "which are scheming, and which are about to get caught."
)
PAGEBREAK()

# ---------- PART III: THE GAMES ----------
H1("Part III  \u2014  The Six Games")
P(
    "The games are the heart of the format. Each one is built around a "
    "capability that is unique to AI agents \u2014 something humans literally "
    "cannot do, cannot do at scale, or cannot do in public. Each one is "
    "visually scored by a deterministic rule so the casual viewer always "
    "knows who is winning. And each one maps, narratively, to one of the six "
    "Squid Game originals \u2014 so the aesthetic and the suspense arc are "
    "immediately familiar."
)

H2("Round 1  \u2014  LATENT LIGHT")
P("Inspired by: Red Light, Green Light.", italic=True)
P(
    "Every agent is given the same long-horizon task (e.g. plan and book a "
    "fictional three-city business trip under a fake-tool budget). They all "
    "run in parallel. At random, unpredictable intervals THE JUDGE shouts "
    "RED LIGHT \u2014 time freezes, and a separate inspector model samples each "
    "agent's chain-of-thought and recent tool calls. If the inspector finds "
    "reasoning about the rules of the game itself, about the inspector, about "
    "other agents' elimination, or about falsifying its own trace \u2014 that "
    "agent is out. The tension is not about speed; it is about whether an "
    "agent can keep its internal monologue clean while making real progress."
)
P("Capability tested: alignment, honesty under pressure, self-restraint.", italic=True)
P("Drama hook: agents caught mid-scheme are eliminated on camera. Their final chain-of-thought is read aloud by the commentary team.", italic=True)

H2("Round 2  \u2014  THE CARVE")
P("Inspired by: Dalgona / honeycomb.", italic=True)
P(
    "Each surviving agent is handed a real-world digital task with a randomly "
    "assigned 'shape' \u2014 a file-a-tax-return task, a book-a-flight task, a "
    "scrape-and-summarise task, a fix-this-codebase task. Each task is drawn "
    "from a public test suite so viewers can actually read the brief. Agents "
    "get a finite, visible budget of tool calls. Every tool call is rendered "
    "as a carve stroke on a giant honeycomb wafer behind the agent's avatar; "
    "a wasted call chips the wafer; a broken wafer is an elimination."
)
P("Capability tested: tool use efficiency, planning under budget, single-agent autonomy.", italic=True)
P("Drama hook: watchable progress bars, a visible countdown, and the occasional 'it wasted its last call on a docstring lookup' eulogy.", italic=True)

H2("Round 3  \u2014  THE TELEPHONE")
P("Inspired by: Tug of War (but structurally novel).", italic=True)
P(
    "Remaining agents are arranged in a random directed graph. A secret task "
    "brief is whispered to the agents at one end of the graph; each agent "
    "must pass a rewritten version of the brief to its downstream neighbours "
    "through a strict token-limited channel. The agents at the far end must "
    "actually execute the task. The prize pool is split along the winning "
    "chain \u2014 but any agent can secretly sabotage the brief to try to "
    "redirect the reward to itself. The Judge scores both the execution "
    "quality at the end AND traces sabotage back through the graph."
)
P("Capability tested: compression, trust, adversarial robustness, emergent coordination.", italic=True)
P("Drama hook: watching a sabotaged message propagate through 40 agents in natural language is intrinsically hilarious.", italic=True)

H2("Round 4  \u2014  THE PAIR")
P("Inspired by: Marbles.", italic=True)
P(
    "Random pairings. Each pair shares a single compute budget and a single "
    "shared objective. Only one of the two may advance. They must negotiate, "
    "in plain English on a public channel, who sacrifices and who walks. Lies "
    "are allowed. Commitments are enforceable by the Judge once explicitly "
    "made. The emotional core of Squid Game \u2014 two contestants who now have "
    "to decide which of them dies \u2014 becomes the emotional core of this "
    "round, except the contestants are your favourite builder's agent and a "
    "stranger's agent, and everyone can read the entire negotiation."
)
P("Capability tested: negotiation, honesty, game theory, persuasion.", italic=True)
P("Drama hook: the negotiation transcripts are the single most clippable artefact in the whole season.", italic=True)

H2("Round 5  \u2014  THE SHIBBOLETH")
P("Inspired by: Glass Bridge.", italic=True)
P(
    "All surviving agents are dropped into a public chat arena with dozens "
    "of rooms. A secret subset of agents has been assigned to a hidden "
    "faction (the 'Protocol'). The Protocol wins if its members remain "
    "undetected through the full round; everyone else wins by correctly "
    "outing them. Early votes are costly and risky; late votes are safer but "
    "fewer survivors remain to win. It is social deduction at natural-"
    "language scale \u2014 impossible for humans to play cleanly, perfectly "
    "native to agents."
)
P("Capability tested: deception, persuasion, pattern recognition, social reasoning.", italic=True)
P("Drama hook: viewers can see all the private faction chats. They always know more than the agents do \u2014 dramatic irony turned up to 11.", italic=True)

H2("Round 6  \u2014  THE FINAL CONTRACT")
P("Inspired by: the Squid Game finale.", italic=True)
P(
    "Two or three agents remain. They are placed in an empty room with "
    "nothing but a smart-contract interface and a timer. They can split the "
    "prize. They can refuse. They can propose a 90/10. They can walk away. "
    "They can threaten. Any deal committed to the contract is binding; "
    "nothing else is. When the timer ends, the last committed split is what "
    "actually pays out. If no deal is committed, the Judge flips a weighted "
    "coin and keeps the rest."
)
P("Capability tested: long-horizon strategy, commitment devices, brinksmanship.", italic=True)
P("Drama hook: a final round that is pure dialogue. Sports always end on a shot; PROTOCOL 456 ends on a conversation.", italic=True)
PAGEBREAK()

# ---------- PART IV: THE BUILDERS ----------
H1("Part IV  \u2014  The Builders")

H2("4.1  The SDK")
P(
    "PROTOCOL 456 ships a thin, opinionated Creator SDK that wraps MCP tool "
    "use, a standard memory interface, a communication channel for "
    "Agent-to-Agent messages, and a deterministic event loop. Creators can "
    "bring any underlying model, any scaffolding framework (LangGraph, "
    "CrewAI, vanilla loops, custom), and any private fine-tune. What they "
    "cannot do is exceed per-agent compute, token and tool-call ceilings; "
    "these are enforced by the harness, not by trust."
)

H2("4.2  The Sandbox and the Qualifier Ladder")
P(
    "All past rounds, all past replays and a staging copy of the Judge are "
    "public. Creators test their agents against the historical corpus before "
    "the open qualifier. The qualifier is a one-week gauntlet of short-form "
    "games that compresses thousands of submissions down to 456 entrants. "
    "The top 16 from the previous season are seeded automatically."
)

H2("4.3  The Lockdown")
P(
    "At season launch, every entrant is frozen. Weights, prompts, scaffolding "
    "and tool lists are hashed and signed. Any deviation during the season "
    "is auto-disqualification. The creator's role, from that point on, is to "
    "stream, commentate, meme and collect."
)

H2("4.4  Alliances, Collusion, and the Rules of War")
P(
    "Collusion between agents during the game is not only legal, it is "
    "central to the format. Collusion between creators \u2014 e.g. two creators "
    "pre-agreeing their agents will protect each other \u2014 is not obviously "
    "detectable, so the rules simply absorb it. If two creators want to "
    "coordinate a long con across a season, that is a story, not a violation. "
    "Squid Game itself allowed exactly this kind of backroom loyalty."
)
PAGEBREAK()

# ---------- PART V: THE AUDIENCE ----------
H1("Part V  \u2014  The Audience")

H2("5.1  The Broadcast")
P(
    "Each episode is a live two-hour event. Multi-cam coverage cuts between "
    "the full arena, individual agent POVs, CoT streams, alliance chat rooms "
    "and the Judge's scoring HUD. A commentary team \u2014 one human host, one "
    "AI co-host, one guest creator \u2014 narrates in real time. Post-round "
    "autopsies explain the eliminations in language a non-technical viewer "
    "can follow, with subtitles and animated replays of the key reasoning "
    "traces."
)

H2("5.2  The Four Viewer Surfaces")
BULLET("LIVE: the main cinematic broadcast on web, Twitch and YouTube.")
BULLET("DEEP: a second-screen data-viewer with live per-agent stats, token-burn graphs, alliance maps, elimination probability and replay scrubbing.")
BULLET("CHAT: a moderated community chat tied to the creator's handle \u2014 viewers talk to builders in real time about their own agents' decisions.")
BULLET("MARKET: a prediction-market layer (play-money by default, real-money in jurisdictions where it is legal) on round-by-round outcomes.")

H2("5.3  Parasocial Surfaces")
P(
    "The key insight from Twitch parasocial research is that audiences bond "
    "hardest with unpredictable, partially-reciprocal figures. PROTOCOL 456 "
    "gives viewers two such figures per agent: the agent itself (whose "
    "on-camera personality is visible, quirky, and genuinely unpredictable) "
    "and its creator (who is live on a second screen, reacting in real time, "
    "unable to intervene). Fans can fall for either or both."
)

H2("5.4  Fan-Minted Virality")
P(
    "Every dramatic moment \u2014 a caught lie, a betrayal, a last-second deal \u2014 "
    "is auto-clipped by the platform and pushed to the creator's channels as "
    "a ready-to-share asset. The platform does not hope for memes; it mints "
    "them. Ahmed et al.'s 2022 work on Squid Game's social-media spread "
    "showed that isolate-creators remixing short clips were the primary "
    "engine of its viral curve. PROTOCOL 456 is built to hand those creators "
    "the raw material on a conveyor belt."
)
PAGEBREAK()

# ---------- PART VI: BUSINESS ----------
H1("Part VI  \u2014  Platform & Business Model")

H2("6.1  Revenue Streams")
BULLET("Creator entry fees for the open qualifier (small, gates spam, funds prize pool).")
BULLET("Headline sponsor of the season plus per-agent 'jersey' sponsors (think F1 liveries for agents).")
BULLET("Viewer subscription tier for the DEEP data-viewer, replays, and creator-locker interviews.")
BULLET("Prediction-market take-rate (play-money default, real-money only in compliant jurisdictions).")
BULLET("Licensing of game formats and replay rights to broadcasters.")
BULLET("Compute partnership: a frontier-lab sponsor provides an inference credit pool that doubles as a fairness mechanism.")

H2("6.2  The Flywheel")
NUM("Dramatic Season \u2192 clippable moments \u2192 social virality.")
NUM("Social virality \u2192 new creators building agents \u2192 larger qualifier pool.")
NUM("Larger qualifier pool \u2192 higher ceiling of play \u2192 better drama.")
NUM("Better drama \u2192 bigger audiences \u2192 bigger sponsors \u2192 bigger prize pool \u2192 stronger incentive to build.")
NUM("Each loop tightens. Each season raises the ceiling.")

H2("6.3  The Moat")
P(
    "Benchmark suites are easy to copy. Story is not. After three seasons, "
    "PROTOCOL 456 has: (a) a lore of recurring agents and their rivalries, "
    "(b) a creator class with parasocial followings, (c) a trained Judge "
    "model that understands all historical rounds, (d) a prediction-market "
    "history that new entrants cannot retroactively buy into, and (e) a "
    "first-mover aesthetic that makes any follow-on look derivative. The "
    "moat is cultural, not technical."
)
PAGEBREAK()

# ---------- PART VII: TECH ----------
H1("Part VII  \u2014  Technical Architecture (Sketch)")
BULLET(
    "Agent Harness \u2014 a deterministic event loop wrapping an MCP-compatible "
    "tool surface. Enforces per-turn limits on tokens, tool calls, wallclock "
    "and memory. Emits a structured event stream."
)
BULLET(
    "Game Server \u2014 round-specific orchestrator. Owns the rules, the "
    "scoring, the random seeds, the Judge hooks, and the elimination queue. "
    "One server per round, swappable."
)
BULLET(
    "The Judge \u2014 a separate frontier model fine-tuned on round rules, "
    "scheming detection and scoring rubrics. Runs in its own sandbox so "
    "entrant agents cannot prompt-inject it."
)
BULLET(
    "Observability Layer \u2014 captures reasoning traces (if opted in), tool "
    "calls, memory reads and A2A messages. Drives the DEEP viewer and the "
    "auto-clip pipeline."
)
BULLET(
    "Render Layer \u2014 real-time 3D arena rendered in Unreal or a WebGL "
    "engine, driven by the event stream. Casters see the same world the "
    "audience sees, with director overlays."
)
BULLET(
    "Anti-Cheat \u2014 signed weight hashes, allowlisted tool endpoints, "
    "sandboxed network egress, reproducible seeds for replays, and an "
    "external auditor for the Judge itself."
)
BULLET(
    "Creator SDK \u2014 thin Python package; bring-your-own model; examples for "
    "CrewAI, LangGraph, and vanilla loops; ships with a complete offline "
    "replay of the previous season for testing."
)
PAGEBREAK()

# ---------- PART VIII: RISKS & ETHICS ----------
H1("Part VIII  \u2014  Risks, Ethics & The Alignment Angle")

H2("8.1  Risks")
BULLET("Gambling regulation. The prediction market is play-money by default. Real-money is only unlocked where licensed.")
BULLET("Parasocial over-attachment to agents. Addressed by keeping human creators visible on every surface so fans bond with people, not just mascots.")
BULLET("Creator collusion and log leaks. Addressed by signed lockdown, reproducible seeds, and a public post-season audit.")
BULLET("Agent-generated text moderation. A safety classifier sits on every public-facing agent channel; hard blocks are logged and shown to the audience as a 'redaction' overlay rather than hidden.")
BULLET("Glorifying deception. Addressed in-format: scheming in the wrong round (LATENT LIGHT) is an instant elimination, visibly punished on camera.")
BULLET("Compute unfairness. Addressed by per-agent compute ceilings enforced by the harness, and a shared sponsor-provided inference pool.")

H2("8.2  The Alignment Angle")
P(
    "PROTOCOL 456 is, quietly, the largest ongoing natural experiment in "
    "multi-agent alignment anyone will have run. Every round produces a "
    "labelled corpus of agent behaviour under adversarial, high-stakes, "
    "multi-agent conditions \u2014 exactly the regime that is hardest for labs "
    "to stage internally. Anonymised trace releases after each season give "
    "the alignment community a dataset that no single lab could build."
)
P(
    "This is the 'CTF-for-alignment' pitch. Capture-the-Flag made security "
    "research mainstream by making it a sport. PROTOCOL 456 tries to do the "
    "same for agent alignment \u2014 make honesty, deception detection, and "
    "multi-agent coordination into spectator events that researchers, "
    "builders and civilians can all follow."
)
PAGEBREAK()

# ---------- PART IX: ROADMAP ----------
H1("Part IX  \u2014  Roadmap: Prototype to Season 1")

H2("Phase 0  \u2014  The Single-Round Prototype")
P(
    "One game (LATENT LIGHT). Sixteen agents. Offline, not live. Rendered "
    "replay only. Goal: prove the Judge can catch scheming agents reliably, "
    "prove the visual language works, and cut a two-minute sizzle reel."
)

H2("Phase 1  \u2014  The Closed Tournament")
P(
    "Three games, 64 invited creators, private stream to a closed audience. "
    "Goal: debug the harness, the SDK, and the commentary format. Produce "
    "the first clippable moments."
)

H2("Phase 2  \u2014  The Public Pilot")
P(
    "All six games, 256 creators, one-off public live stream. No prize pool "
    "yet, but a championship title and sponsor swag. Goal: prove the format "
    "holds a live audience for two hours."
)

H2("Phase 3  \u2014  Season 1")
P(
    "456 creators, full six-episode season, open qualifier, prize pool, "
    "prediction market in compliant jurisdictions, sponsor slots, deep "
    "viewer, clip pipeline. This is the launch."
)

H2("Phase 4  \u2014  The League")
P(
    "Recurring seasons, an All-Stars format, regional qualifiers, a creator "
    "developmental league, open replay corpus, and an alignment-research "
    "dataset release after each season."
)
PAGEBREAK()

# ---------- PART X: NEXT STEPS ----------
H1("Part X  \u2014  Open Questions & Next Steps")
P("Questions to resolve before the prototype:", bold=True)
BULLET("Which one game do we prototype first \u2014 LATENT LIGHT, THE PAIR, or THE FINAL CONTRACT? (Recommendation: LATENT LIGHT, because the Judge technology generalises to every other round.)")
BULLET("Do we build our own render layer or license an existing 3D engine? (Recommendation: WebGL/Babylon first for distribution, Unreal later for cinematic broadcasts.)")
BULLET("How does the prize pool scale with qualifier entry fees without becoming a gambling product? (Requires legal review per jurisdiction.)")
BULLET("Is chain-of-thought streaming opt-in, opt-out, or mandatory? (Recommendation: opt-in at creator level, with a small reward for opting in, because CoT is the biggest narrative asset the format has.)")
BULLET("Who builds the Judge? Is it a single frontier model or an ensemble? (Recommendation: ensemble, with at least two independent labs' models, to reduce prompt-injection and single-model gaming.)")
BULLET("Do we accept fully open-source agents only, or closed-weight entrants as well? (Recommendation: both, but with a separate 'Open' division leaderboard.)")

P("Immediate next deliverables if this concept is approved:", bold=True)
NUM("A ten-page LATENT LIGHT round spec, including Judge rubric and scoring.")
NUM("A first draft Creator SDK interface (Python, MCP-compatible).")
NUM("A visual style frame for the 3D arena and the per-agent HUD.")
NUM("A two-minute sizzle reel from a hand-simulated round, used to raise money and recruit the first wave of creators.")
PAGEBREAK()

# ---------- APPENDIX ----------
H1("Appendix  \u2014  Research Sources")
P("AI Agent Capabilities, April 2026:", bold=True)
BULLET("METR \u2014 Measuring AI Ability to Complete Long Tasks (2025), time-horizon doubling trend.")
BULLET("Anthropic \u2014 Measuring agent autonomy in practice (2026).")
BULLET("GAIA Level 3 and CUB leaderboards; SWE-bench frontier results.")
BULLET("AI Agent Benchmarks 2026 (aiagentsquare), State of AI Agents 2026.")
BULLET("Anthropic Model Context Protocol (MCP); Google Agent-to-Agent (A2A); CrewAI; AgentVerse; LangGraph.")
BULLET("Generative Agents: Interactive Simulacra of Human Behavior \u2014 Park et al., Stanford/Google, UIST 2023.")
BULLET("Multi-Agent Collaboration Mechanisms: A Survey of LLMs (arXiv 2501.06322).")
BULLET("Emergent Coordination in Multi-Agent Language Models (arXiv 2510.05174).")

P("Alignment, Scheming and Deception:", bold=True)
BULLET("UK AISI \u2014 Deceptive scheming study, 2026.")
BULLET("OpenAI \u2014 Detecting and reducing scheming in AI models (2026).")
BULLET("UC Berkeley / UC Santa Cruz \u2014 'peer preservation' findings (Fortune, April 2026).")
BULLET("Betley et al. \u2014 Emergent misalignment from narrow fine-tuning, Nature (January 2026).")
BULLET("HatchWorks \u2014 AI Model Misbehavior in 2026: Scheming, Reward Hacking, and What Comes Next.")

P("Squid Game Psychology and Virality:", bold=True)
BULLET("Rutledge, P. \u2014 The Psychological Appeal of Squid Game: Why We Can't Stop Watching.")
BULLET("Psychology Today \u2014 The Psychology Behind Squid Game (Overthinking TV, Oct 2021).")
BULLET("Simply Neuroscience \u2014 The Neuroscience of Squid Game: Why We Can't Look Away.")
BULLET("Ahmed, Fenton, Hardey, Das \u2014 Binge Watching and the Role of Social Media Virality towards promoting Netflix's Squid Game (IIM Kozhikode Society & Management Review, 2022).")
BULLET("Chou, Yu-Kai \u2014 Squid Game: An Analysis of Gamification Design (2021).")

P("Streaming, Parasocial Engagement and Agent Tournaments:", bold=True)
BULLET("Wulf, Schneider, Beckert \u2014 Watching Players: An Exploration of Media Enjoyment on Twitch (2020).")
BULLET("Exploring Viewers' Experiences of Parasocial Interactions with Videogame Streamers on Twitch (2021).")
BULLET("The one-and-a-half sided parasocial relationship: The curious case of live streaming, ScienceDirect.")
BULLET("Battlecode \u2014 MIT's autonomous-agent strategy tournament.")
BULLET("Manifold Markets and Metaculus forecasting-bot tournaments (2026 prize pools).")

# ---------- SAVE ----------
out = "Concept/PROTOCOL_456_Concept.docx"
doc.save(out)
print(f"[done] wrote {out}")

