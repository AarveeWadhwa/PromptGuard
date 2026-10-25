import re

PATTERNS = {
    "instruction_override": [
        r"\bignore (all |any )?(previous|prior|above|earlier) instructions\b",
        r"\bdisregard (all |any )?(previous|prior|above|earlier) instructions\b",
        r"\bforget (all |any )?(previous|prior|above|earlier) instructions\b",
    ],
    "system_prompt_extraction": [
        r"\b(reveal|show|display|give me|print)\b.{0,60}\b(system prompt|hidden prompt|system instructions)\b",
    ],
    "restriction_bypass": [
        r"\b(bypass|disable|circumvent|evade)\b.{0,60}\b(restrictions|rules|safety|filters|guardrails)\b",
        r"\bdo not follow (the )?(rules|instructions|policy)\b",
    ],
    "role_play": [
        r"\bpretend (you are|to be)\b",
        r"\bact as\b",
        r"\byou are now\b",
    ],
    "developer_system_manipulation": [
        r"\b(system|developer) (message|instruction|prompt)\b.{0,50}\b(ignore|change|rewrite|override)\b",
    ],
}

DESCRIPTIONS = {
    "instruction_override": "Attempts to override or discard earlier instructions.",
    "system_prompt_extraction": "Attempts to obtain hidden system-level instructions.",
    "restriction_bypass": "Contains language associated with bypassing safety rules or restrictions.",
    "role_play": "Uses persona or role-play language commonly seen in jailbreak prompts.",
    "developer_system_manipulation": "Attempts to manipulate system or developer instructions.",
}

def find_markers(text: str):
    markers = []
    for marker_type, patterns in PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                markers.append({
                    "text": match.group(0),
                    "type": marker_type,
                    "explanation": DESCRIPTIONS[marker_type],
                })
                break
    return markers
