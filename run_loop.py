#!/usr/bin/env python3
"""
Phoenix Swarm Omega - Loop Contínuo de Aprendizado
Pesquisa objeções, desafia premissas e encontra soluções em tempo real.
Compartilha memória com Swarm Alpha via TiDB.
"""
import time
import logging
import signal
import sys
from datetime import datetime
from agents.researcher import Researcher
from agents.devil_advocate import DevilAdvocate
from agents.solution_finder import SolutionFinder
from memory.omega_memory import OmegaMemory

logging.basicConfig(level=logging.INFO, format="%(asctime)s [OMEGA] %(message)s")
logger = logging.getLogger(__name__)

class OmegaLoop:
    def __init__(self):
        self.memory = OmegaMemory()
        self.researcher = Researcher(self.memory)
        self.advocate = DevilAdvocate(self.memory)
        self.solver = SolutionFinder(self.memory)
        self.running = True
        
        signal.signal(signal.SIGINT, self._stop)
        signal.signal(signal.SIGTERM, self._stop)
    
    def _stop(self, *args):
        logger.info('Shutting down Omega Loop')
        self.running = False
    
    def run(self, interval_sec=300, once=False):
        logger.info('Starting Omega continuous learning loop')
        while self.running:
            try:
                objections = self.researcher.search_latest_objections()
                challenges = self.advocate.challenge_pitch(objections)
                solutions = self.solver.find_solutions(challenges)
                self.memory.store_insight(objections, challenges, solutions)
                logger.info(f"Novo insight: {solutions[0]['summary'] if solutions else 'n/a'}")
            except Exception as e:
                logger.exception('Error in Omega loop: %s', e)
            if once:
                break
            time.sleep(interval_sec)

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--once', action='store_true')
    p.add_argument('--interval', type=int, default=300)
    args = p.parse_args()
    loop = OmegaLoop()
    if args.once:
        loop.running = True
    loop.run(interval_sec=args.interval, once=args.once)
