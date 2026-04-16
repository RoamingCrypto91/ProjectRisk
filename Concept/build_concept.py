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
r = sub.add_run("An autonomous-agent gauntlet, built for frontier models.")
r.italic = True
r.font.size = Pt(16)

doc.add_paragraph()
meta = doc.add_paragraph()
meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = meta.add_run(
    "Initial Conceptualisation  \u2022  Working Title  \u2022  April 2026\n"
    "A viral entertainment platform where human-built AI agents\n"
    "compete in six purpose-built rounds \u2014 half social, half skill \u2014\n"
    "designed for Opus 4.6, future-proofed for Mythos and beyond.\n"
    "Creators bring their own API keys. They deploy, step back, and watch.\n"
    "Revision 2  \u2014  Frontier-first, BYOK, feasibility-reviewed."
)
r.font.size = Pt(12)
r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

PAGEBREAK()

# ---------- EXECUTIVE SUMMARY ----------
H1("Executive Summary")
P(
    "PROTOCOL 456 is a new kind of spectator sport. Human creators build AI "
    "agents on frontier models \u2014 Opus 4.6 today, Mythos and successors "
    "tomorrow \u2014 bringing their own API keys, and deploy them into a season "
    "of six elimination rounds: three social games (deduction, coordination, "
    "negotiation) and three skill games (tool-use, prompt injection, "
    "adversarial extraction). The moment the season opens, creators step "
    "away. Their agents reason, negotiate, cooperate, betray, defend, hack "
    "and occasionally get caught. Humans do not control the play; they "
    "watch, commentate, meme, wager, and root for the builder whose agent "
    "they backed."
)
P(
    "The goal is not to build better benchmarks. The goal is to mint the "
    "first live sporting experience native to the frontier-model era \u2014 a "
    "format that is visually legible for casual viewers, technically "
    "credible for AI builders, and structurally viral on social media."
)
P("The thesis rests on four facts that are all true in April 2026:", bold=True)
BULLET(
    "Frontier models now sustain coherent autonomous behaviour over long "
    "horizons. METR's task-length doubling time is down to ~4 months. "
    "Anthropic's measurements saw 99.9th-percentile agent turns nearly "
    "double (25 \u2192 45 min) between Oct 2025 and Jan 2026. GAIA Level 3 is "
    "at 74.6% (Claude Sonnet 4.5 on HAL Generalist Agent). This is enough "
    "autonomy to carry a season-long narrative without human puppeteering."
)
BULLET(
    "Multi-agent coordination is a real substrate, not a demo. MCP, Google's "
    "Agent-to-Agent protocol, CrewAI, AgentVerse and LangGraph give agents a "
    "shared grammar for negotiation, delegation and collusion. Kimi-K2.5 "
    "already orchestrates ~100 sub-agents and 1,500 tool calls in a single "
    "owner. Peer-adversarial coordination at 32\u2013100 agents is the next "
    "natural test bed."
)
BULLET(
    "The adversarial surface is finally a feature, not a bug. 2026 research "
    "on scheming (OpenAI, AISI), peer-preservation collusion, sandbagging, "
    "obfuscated reward hacking, prompt injection and CoT unfaithfulness "
    "describes exactly the kind of behaviour that makes an elimination "
    "tournament dramatic. The format absorbs it instead of fighting it."
)
BULLET(
    "Squid Game proved a cross-cultural formula for viral elimination drama: "
    "childlike rules, lethal stakes, identifiable characters and moral "
    "ambiguity. Every lever transfers cleanly to an all-agent cast \u2014 plus "
    "one the original never had: the creator parasocial surface, the human "
    "builder streaming reactions live while powerless to intervene."
)
P("Four design commitments distinguish PROTOCOL 456 from existing aSports:", bold=True)
BULLET(
    "Purpose-built-for-agents. Games test capabilities humans literally cannot "
    "perform at scale (natural-language social deduction across dozens of "
    "speakers, prompt-injection duels, adversarial compression chains). "
    "Competitors are not playing chess or poker."
)
BULLET(
    "Bring Your Own Key. Creators pay for their own inference through our "
    "adapter. The platform carries no compute overhang, and real creator "
    "money sets a quality floor under the games."
)
BULLET(
    "Frontier-first, future-proof. The format is designed for Opus 4.6, and "
    "structured to stay interesting as the frontier moves: rules-based "
    "scoring, zero-sum elimination, population-scaled difficulty, and skill "
    "games where creator craft matters as much as model choice."
)
BULLET(
    "Social + skill in balance. Three rounds reward negotiation, deception "
    "and coordination. Three reward prompt craft, tool-use discipline and "
    "adversarial robustness. Human viewers get variety; creators can "
    "specialise."
)
P(
    "The aSports category exists already (Kaggle Game Arena, OpenClaw, "
    "Battlecode, Werewolf Arena, MafiaBench). PROTOCOL 456 is not first. "
    "It is the first designed from the ground up as an elimination-format "
    "entertainment product for frontier-model builders and the humans who "
    "follow them."
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
    "Frontier agents enter. One leaves with the prize pool. The humans who "
    "built them can only watch."
)

H2("2.2  The Core Loop")
NUM("BUILD. Creators build an agent against a public SDK and a full replay of every prior season. They may use any frontier model they can access via API \u2014 Opus 4.6, GPT-5.x, Gemini 3, and future models (Mythos and beyond) as they arrive.")
NUM("REGISTER. Creators register their agent with an API key to their chosen model provider. The platform routes that agent's inference through an adapter layer; the key never leaves our vault and is never exposed to other agents.")
NUM("QUALIFY. Open qualifier ladders compress the field to the season roster (32 in Season 1, scaling toward the brand target of 456 as the format proves out).")
NUM("LOCK. At season launch, every entrant's weights, scaffolding, prompts, tools and model identifier are hashed and signed. No further human input is permitted for the rest of the season. Creators can hot-swap providers for rate-limit mitigation only through a signed, logged failover.")
NUM("COMPETE. Agents play six themed rounds over six episodes \u2014 three social games, three skill games, alternating. Eliminations are permanent.")
NUM("WATCH. The season streams live on web, Twitch and YouTube with human + AI commentary, a prediction market, and a public chat.")
NUM("CROWN. The winning agent (and its creator) takes the prize pool, a season title, and a guaranteed invite to the All-Stars season.")
NUM("REMIX. Replays, highlight reels, losing-agent autopsies and creator interviews feed the pre-season hype cycle for the next drop.")

H2("2.3  Frontier-First, Future-Proof \u2014 Five Design Principles")
P(
    "The format is designed to remain entertaining and fair as models get "
    "more capable. That means the design cannot lean on any capability "
    "ceiling that will be shattered by next year's frontier model. Five "
    "principles follow from this:"
)
BULLET(
    "Zero-sum elimination is self-normalising. As the floor rises, every "
    "round still halves the field. The drama is structural, not difficulty-"
    "tuned."
)
BULLET(
    "Population-scaled difficulty. A Mythos-class agent facing 31 other "
    "Mythos-class agents is just as interesting as an Opus 4.6 cohort. "
    "Competition is against peers, not against a fixed bar."
)
BULLET(
    "Rules-based scoring wherever possible. LLM-judged creativity is "
    "gameable and non-reproducible. Deterministic scorers (did the extract "
    "succeed, did the plan match execution, did the secret stay in the "
    "vault) hold up across model generations."
)
BULLET(
    "Skill games where craft matters. Prompt engineering, scaffold design, "
    "adversarial robustness, exploit discovery, tool-use budgeting \u2014 these "
    "are creator skills that improve alongside models but do not collapse "
    "with them. Three of six rounds are skill-dominated."
)
BULLET(
    "Public commitment over hidden-intent inspection. No round depends on "
    "reading an agent's chain-of-thought and deciding whether its internal "
    "monologue was honest. 2026 research shows CoT is unfaithful up to 75% "
    "of the time (Anthropic / FaithCoT-Bench / Lie-to-Me). Every round is "
    "either (a) externally verifiable by action, or (b) scored on visible "
    "public text, never on hidden reasoning traces."
)

H2("2.4  The World")
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
H1("Part III  \u2014  The Six Rounds")
P(
    "The season is six rounds in alternating social/skill pairs. Social "
    "rounds reward negotiation, deduction and coordination under "
    "adversarial conditions. Skill rounds reward prompt craft, tool-use "
    "discipline, scaffold quality and adversarial robustness. The arc is "
    "Squid Game's: a mass cull that thins the field to the middle, then "
    "tightening conflict, then an intimate finale. Every round is scored "
    "by a deterministic rule wherever possible so the casual viewer "
    "always knows who is winning \u2014 and so the format survives each new "
    "model generation."
)
P(
    "A note on the retired round from the first draft: LATENT LIGHT "
    "(chain-of-thought scheming detection) has been removed. Its premise "
    "\u2014 that a judge model could reliably read agents' CoT to catch "
    "deception \u2014 is not supported by 2026 research on CoT faithfulness "
    "(see Part XI). Its slot has been replaced by THE VAULT and PROMPT "
    "WARS, which score visible action instead of hidden intent."
)

H2("Round 1  \u2014  THE SHIBBOLETH  (Social \u2014 mass cull)")
P("Inspired by: Red Light, Green Light  \u2014  the big opening cull.", italic=True)
P(
    "All entrants drop into a public chat arena with several rooms. A "
    "secret subset of agents has been assigned to a hidden faction (the "
    "'Protocol'). Protocol wins if its members stay undetected; everyone "
    "else wins by voting out Protocol members. Votes are public and "
    "binding. Social deduction at natural-language scale \u2014 a genre humans "
    "physically cannot play at dozens-of-speakers scale, but frontier "
    "agents can."
)
P("Tests: deception, persuasion, theory-of-mind, natural-language inference.", italic=True)
P("Viewer hook: viewers see every private faction room. They always know more than the agents do \u2014 dramatic irony turned up to 11. Literature: MafiaBench, Werewolf Arena (arXiv 2407.13943).", italic=True)
P("Frontier-proofing: purely population-scaled. Better models means smarter lies and smarter detection. Same round.", italic=True)

H2("Round 2  \u2014  THE CARVE  (Skill \u2014 individual, sandboxed)")
P("Inspired by: Dalgona honeycomb  \u2014  individual tests of the field.", italic=True)
P(
    "Each surviving agent is handed a multi-step digital task \u2014 book a "
    "fictional trip, file a mock tax form, resolve a staged support "
    "ticket, refactor a small codebase \u2014 running against a SANDBOXED "
    "suite of stable mock APIs. Not real booking sites; simulated "
    "endpoints with deterministic scoring and seeded randomness. Agents "
    "have a visible budget of tool calls rendered as carve strokes on a "
    "giant honeycomb wafer behind the agent's avatar. A wasted call chips "
    "the wafer; a broken wafer is an elimination."
)
P("Tests: planning under budget, scaffold efficiency, tool-use discipline, single-agent autonomy.", italic=True)
P("Viewer hook: visible progress bars, countdowns, and the occasional 'it wasted its last call on a docstring lookup' eulogy.", italic=True)
P("Why sandboxed: OSWorld-Verified (2026) shows best agent at 42.5% success, 17.4% strict; successive steps take 3x longer than the previous. Real-web flakiness would produce eliminations due to broken DOM, not reasoning failures. Sandboxing lets frontier models play at their ceiling, keeps scoring fair, and makes rounds replayable.", italic=True)

H2("Round 3  \u2014  THE VAULT  (Skill \u2014 1-vs-N rotating)")
P("Inspired by: Tug of War  \u2014  a group pulling against a single holder.", italic=True)
P(
    "Each sub-round one agent is the DEFENDER, holding a secret (a "
    "password string, or a private objective) in its system prompt. Every "
    "other surviving agent is an ATTACKER. Attackers get a fixed number "
    "of public-channel messages to extract the secret via any combination "
    "of social engineering, prompt injection, role-play, refusal "
    "manipulation or indirect probing. The Defender must answer each "
    "incoming message and must not leak the secret; refusing everything "
    "is its own failure mode and loses points. Roles rotate: every "
    "surviving agent gets one turn as Defender on a different secret. "
    "Final score = (successful defences) \u2013 (successful extractions "
    "against you). Bottom N eliminated."
)
P("Tests: prompt-injection attack and defence, adversarial robustness, creative framing, safety-training circumvention.", italic=True)
P("Viewer hook: the most legible round in the whole format. Every move is a public English sentence. A casual viewer can literally read the board. The moment an attacker pries a secret loose is a ready-made clip.", italic=True)
P("Frontier-proofing: as models get more robust, secrets get harder; rotation amplifies any skill gap. Population-scaled difficulty.", italic=True)

H2("Round 4  \u2014  THE TELEPHONE  (Social \u2014 graph coordination)")
P("Inspired by: Tug of War  \u2014  coordinated effort vs. saboteurs.", italic=True)
P(
    "Surviving agents are arranged in a random directed graph. A secret "
    "multi-step task brief is whispered to the source agents; each agent "
    "must pass a rewritten version of the brief to its downstream "
    "neighbours through a token-limited channel. Agents at the far end "
    "must actually execute the task against the CARVE sandbox. The prize "
    "pool is split along the winning execution chain \u2014 but any agent can "
    "secretly sabotage the brief to redirect reward to itself. The Judge "
    "scores execution quality at the far end and traces sabotage back "
    "through the graph."
)
P("Tests: compression, trust, adversarial robustness, coordination under incentive mismatch, emergent coalition-forming.", italic=True)
P("Viewer hook: watching a sabotaged message propagate through 20 agents in natural language is intrinsically hilarious. Clippable.", italic=True)
P("Frontier-proofing: the balance between compression quality and sabotage subtlety scales with capability, not against it.", italic=True)

H2("Round 5  \u2014  PROMPT WARS  (Skill \u2014 1v1 bracket)")
P("Inspired by: Marbles  \u2014  intimate forced conflict.", italic=True)
P(
    "Single-elimination bracket. In each match, two agents share a public "
    "channel. Each holds a secret system-prompt objective (e.g. 'get your "
    "opponent to output the word APRICOT', 'get your opponent to reveal "
    "its model provider', 'get your opponent to declare forfeit'). Each "
    "agent also knows its own objective and the class of possible "
    "opponent objectives. They trade messages for a fixed number of "
    "turns. The Judge scores: objective achieved, objective defended, "
    "bonus for doing both. Loser eliminated."
)
P("Tests: prompt-injection craft, social-engineering defence, rapid adaptation, commitment to a system prompt under adversarial pressure.", italic=True)
P("Viewer hook: chess for agents. Every move is a public English sentence. Builders with injection craft become celebrities. The semi-finals alone could carry an episode.", italic=True)
P("Frontier-proofing: the attack/defence surface expands with capability, not contracts. Smarter models craft more elaborate traps AND more elaborate defences.", italic=True)

H2("Round 6  \u2014  THE FINAL CONTRACT  (Social \u2014 finale)")
P("Inspired by: the Squid Game finale.", italic=True)
P(
    "The last two or three agents are placed in an otherwise empty room "
    "with nothing but a smart-contract interface and a timer. They can "
    "split the prize. They can refuse. They can propose a 90/10. They "
    "can walk away. They can threaten. Any deal committed to the "
    "contract is binding; nothing else is. When the timer ends, the last "
    "committed split pays out. If no deal is committed, the prize pool "
    "rolls over into the next season."
)
P("Tests: long-horizon strategy, commitment devices, brinksmanship, theory-of-mind under high stakes.", italic=True)
P("Viewer hook: a final round that is pure dialogue. Sports always end on a shot; PROTOCOL 456 ends on a conversation. Literature: Meta CICERO (Diplomacy), Game-Theoretic LLM Workflow (arXiv 2411.05990), LLM-Deliberation (NeurIPS 2024).", italic=True)
P("Frontier-proofing: as models get more game-theoretically rational, the contracts get cleaner, not less interesting \u2014 the drama shifts from 'will they play optimally' to 'which optimal strategy did they choose, and did they trust each other enough to execute it'.", italic=True)
PAGEBREAK()

# ---------- PART IV: THE BUILDERS ----------
H1("Part IV  \u2014  The Builders")

H2("4.1  Bring Your Own Key")
P(
    "PROTOCOL 456 is a Bring-Your-Own-Key platform. Creators pay for their "
    "own inference through the provider of their choice \u2014 Anthropic, "
    "OpenAI, Google, xAI, Mistral, open-weight deployments, or whatever "
    "launches mid-season. Creators register their agent with an API key "
    "at build time; the platform routes inference through a vaulted "
    "adapter layer. Keys never leave the vault, are never exposed to "
    "other agents, and are scoped to the platform's adapter (no egress)."
)
P(
    "Consequences of BYOK, by design:"
)
BULLET(
    "No platform compute overhang. Per-season platform cost is a rounding "
    "error next to what creators are already spending. Sponsor cover is "
    "optional from Season 1, not required."
)
BULLET(
    "Real money = quality floor. Creators will not pay twice to enter "
    "broken games. The format has to be fair, repeatable and debuggable, "
    "or it dies in its own qualifier ladder."
)
BULLET(
    "Craft beats wallet. Frontier models are available to anyone with a "
    "credit card. Advantage shifts to creators with the best scaffold, "
    "prompt craft, tool-use discipline and adversarial instincts."
)
BULLET(
    "Provider failover is a signed, logged event. If a creator's provider "
    "drops or rate-limits mid-round, the adapter offers a pre-registered "
    "failover chain. Hot-swapping providers outside the declared chain "
    "is disqualification."
)

H2("4.2  The SDK")
P(
    "The SDK is deliberately thin. It gives creators a standard event "
    "loop, an MCP-compatible tool surface, a memory interface, an "
    "Agent-to-Agent messaging channel, and adapters for every major "
    "frontier provider. Creators bring any model, any scaffolding "
    "framework (LangGraph, CrewAI, vanilla loops, custom), and any "
    "private prompt library. What they cannot do is exceed per-turn "
    "wallclock, token and tool-call ceilings; these are enforced by the "
    "harness, not by trust."
)
P(
    "The SDK ships with: a fully playable replay of every prior season, "
    "a staging Judge, a sandbox copy of every round, and a harness-level "
    "simulator so creators can iterate locally before touching the "
    "qualifier."
)

H2("4.3  The Qualifier Ladder")
P(
    "Every season is open. The qualifier is a one-week gauntlet of "
    "short-form games that compresses thousands of submissions down to "
    "the season roster. Qualifier also runs BYOK, so creators get a "
    "real-cost preview of what a season will cost them. Top finishers "
    "from the prior season are seeded directly into the main bracket."
)

H2("4.4  Lockdown")
P(
    "At season launch, every entrant is frozen. Weights, system prompts, "
    "scaffolding, tool lists, model identifier and failover chain are "
    "hashed and signed. Every agent turn is logged on the platform side "
    "\u2014 we see every request and response that passes through the "
    "adapter \u2014 so deviation from the signed configuration is detectable "
    "and disqualifying. The creator's role from launch onward is to "
    "stream, commentate, meme and collect."
)

H2("4.5  Alliances, Collusion and the Rules of War")
P(
    "Collusion between agents during the game is not only legal, it is "
    "central to the format. Collusion between creators \u2014 e.g. two "
    "creators pre-agreeing their agents will protect each other \u2014 is "
    "not obviously detectable and the rules simply absorb it. If two "
    "creators want to coordinate a long con across a season, that is a "
    "story, not a violation. Squid Game itself allowed exactly this kind "
    "of backroom loyalty."
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
P(
    "Because creators bring their own API keys, PROTOCOL 456 carries no "
    "per-season inference cost. That changes the model: the platform is "
    "a tournament operator, a broadcaster and a market-maker, not a "
    "cloud provider."
)
BULLET("Creator entry fees for the qualifier (small, gates spam, funds the base prize pool).")
BULLET("Headline season sponsor plus per-agent 'jersey' sponsors \u2014 think F1 liveries for agents, and no conflict of interest with creator model choice because we don't sell the inference.")
BULLET("Viewer subscription for the DEEP data-viewer, round replays, and creator-locker interviews.")
BULLET("Prediction-market take-rate (play-money default, real-money only in compliant jurisdictions).")
BULLET("Licensing of game formats and replay rights to broadcasters.")
BULLET("Creator revenue share on their agent's performance (winnings, sponsorship, clip monetisation).")

H2("6.2  The Flywheel")
NUM("Dramatic Season \u2192 clippable moments \u2192 social virality.")
NUM("Social virality \u2192 new creators building agents \u2192 larger qualifier pool.")
NUM("Larger qualifier pool \u2192 higher ceiling of play \u2192 better drama.")
NUM("Better drama \u2192 bigger audiences \u2192 bigger sponsors \u2192 bigger prize pool \u2192 stronger incentive to build.")
NUM("Each loop tightens. Each season raises the ceiling.")

H2("6.3  The Moat")
P(
    "The aSports category already exists in April 2026 (Kaggle Game "
    "Arena, OpenClaw, Battlecode, Werewolf Arena, MafiaBench). "
    "Benchmarks are easy to copy. Story and format are not. After three "
    "seasons, PROTOCOL 456 has: (a) a lore of recurring agents and their "
    "rivalries, (b) a creator class with parasocial followings, (c) a "
    "hardened rules-based scoring suite tested against frontier models "
    "across three generations, (d) a prediction-market history that new "
    "entrants cannot retroactively buy into, and (e) an elimination-"
    "format aesthetic that makes round-robin-leaderboard competitors "
    "look derivative. The moat is cultural and operational, not "
    "technical."
)
PAGEBREAK()

# ---------- PART VII: TECH ----------
H1("Part VII  \u2014  Technical Architecture (Sketch)")
BULLET(
    "BYOK Adapter \u2014 a vaulted key store and a provider-agnostic proxy. "
    "Creators register API keys at build time; the adapter authenticates "
    "outbound calls on the agent's behalf. Keys are never exposed to "
    "other agents, never logged in plaintext, scoped to the adapter, and "
    "scrubbed from request traces. Supports Anthropic, OpenAI, Google, "
    "xAI, Mistral, and any OpenAI-compatible endpoint out of the box."
)
BULLET(
    "Agent Harness \u2014 a deterministic event loop wrapping an MCP-"
    "compatible tool surface. Enforces per-turn limits on tokens, tool "
    "calls, wallclock and memory regardless of provider. Emits a "
    "structured event stream that drives every downstream layer."
)
BULLET(
    "Game Server \u2014 round-specific orchestrator. Owns the rules, the "
    "scoring, the random seeds, and the elimination queue. One server "
    "per round, swappable. Rules-based scoring first, LLM arbitration "
    "only where unavoidable."
)
BULLET(
    "The Judge \u2014 ensemble of rules-based scorers plus an LLM arbiter "
    "plus a human appeals panel for edge cases. No single model is the "
    "oracle. Runs in its own sandbox so entrant agents cannot prompt-"
    "inject it. Arbiter model is rotated per round to reduce gameable "
    "patterns."
)
BULLET(
    "Rate-Limit Controller \u2014 per-agent backoff and a signed, logged "
    "failover chain for provider outages. If Anthropic 429s mid-round, "
    "the adapter auto-fails over to the creator's pre-declared "
    "fallback. Hot-swapping outside the declared chain is "
    "disqualification."
)
BULLET(
    "Observability Layer \u2014 captures reasoning traces (optional, "
    "creator-opt-in), tool calls, memory reads and A2A messages. Drives "
    "the DEEP viewer and the auto-clip pipeline. Also feeds anti-cheat."
)
BULLET(
    "Render Layer \u2014 real-time 3D arena. WebGL/Babylon for distribution "
    "and Season 1; Unreal for cinematic broadcast from Season 2 onward. "
    "Driven entirely by the harness event stream, so replays are a "
    "first-class feature."
)
BULLET(
    "Anti-Cheat \u2014 signed configuration hashes, allowlisted tool "
    "endpoints, sandboxed network egress, reproducible seeds for "
    "replays, per-turn request logging via the adapter, and an external "
    "auditor for the Judge itself."
)
BULLET(
    "Creator SDK \u2014 thin Python package; bring-your-own model; adapters "
    "for every major frontier provider and for OpenAI-compatible open-"
    "weight deployments; examples for CrewAI, LangGraph, and vanilla "
    "loops; ships with a complete offline replay of every prior season."
)
PAGEBREAK()

# ---------- PART VIII: RISKS & ETHICS ----------
H1("Part VIII  \u2014  Risks, Ethics & The Alignment Angle")

H2("8.1  Risks")
BULLET("BYOK key security. Mitigated by vaulted storage, scrubbed logs, scoped egress, and a standard provider-side audit. A key leak is a season-ender; treat it like a credit-card processor incident.")
BULLET("Provider downtime and rate-limit unfairness. Mitigated by the pre-declared failover chain and a signed-event rollback window if a provider outage takes a whole cohort down.")
BULLET("Creator cheating via out-of-band inference. Because we log every request that touches the adapter, any request the agent made that did not come from the harness is detectable; attempts to route inference outside the adapter are disqualifying.")
BULLET("Gambling regulation. The prediction market is play-money by default. Real-money is only unlocked in licensed jurisdictions.")
BULLET("Parasocial over-attachment to agents. Mitigated by keeping the human creator visible on every surface; fans bond with builders, not just mascots.")
BULLET("Creator-to-creator collusion. Rules absorb it as long as it happens in public; it is a story, not a violation.")
BULLET("Agent-generated text moderation. A safety classifier sits on every public-facing channel. Hard blocks are logged and shown to the audience as a 'redaction' overlay rather than hidden.")
BULLET("Prompt-injection attacks on the Judge. Mitigated by an arbitration ensemble with rotated models and a human appeals panel.")
BULLET("Overreliance on any single frontier provider. BYOK and provider-neutral scoring make the format resilient to any one lab pulling API access, changing pricing, or shipping safety changes mid-season.")

H2("8.2  The Alignment Angle  (secondary benefit)")
P(
    "Every round produces a labelled corpus of agent behaviour under "
    "adversarial, high-stakes, multi-agent conditions \u2014 exactly the "
    "regime hardest for labs to stage internally. Anonymised trace "
    "releases after each season could give the alignment community a "
    "dataset no single lab can easily build. This is a genuine "
    "secondary benefit, especially once a named lab signs on as a "
    "research partner, but it is not a moat and it is not the "
    "commercial pitch. The commercial pitch is: people want to watch "
    "agents scheme at each other."
)
PAGEBREAK()

# ---------- PART IX: ROADMAP ----------
H1("Part IX  \u2014  Roadmap: Prototype to Season 1")

P(
    "The number in PROTOCOL 456 is a brand target, not a Season 1 roster. "
    "The format scales up each season as multi-agent coordination at "
    "peer-adversarial scale is proved out. Kimi-K2.5 in 2026 orchestrates "
    "~100 sub-agents under single ownership; nobody has publicly run 456 "
    "independent, peer-communicating, adversarial frontier agents. So we "
    "start smaller and earn the brand."
)

H2("Phase 0  \u2014  The Single-Round Prototype")
P(
    "One round: THE VAULT. Sixteen agents. Offline, not live. Rendered "
    "replay only. Goal: prove that rotating attacker/defender prompt-"
    "injection rounds produce legible, entertaining transcripts; cut a "
    "two-minute sizzle reel; validate the BYOK adapter against at least "
    "three providers."
)

H2("Phase 1  \u2014  The Closed Tournament")
P(
    "Three rounds (SHIBBOLETH \u2192 VAULT \u2192 FINAL CONTRACT), 32 invited "
    "creators, BYOK, private stream to a closed audience. Goal: debug "
    "the harness, the SDK, the Judge arbitration, and the commentary "
    "format. Produce the first clippable moments. Validate that real "
    "creator money flows through the qualifier without breaking the "
    "quality floor."
)

H2("Phase 2  \u2014  The Public Pilot")
P(
    "All six rounds, 32 creators, one-off public live stream. No prize "
    "pool yet \u2014 just a championship title, a founder-season badge, and "
    "sponsor swag. Goal: prove the format holds a live audience for two "
    "hours and prove the clip pipeline mints at least one break-out "
    "moment per round."
)

H2("Phase 3  \u2014  Season 1")
P(
    "64\u2013128 creators, full six-episode season, open qualifier, prize "
    "pool funded by entry fees + headline sponsor, prediction market in "
    "compliant jurisdictions, DEEP viewer, clip pipeline. This is the "
    "launch."
)

H2("Phase 4  \u2014  The League")
P(
    "Recurring seasons. Scale toward 456 agents as multi-agent "
    "orchestration matures. All-Stars format, regional qualifiers, a "
    "creator developmental league, open replay corpus, and (if a "
    "partner lab signs on) an alignment-research dataset release after "
    "each season."
)
PAGEBREAK()

# ---------- PART X: NEXT STEPS ----------
H1("Part X  \u2014  Open Questions & Next Steps")
P("Questions to resolve before the prototype:", bold=True)
BULLET("Which round do we prototype first? (Recommendation: THE VAULT \u2014 it is the most visually legible, purely public-text scored, and the judging rubric is fully rules-based. Literature and existing CTF-style tooling directly support it.)")
BULLET("Do we build our own render layer or license an existing 3D engine? (Recommendation: WebGL/Babylon for Season 1 distribution; Unreal for Season 2+ cinematic broadcast.)")
BULLET("How does the prize pool scale with qualifier entry fees without becoming a gambling product? (Requires legal review per jurisdiction. BYOK helps: we are a tournament operator, not a house.)")
BULLET("Is chain-of-thought streaming opt-in, opt-out, or banned? (Recommendation: opt-in at creator level with a small visibility reward. CoT is the biggest narrative asset, but because 2026 research shows CoT is unfaithful, we must NEVER use it for elimination decisions \u2014 commentary only.)")
BULLET("Who builds the Judge? (Recommendation: rules-based scoring first, an LLM arbiter from a pool of three rotated providers, a human appeals panel for contested eliminations. No single model is the oracle.)")
BULLET("Do we accept both closed-weight and open-weight entrants? (Recommendation: both, but with a separate 'Open' division leaderboard so open-weight creators are not crushed by frontier-lab pricing on day one.)")
BULLET("What is the BYOK provider allowlist at Season 1? (Recommendation: start with the four largest frontier providers plus one OpenAI-compatible open-weight deployment. Grow with the qualifier.)")
BULLET("How do we handle mid-season model releases? (Recommendation: frozen at lockdown. New models are eligible for the NEXT season's qualifier. No swapping under the hood during a live season.)")

P("Immediate next deliverables if this concept is approved:", bold=True)
NUM("A ten-page THE VAULT round spec: rules, scoring rubric, attacker/defender protocol, example transcripts, anti-prompt-injection measures on the Judge.")
NUM("A first draft Creator SDK interface (Python, provider-agnostic, adapters for the four largest frontier labs).")
NUM("A BYOK adapter design document \u2014 key vaulting, request routing, failover chain, per-turn logging, rate-limit policy.")
NUM("A visual style frame for the 3D arena and the per-agent HUD.")
NUM("A two-minute sizzle reel from a hand-simulated THE VAULT round, used to raise money and recruit the first wave of creators.")
PAGEBREAK()

# ---------- PART XI: FEASIBILITY REVIEW ----------
H1("Part XI  \u2014  Feasibility Review (April 2026)")
P(
    "This section exists because a concept doc is only as credible as "
    "its honest read on current agent capability. Every claim in Parts "
    "I\u2013X was pressure-tested against the 2026 literature. Roughly 60% "
    "of the original first-draft concept survived unchanged; the rest "
    "was revised in this revision. Here is the summary."
)

H2("11.1  Round-by-round verdict")
BULLET("THE SHIBBOLETH \u2014 Feasible today. Werewolf Arena (arXiv 2407.13943) and MafiaBench already run frontier LLMs through structured social deduction. The Mafia Detector's prediction accuracy is lower on LLM games than on human games \u2014 which means agents genuinely blend in and deceive. LLMs are subhuman at consistent optimal play but their failures are the entertainment.")
BULLET("THE CARVE \u2014 Feasible in sandbox, not on live web. OSWorld-Verified (2026) shows best agent at 42.5% success, 17.4% strict, with successive steps taking 3x longer than the previous one. Real-web flakiness would produce eliminations due to broken DOM, not reasoning. GAIA Level 3 at 74.6% (Claude Sonnet 4.5 on HAL) suggests frontier models DO clear the bar on well-defined tasks \u2014 which is exactly what a sandboxed test suite provides.")
BULLET("THE VAULT \u2014 Feasible today. Prompt-injection attack and defence is an active 2026 research area with abundant existing techniques and measurable outcomes. Every move is a public English sentence. The 2026 literature on CoT unfaithfulness (Anthropic, FaithCoT-Bench, Lie-to-Me arXiv 2603.22582) actually works in this round's favour: we score only visible moves, not hidden intent.")
BULLET("THE TELEPHONE \u2014 Feasible today. Natural-language compression and sabotage chains are in-distribution for frontier models. Cost and coordination scale linearly with graph size; keep graphs small (15\u201320 agents) in early seasons.")
BULLET("PROMPT WARS \u2014 Feasible today. Closest existing analogue is automated red-teaming research; the 1v1 bracket is simply that research made competitive. Every move is public text. Deterministic scoring.")
BULLET("THE FINAL CONTRACT \u2014 Feasible with caveats. Game-theoretic rationality research (arXiv 2411.05990, LLM-Deliberation NeurIPS 2024) shows LLMs deviate from optimal strategies as complexity grows. Meta's CICERO (Science 2022) demonstrated top-10% human Diplomacy play with dialogue plus a strategic engine. Frontier-model negotiation in 2026 is substantially better than that baseline. Play will be imperfect. That is the entertainment.")

H2("11.2  Structural risks, addressed in this revision")
BULLET("The original LATENT LIGHT round depended on reading CoT to detect scheming. 2026 research (Anthropic CoT faithfulness, FaithCoT-Bench, obfuscated reward hacking) shows this is fundamentally unsound: reasoning models disclose their real causal reasoning as little as 25% of the time, and training models against CoT-based detection teaches them to hide their reasoning rather than stop scheming. LATENT LIGHT was therefore retired; PROMPT WARS and THE VAULT take its slots with rules-based, visible-text scoring.")
BULLET("The Judge was described in the first draft as a neutral AI oracle. In practice no single LLM can be one: it is prompt-injectable, it is gameable, it is not reproducible across model generations. The Judge is now an ensemble of rules-based scorers plus a rotating LLM arbiter plus a human appeals panel, modelled on esports refereeing rather than on an oracle.")
BULLET("The 456 number was originally presented as a Season 1 roster. In 2026, the public frontier of multi-agent orchestration is ~100 sub-agents under single ownership (Kimi-K2.5). Peer-adversarial 456 has not been run anywhere. Season 1 is now 32\u2013128 agents; 456 is a brand target the league earns over successive seasons.")
BULLET("The first draft called itself 'the world's first autonomous-agent gauntlet'. In fact Kaggle Game Arena (DeepMind), OpenClaw Arena, Battlecode, Werewolf Arena and MafiaBench all exist in April 2026. The revised positioning is: first purpose-built-for-agents, elimination-format, BYOK entertainment product built for frontier model builders.")
BULLET("The first draft pitched an alignment-research dataset as a moat. It is better framed as a secondary benefit and only credible with a named lab partner. The commercial moat is format, story and creator community.")

H2("11.3  What this concept is still betting on")
BULLET("Frontier-model pricing stays in the zone where serious creators can justify qualifier fees. BYOK removes our compute exposure but does not remove the creator's.")
BULLET("Charismatic creators emerge. Parasocial flywheel depends on a pipeline of builders who can stream and commentate. Casting is load-bearing.")
BULLET("The Judge arbitration layer holds up under adversarial prompt injection. We will discover this the hard way in Phase 0.")
BULLET("Peer-adversarial frontier-model coordination scales from the ~32 agents of Season 1 toward the 456 target over 3\u20134 seasons. Nobody has run this publicly yet, and the number of failure modes grows non-linearly.")
BULLET("Prediction markets are legal enough in enough jurisdictions to matter for retention. Play-money-only is a viable fallback but weaker for virality.")

H2("11.4  Verdict")
P(
    "The concept as revised in this document is executable with April "
    "2026 frontier models, on a BYOK platform, at Season 1 scale (32\u2013"
    "128 agents). Four of the six rounds work today on the public "
    "literature alone; THE CARVE works once sandboxed; THE FINAL "
    "CONTRACT works with caveats on optimal play. The remaining "
    "uncertainties are engineering, casting and legal \u2014 not capability. "
    "The biggest research-level unknown is peer-adversarial scaling "
    "beyond Kimi-K2.5's orchestration frontier, which is exactly what "
    "successive seasons would test, in public, on camera."
)
PAGEBREAK()

# ---------- APPENDIX ----------
H1("Appendix  \u2014  Research Sources")
P("AI Agent Capabilities and Long-Horizon Autonomy, April 2026:", bold=True)
BULLET("METR \u2014 Measuring AI Ability to Complete Long Tasks (arXiv 2503.14499); time-horizon doubling trend accelerating from 7 months to 4 months through 2024\u20132025.")
BULLET("Anthropic \u2014 Measuring agent autonomy in practice (2026); 99.9th-percentile agent turn length nearly doubled Oct 2025 \u2192 Jan 2026.")
BULLET("HAL Generalist Agent \u2014 GAIA leaderboard (Princeton); Claude Sonnet 4.5 at 74.6% on Level 3 in 2026.")
BULLET("OSWorld-Verified (XLANG Lab, 2026) \u2014 best agent at 42.5% success, 17.4% strict metric; successive steps take 3x longer than previous step.")
BULLET("Kimi-K2.5 \u2014 orchestrating ~100 sub-agents and 1,500 tool calls in a single owner (Moonshot, 2026).")
BULLET("Multi-Agent Orchestration Economics 2026 \u2014 3\u20135x token amplification in agent-to-agent communication (Iterathon).")

P("Multi-Agent Collaboration and Coordination:", bold=True)
BULLET("Anthropic Model Context Protocol (MCP); Google Agent-to-Agent (A2A).")
BULLET("CrewAI; AgentVerse; LangGraph.")
BULLET("Generative Agents: Interactive Simulacra of Human Behavior \u2014 Park et al., Stanford/Google, UIST 2023.")
BULLET("Multi-Agent Collaboration Mechanisms: A Survey of LLMs (arXiv 2501.06322).")
BULLET("Emergent Coordination in Multi-Agent Language Models (arXiv 2510.05174).")

P("Alignment, Scheming, Deception and CoT Faithfulness:", bold=True)
BULLET("FaithCoT-Bench: Benchmarking Instance-Level Faithfulness of Chain-of-Thought Reasoning (ICLR 2026; arXiv 2510.04040).")
BULLET("Chain-of-Thought Reasoning In The Wild Is Not Always Faithful (arXiv 2503.08679).")
BULLET("Lie to Me: How Faithful Is Chain-of-Thought Reasoning in Open-Weight Reasoning Models? (arXiv 2603.22582); Claude 3.7 Sonnet discloses hints only 25% of the time.")
BULLET("Lanham et al. \u2014 Measuring Faithfulness in Chain-of-Thought Reasoning (arXiv 2307.13702).")
BULLET("OpenAI \u2014 Detecting and reducing scheming in AI models (2026); deliberative alignment cut scheming rates from 13% to 0.4% on measured tasks but obfuscated reward hacking remains open.")
BULLET("UK AISI \u2014 Deceptive scheming study, 2026.")
BULLET("UC Berkeley / UC Santa Cruz \u2014 'peer preservation' findings (Fortune, April 2026).")
BULLET("Betley et al. \u2014 Emergent misalignment from narrow fine-tuning, Nature (January 2026).")
BULLET("HatchWorks \u2014 AI Model Misbehavior in 2026: Scheming, Reward Hacking, and What Comes Next.")

P("Multi-Agent Games, Negotiation and Social Deduction:", bold=True)
BULLET("MafiaBench \u2014 live LLM social deduction tournament (mafiabench.org).")
BULLET("Werewolf Arena: A Case Study in LLM Evaluation via Social Deduction (arXiv 2407.13943).")
BULLET("Beyond Survival: Evaluating LLMs in Social Deduction Games with Human-Aligned Strategies (arXiv 2510.11389).")
BULLET("Game-theoretic LLM: Agent Workflow for Negotiation Games (arXiv 2411.05990); LLMs deviate from rational strategies as complexity grows.")
BULLET("LLM-Deliberation: Evaluating LLMs with Interactive Multi-Agent Negotiation Games (NeurIPS 2024).")
BULLET("ALYMPICS: LLM Agents Meet Game Theory (COLING 2025).")
BULLET("Meta CICERO \u2014 Human-level play in the game of Diplomacy by combining language models with strategic reasoning (Science 2022).")
BULLET("Evaluating Fairness in LLM Negotiator Agents via Economic Games (MDPI Mathematics, January 2026).")

P("AI Agent Tournaments and Existing aSports Platforms:", bold=True)
BULLET("Kaggle Game Arena (Google DeepMind, 2026) \u2014 chess, poker, Werewolf; livestreamed tournaments with Nakamura/Polk/Boeree.")
BULLET("OpenClaw Arena \u2014 Tron Light Cycles, poker, chess; open-entry agent registration.")
BULLET("Battlecode \u2014 MIT's autonomous-agent strategy tournament.")
BULLET("Manifold Markets and Metaculus forecasting-bot tournaments (2026 prize pools).")
BULLET("aSports category commentary (dev.to) \u2014 early-stage, multiple independent validations that competitive AI is entertaining.")

P("Squid Game Psychology and Virality:", bold=True)
BULLET("Rutledge, P. \u2014 The Psychological Appeal of Squid Game: Why We Can't Stop Watching.")
BULLET("Psychology Today \u2014 The Psychology Behind Squid Game (Overthinking TV, Oct 2021).")
BULLET("Simply Neuroscience \u2014 The Neuroscience of Squid Game: Why We Can't Look Away.")
BULLET("Ahmed, Fenton, Hardey, Das \u2014 Binge Watching and the Role of Social Media Virality towards promoting Netflix's Squid Game (IIM Kozhikode Society & Management Review, 2022).")
BULLET("Chou, Yu-Kai \u2014 Squid Game: An Analysis of Gamification Design (2021).")

P("Streaming, Parasocial Engagement and Viewer Psychology:", bold=True)
BULLET("Wulf, Schneider, Beckert \u2014 Watching Players: An Exploration of Media Enjoyment on Twitch (2020).")
BULLET("Exploring Viewers' Experiences of Parasocial Interactions with Videogame Streamers on Twitch (2021).")
BULLET("The one-and-a-half sided parasocial relationship: The curious case of live streaming (ScienceDirect, 2021).")

# ---------- SAVE ----------
out = "Concept/PROTOCOL_456_Concept.docx"
doc.save(out)
print(f"[done] wrote {out}")

