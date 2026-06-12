"""Nodo eNB. Relay radio (RRC) <-> NAS/S1 (MME). Correr:  python enb.py"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "eNB"


class ENB(Node):
    def handle(self, env):
        action = env["action"]
        ue = env["Node_origin"]   # responde al UE que lo contacto (UE1 o UE2)
        if action == "RRC_CONNECTION_REQUEST":
            return [("RRC_CONNECTION_SETUP", ue, {})]
        if action == "RRC_CONNECTION_SETUP_COMPLETE":
            # Reenvia el Attach hacia el MME por S1-MME
            return [("ATTACH_REQUEST", "MME", env.get("payload", {}))]
        return []


if __name__ == "__main__":
    ENB(NODE).run()
