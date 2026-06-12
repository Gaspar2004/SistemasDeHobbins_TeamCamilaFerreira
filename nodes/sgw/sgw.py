"""Nodo SGW. Relay de Create Session y Modify Bearer entre MME y PGW. Correr:  python sgw.py"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "SGW"


class SGW(Node):
    def handle(self, env):
        a = env["action"]
        p = env.get("payload", {})
        if a == "CREATE_SESSION_REQUEST":      # de MME -> PGW
            return [("CREATE_SESSION_REQUEST", "PGW", p)]
        if a == "CREATE_SESSION_RESPONSE":     # de PGW -> MME
            return [("CREATE_SESSION_RESPONSE", "MME", p)]
        if a == "MODIFY_BEARER_REQUEST":       # de MME -> responde a MME
            return [("MODIFY_BEARER_RESPONSE", "MME", {})]
        print(f"[{self.name}] (TODO) sin regla para {a} de {env['Node_origin']}")
        return []


if __name__ == "__main__":
    SGW(NODE).run()
