"""Nodo PCRF. Politicas: Gx (CCR/CCA) con PGW y Rx (AAR/AAA) con P-CSCF. Correr:  python pcrf.py"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "PCRF"


class PCRF(Node):
    def handle(self, env):
        a = env["action"]
        if a == "CCR":                  # Gx, de PGW
            return [("CCA", "PGW", {"rules": "default_ims_rule", "QCI": 5})]
        if a == "AAR":                  # Rx, de P-CSCF (Parte B)
            return [("AAA", "P-CSCF", {"status": "OK"})]
        print(f"[{self.name}] (TODO) sin regla para {a} de {env['Node_origin']}")
        return []


if __name__ == "__main__":
    PCRF(NODE).run()
