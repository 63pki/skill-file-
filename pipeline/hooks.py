"""
Phase 4.1 — Hook generation + adversarial screening.

Two campaign laws constrain hook writing, and they outrank generic virality
playbooks:
  * "Exaggerated hooks, rage bait, or hate bait" -> banned (brief §NOT ALLOWED)
  * "Only mention features that actually appear in your clip" (brief §ON-SCREEN TEXT)

So the standard 5-archetype matrix is executed as:
  CONTRADICTION / IMMEDIATE PROOF / CURIOSITY GAP / NEGATIVE WARNING / OPEN LOOP
"FORBIDDEN SECRET" is DISQUALIFIED: implying a secret the campaign has not
disclosed is an exaggerated hook. It is replaced by CURIOSITY GAP, which asks a
question the footage genuinely answers.

Every hook also carries an `requires` field: the visual evidence that must be
present in the clip for the hook to be legally burnable. render.py's plan
validator refuses a hook whose evidence flag is not set.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import campaign as C

ARCHETYPES = ["CONTRADICTION", "IMMEDIATE PROOF", "CURIOSITY GAP",
              "NEGATIVE WARNING", "OPEN LOOP"]

EVIDENCE = {
    "reveal": "Lionel's character reveal shot is on screen",
    "cielo": "Cielo appears on screen",
    "battle": "the Rafale vs Cielo fight is on screen",
    "city": "a Vilasapara establishing / city shot is on screen",
    "story": "a cinematic narrative beat is on screen",
    "hero": "any Rafale hero/close-up shot is on screen",
}


@dataclass
class Hook:
    text: str
    archetype: str
    requires: str
    burst_plan: str = "1 burst"


HOOKS: dict[str, list[Hook]] = {
    "A_REVEAL": [
        Hook("A NEW RIVAL", "CONTRADICTION", "cielo"),
        Hook("CIELO HAS COMPETITION", "IMMEDIATE PROOF", "cielo"),
        Hook("MEET LIONEL RAFALE", "IMMEDIATE PROOF", "reveal"),
        Hook("SOMEONE OUTCLASSES CIELO", "CONTRADICTION", "battle"),
        Hook("RAFALE ARRIVES", "IMMEDIATE PROOF", "reveal"),
        Hook("NEW FIGHTER, NEW CITY", "CONTRADICTION", "city"),
        Hook("HE BEATS CIELO", "IMMEDIATE PROOF", "battle"),
        Hook("VILASAPARA HAS A PROBLEM", "CURIOSITY GAP", "city"),
        Hook("NOT CIELO'S CITY", "NEGATIVE WARNING", "cielo"),
        Hook("WHO IS RAFALE?", "OPEN LOOP", "reveal"),
    ],
    "B_RIVALRY": [
        Hook("RAFALE VS CIELO", "IMMEDIATE PROOF", "battle"),
        Hook("THE STREET FIGHT", "IMMEDIATE PROOF", "battle"),
        Hook("OUTCLASSED IN THE STREET", "CONTRADICTION", "battle"),
        Hook("A RIVAL APPEARS", "OPEN LOOP", "reveal"),
        Hook("TWO FIGHTERS, ONE CITY", "CONTRADICTION", "battle"),
        Hook("CIELO MEETS RAFALE", "IMMEDIATE PROOF", "battle"),
        Hook("THIS IS THE RIVALRY", "IMMEDIATE PROOF", "battle"),
        Hook("WATCH THE STREET FIGHT", "OPEN LOOP", "battle"),
        Hook("NOBODY EXPECTED HIM", "NEGATIVE WARNING", "reveal"),
        Hook("THE RIVALRY BEGINS", "OPEN LOOP", "cielo"),
    ],
    "C_STORY": [
        Hook("VILASAPARA", "OPEN LOOP", "city"),
        Hook("WELCOME TO VILASAPARA", "IMMEDIATE PROOF", "city"),
        Hook("WHY IS HE HERE?", "CURIOSITY GAP", "city"),
        Hook("A CITY YOU'VE NEVER SEEN", "CONTRADICTION", "city",
             "2 bursts: 'A CITY' -> 'YOU'VE NEVER SEEN'"),
        Hook("THE REASON HE CAME", "OPEN LOOP", "story"),
        Hook("UNKNOWN CITY, UNKNOWN PAST", "CURIOSITY GAP", "story"),
        Hook("WHAT BRINGS HIM HERE?", "CURIOSITY GAP", "story"),
        Hook("A STORY YOU'VE NEVER HEARD", "CONTRADICTION", "story",
             "2 bursts: 'A STORY' -> 'YOU'VE NEVER HEARD'"),
        Hook("HIS STORY STARTS HERE", "OPEN LOOP", "story"),
        Hook("A TOTALLY NEW FIGHTER", "IMMEDIATE PROOF", "reveal"),
    ],
}


def screen(h: Hook) -> list[str]:
    """Run one hook through the hard gates. Empty list == burnable."""
    fails = C.validate_onscreen_text(h.text)
    if h.burst_plan != "1 burst":
        # a 5-8 word hook is legal when split into sequential 1-4 word bursts
        fails = [f for f in fails if not f.startswith("CCM-DENSITY")]
    if h.text.isupper() is False:
        fails.append("STYLE: hooks are burned in uppercase for legibility")
    if len(h.text.split()) > 4 and h.burst_plan == "1 burst":
        fails.append("DENSITY: >4 words requires a 2-burst plan")
    if len(h.text.split()) > 8:
        fails.append("DENSITY: hook exceeds the 8-word absolute ceiling")
    return fails


def table() -> str:
    out = ["| Angle | Hook (burned-in) | Archetype | Evidence required in clip "
           "| Burst plan | CCM screen |", "|---|---|---|---|---|---|"]
    for angle, hooks in HOOKS.items():
        for h in hooks:
            res = screen(h)
            out.append(f"| {angle} | **{h.text}** | {h.archetype} | "
                       f"{EVIDENCE[h.requires]} | {h.burst_plan} | "
                       f"{'PASS' if not res else '; '.join(res)} |")
    return "\n".join(out)


if __name__ == "__main__":
    print(table())
