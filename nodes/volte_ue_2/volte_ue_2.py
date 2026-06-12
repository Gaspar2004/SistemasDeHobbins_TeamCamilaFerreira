"""Nodo UE2. Inicia el Attach (mirror de UE1). Correr:  python volte_ue_2.py [auto]"""
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "UE2"
SESSION = "ue2-attach"
IMSI = "748010000000002"


class UE2(Node):
    def on_start(self):
        if "auto" in sys.argv:
            time.sleep(2)
        else:
            input(f"[{self.name}] Enter para iniciar el Attach...")
        self.originate("RRC_CONNECTION_REQUEST", "eNB", {"IMSI": IMSI}, session=SESSION)

    def handle(self, env):
        if env["action"] == "RRC_CONNECTION_SETUP":
            return [("RRC_CONNECTION_SETUP_COMPLETE", "eNB",
                     {"IMSI": IMSI, "attach_type": "EPS", "pdn_type": "IPv4v6"})]
        return []


if __name__ == "__main__":
    UE2(NODE).run()
