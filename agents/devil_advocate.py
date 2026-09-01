import json, logging
from pathlib import Path
from typing import List, Dict, Any
logger = logging.getLogger(__name__)
SYSTEM = (Path(__file__).parent.parent / "prompts" / "devil_advocate_system.md")
if SYSTEM.exists():
    SYSTEM = SYSTEM.read_text(encoding="utf-8")
else:
    SYSTEM = "You are a devil's advocate. Challenge succinctly."

class DevilAdvocate:
    def __init__(self, memory):
        self.memory = memory
        from core.bedrock_client import BedrockClient
        self.bedrock = BedrockClient()
    def challenge_pitch(self, objections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        challenges = []
        for obj in objections[:6]:
            prompt = f"Objection from research:\n{json.dumps(obj)}\n\nGenerate ONE challenge in the defined JSON format."
            try:
                challenges.append(json.loads(self.bedrock.chat(prompt=prompt, system=SYSTEM, max_tokens=300)))
            except Exception as e:
                logging.error(f"Advocate falhou: {e}")
        return challenges
