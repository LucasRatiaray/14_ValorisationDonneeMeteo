"""Configuration gunicorn.

Reprend les options qui etaient passees en arguments dans le Dockerfile, et ajoute
le support du mode multiprocess de prometheus_client.

Pourquoi : chaque worker gunicorn est un processus separe avec ses propres compteurs
en memoire. Un scrape de /metrics tombe sur un seul worker au hasard et ne voit donc
qu'une fraction du trafic, avec des valeurs qui montent et descendent d'un scrape a
l'autre. Prometheus interprete une baisse de compteur comme un redemarrage et fausse
tous ses calculs.

En mode multiprocess, les workers ecrivent dans un repertoire partage
(PROMETHEUS_MULTIPROC_DIR) et la vue /metrics additionne ces fichiers.
"""

import os

bind = "0.0.0.0:8000"
workers = 3
timeout = 120
worker_tmp_dir = "/dev/shm"
accesslog = "-"
errorlog = "-"
loglevel = "info"


def child_exit(server, worker):
    """Marque un worker mort pour que ses compteurs cessent d'etre agreges."""
    if os.environ.get("PROMETHEUS_MULTIPROC_DIR"):
        from prometheus_client import multiprocess

        multiprocess.mark_process_dead(worker.pid)
