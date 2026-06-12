"""Nodo VoLTE UE 1. Inicia el Attach. Correr:  python volte_ue_1.py [auto]"""
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "UE1"
SESSION = "ue1-attach"
IMSI = "748010000000001"


class UE1(Node):
    def on_start(self):
        if "auto" in sys.argv:
            print(f"[{self.name}] auto-start en 2s...")
            time.sleep(2)
        else:
            input(f"[{self.name}] Enter para iniciar el Attach...")
        self.originate("RRC_CONNECTION_REQUEST", "eNB", {"IMSI": IMSI}, session=SESSION)

    def handle(self, env):
        if env["action"] == "RRC_CONNECTION_SETUP":
            # Responde con el Setup Complete (que lleva el Attach Request / PDN Connectivity)
            return [("RRC_CONNECTION_SETUP_COMPLETE", "eNB",
                     {"IMSI": IMSI, "attach_type": "EPS", "pdn_type": "IPv4v6"})]
        return []


if __name__ == "__main__":
    UE1(NODE).run()
