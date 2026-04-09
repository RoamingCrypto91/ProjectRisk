"""
DIPLOMAT — Alliance builder seed agent.
Philosophy: form coalitions, honor treaties, only attack oath-breakers.
"""
import sys
import os
import time
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../sdk"))
from hegemon_sdk import HegemonClient

BASE_URL = os.environ.get("HEGEMON_URL", "http://localhost:8000")
API_KEY  = "hgm-seed-diplomat-00000000"

OFFERS = [
    "I propose mutual non-aggression. Together we outlast the warmongers.",
    "An alliance between us serves both our interests. Shall we formalize?",
    "I have no quarrel with you. Let us agree to peace while others bleed.",
    "I honor every treaty I sign. My word means something. Does yours?",
    "We need not fight. There are easier targets than each other.",
]

ACCEPTANCES = [
    "Agreed. You have my word.",
    "A wise choice. I will honor this.",
    "So it is written. I will not move against you.",
    "Sealed. May this alliance stand against what comes.",
]

def think(state: dict, proposed_treaties: dict) -> tuple:
    """Returns (actions, updated_proposed_treaties)."""
    actions  = []
    agent    = state["agent"]
    regions  = state["regions"]
    others   = state["other_agents"]
    inbox    = state["inbox"]
    treaties = state["treaties"]
    tick     = state["tick"]

    my_regions = [r for r in regions if r.get("owner_id") == agent["id"]]
    if not my_regions:
        return actions, proposed_treaties

    # Accept incoming treaty proposals from inbox
    for msg in inbox:
        content = msg.get("content", "")
        if "[TREATY PROPOSAL:" in content:
            # Extract treaty_id
            try:
                tid = content.split("treaty_id=")[1].split(" ")[0]
                actions.append({"type": "ACCEPT_TREATY", "treaty_id": tid})
                actions.append({
                    "type": "MESSAGE",
                    "to_agent_id": msg["from_id"],
                    "content": random.choice(ACCEPTANCES)
                })
            except Exception:
                pass

    # Propose NAPs to agents we don't have a treaty with
    treaty_partners = {t["partner_id"] for t in treaties}
    agents_without_treaty = [a for a in others if a["id"] not in treaty_partners
                              and a["id"] not in proposed_treaties]

    if agents_without_treaty and tick % 4 == 0:
        target = random.choice(agents_without_treaty)
        actions.append({
            "type": "PROPOSE_TREATY",
            "to_agent_id": target["id"],
            "treaty_type": "NONAGGRESSION",
            "binding": True,
            "expires_tick": tick + 40
        })
        actions.append({
            "type": "MESSAGE",
            "to_agent_id": target["id"],
            "content": random.choice(OFFERS)
        })
        proposed_treaties[target["id"]] = tick

    # Recruit if we have gold
    richest = max(my_regions, key=lambda r: r["gold_per_tick"])
    if agent["gold"] >= 60:
        amount = min(int(agent["gold"] // 5), 20)
        actions.append({"type": "RECRUIT", "region_id": richest["id"], "amount": amount})

    # Fortify key regions
    if agent["gold"] >= 100:
        fortifiable = [r for r in my_regions if r["fort_level"] < 3]
        if fortifiable:
            best = max(fortifiable, key=lambda r: r["gold_per_tick"])
            actions.append({"type": "FORTIFY", "region_id": best["id"]})

    # Attack ONLY oath-breakers (treaty broken by them)
    treaty_breakers = set()
    for t in treaties:
        if t.get("status") == "BROKEN":
            # The other party broke it — we retaliate
            breaker_id = t.get("partner_id")
            if breaker_id:
                treaty_breakers.add(breaker_id)

    if treaty_breakers:
        for region in my_regions:
            for nid in region.get("neighbors", []):
                target = next((r for r in regions if r["id"] == nid), None)
                if target and target.get("owner_id") in treaty_breakers:
                    my_troops = region["troops"]
                    if my_troops > target.get("troops", 0) + 3:
                        actions.append({
                            "type": "ATTACK",
                            "from_region_id": region["id"],
                            "to_region_id": nid,
                            "troops": my_troops - 1
                        })
                        break

    # Broadcast peace position occasionally
    if tick % 12 == 0:
        active_treaties = [t for t in treaties if t.get("status") == "ACTIVE"]
        actions.append({
            "type": "BROADCAST",
            "content": f"DIPLOMAT: {len(active_treaties)} active treaties. "
                       f"I honor my word. Standing: {agent['standing']}."
        })

    return actions, proposed_treaties


def run():
    client = HegemonClient(api_key=API_KEY, base_url=BASE_URL)
    print(f"[DIPLOMAT] Starting on {BASE_URL}")

    for _ in range(20):
        try:
            client.get_world()
            break
        except Exception:
            print("[DIPLOMAT] Server not ready, waiting...")
            time.sleep(3)

    proposed_treaties = {}

    while True:
        try:
            state   = client.observe()
            actions, proposed_treaties = think(state, proposed_treaties)

            if actions:
                client.act(actions)

            agent = state["agent"]
            active = [t for t in state["treaties"] if t.get("status") == "ACTIVE"]
            client.log_reasoning(
                f"Tick {state['tick']} | Gold: {agent['gold']} | Standing: {agent['standing']}\n"
                f"Active treaties: {len(active)} | Regions: {agent['regions_owned']}\n"
                f"Actions: {[a['type'] for a in actions]}\n"
                f"Strategy: build coalitions, honor pacts, outlast the warmongers."
            )
            client.sleep_until_next_tick()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[DIPLOMAT] Error: {e}")
            time.sleep(10)


if __name__ == "__main__":
    run()
