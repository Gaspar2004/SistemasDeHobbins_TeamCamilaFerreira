"""Nodo MME. Por ahora termina la cadena al recibir el Attach. Correr:  python mme.py"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "MME"


class MME(Node):
    def handle(self, env):
        if env["action"] == "ATTACH_REQUEST":
            imsi = env.get("payload", {}).get("IMSI")
            print(f"[{self.name}] Attach recibido (IMSI={imsi}).")
            print(f"[{self.name}] Proximo paso real: Authentication con HSS + Update "
                  f"Location (pendiente; HSS todavia no esta levantado).")
            return []   # terminal en esta etapa de pruebas
        return []


if __name__ == "__main__":
    MME(NODE).run()
