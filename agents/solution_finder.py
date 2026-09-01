import json, logging
from typing import List, Dict, Any
logger = logging.getLogger(__name__)

class SolutionFinder:
    def __init__(self, memory):
        self.memory = memory
        # Defer BedrockClient creation to allow offline mode
        self.bedrock = None
        try:
            from core.bedrock_client import BedrockClient
            self.bedrock = BedrockClient()
        except Exception:
            logging.warning('BedrockClient not available; SolutionFinder will run in offline fallback mode')

    def find_solutions(self, challenges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        solutions = []
        for ch in challenges:
            past = []
            try:
                past = self.memory.get_relevant_solutions(ch.get("weakness", ""))
            except Exception:
                past = []
            prompt = (f"Challenge: {json.dumps(ch)}\nPast solutions from vector memory: {json.dumps(past)}\n"
                      "Produce evidence-backed mitigation. JSON: {\"summary\": str, \"evidence\": str, \"action_for_pitch\": str}")
            if not self.bedrock:
                # Offline fallback: produce a templated solution using past context
                solutions.append({"id": f"sol-{ch.get('id','na')}", "summary": "(offline) Suggested mitigation based on past solutions", "evidence": "n/a", "action_for_pitch": "Present mitigation plan and highlight need to validate with live infra"})
                continue
            try:
                solutions.append(json.loads(self.bedrock.chat(prompt=prompt, max_tokens=300)))
            except Exception as e:
                logger.error(f"Solver falhou: {e}")
                solutions.append({"id": f"sol-{ch.get('id','na')}", "summary": "(fallback) Bedrock unavailable", "evidence": "n/a", "action_for_pitch": "Fallback: document limitation and propose manual review"})
        return solutions
