import json, logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
FALLBACK = Path(__file__).parent.parent / "data" / "known_objections.json"

class Researcher:
    def __init__(self, memory):
        self.memory = memory
    def search_latest_objections(self, queries=None) -> List[Dict[str, Any]]:
        queries = queries or [
            "TiDB vector search limitations",
            "serverless database cold start cost objections",
            "pinecone pgvector vs tidb why not"
        ]
        results = []
        for q in queries:
            try:
                from duckduckgo_search import DDGS
                with DDGS() as ddgs:
                    for h in list(ddgs.text(q, max_results=3)):
                        results.append({"source": "web", "query": q, "title": h.get("title"), "snippet": h.get("body")})
            except Exception as e:
                logger.warning(f"Web search falhou ({e}); usando fallback offline")
                if FALLBACK.exists():
                    for o in json.loads(FALLBACK.read_text(encoding="utf-8")):
                        results.append({"source": "offline", "query": q, **o})
        return results[:12]
