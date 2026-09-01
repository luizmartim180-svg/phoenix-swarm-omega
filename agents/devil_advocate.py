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
        # Defer BedrockClient creation until needed and allow offline mode
        self.bedrock = None
        try:
            from core.bedrock_client import BedrockClient
            self.bedrock = BedrockClient()
        except Exception:
            logging.warning('BedrockClient not available; DevilAdvocate will run in offline fallback mode')

    def challenge_pitch(self, objections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        challenges = []
        for obj in objections[:6]:
            prompt = f"Objection from research:\n{json.dumps(obj)}\n\nGenerate ONE challenge in the defined JSON format."
            if not self.bedrock:
                # Offline fallback: produce a simple heuristic challenge
                challenges.append({"id": f"ch-{obj.get('id','na')}", "challenge": f"(offline) Question the assumption: {obj.get('summary', obj.get('text',''))}"})
                continue
            try:
                challenges.append(json.loads(self.bedrock.chat(prompt=prompt, system=SYSTEM, max_tokens=300)))
            except Exception as e:
                logging.error(f"Advocate falhou: {e}")
                # On failure, fall back to a simple challenge
                challenges.append({"id": f"ch-{obj.get('id','na')}", "challenge": "(fallback) Unable to reach Bedrock; question the evidence strength."})
        return challenges
