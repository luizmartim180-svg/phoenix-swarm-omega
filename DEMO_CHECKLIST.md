Demo checklist — Phoenix Swarm Omega (final prep)

(See alpha checklist for shared steps; these are Omega-specific items)

1) Local runs & insights
- Run python -m pip install -e .[dev] in Omega virtualenv if not installed.
- Run run_loop.py --once two additional cycles and commit outputs/insights_offline.md with [OFFLINE] timestamps.

2) TiDB & env
- Ensure TIDB_SSL_CA points to the CA in alpha path or local path.
- Verify Omega memory lazy-init works when TiDB is present.

3) Git & publish
- Commit outputs and push origin main. Use --force-with-lease if needed (force push authorized previously).

4) Demo
- Show agent cycle outputs and explain fallback logic when external embeddings are unavailable.

Timestamp: 2026-09-02T11:47:36-03:00
