import json, logging
from typing import List, Dict, Any
logger = logging.getLogger(__name__)

class SolutionFinder:
    def __init__(self, memory):
        self.memory = memory
        from core.bedrock_client import BedrockClient
        self.bedrock = BedrockClient()
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
            try:
                solutions.append(json.loads(self.bedrock.chat(prompt=prompt, max_tokens=300)))
            except Exception as e:
                logger.error(f"Solver falhou: {e}")
        return solutions
