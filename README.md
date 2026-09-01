# Phoenix Swarm Omega

Meta-swarm para pesquisa de objeções, validação de pitch e geração de contra-argumentos.

Este repositório roda um ciclo Researcher -> DevilAdvocate -> SolutionFinder que busca objeções, gera desafios ao pitch e encontra respostas suportadas por evidência.

Quick start (local):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_loop.py --once
```

Arquitetura:
- agents/researcher.py: pesquisa na web (ou usa fallback offline)
- agents/devil_advocate.py: gera desafios via Bedrock
- agents/solution_finder.py: produz soluções e evidências
- memory/omega_memory.py: armazena e recupera soluções relevantes (TiDB)

Veja .env.example para variáveis necessárias. Para testes rápidos use `--once`.
