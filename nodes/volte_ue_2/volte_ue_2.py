"""Nodo VoLTE UE 2. Inicia el Attach (mirror de UE1). Correr:  python volte_ue_2.py [auto]"""
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
            print(f"[{self.name}] auto-start en 2s...")
            time.sleep(2)
        else:
            input(f"[{self.name}] Enter para iniciar el Attach...")
        self.originate("RRC_CONNECTION_REQUEST", "eNB", {"IMSI": IMSI}, session=SESSION)

    def handle(self, env):
        a = env["action"]
        if a == "RRC_CONNECTION_SETUP":
            return [("RRC_CONNECTION_SETUP_COMPLETE", "eNB",
                     {"IMSI": IMSI, "attach_type": "EPS", "pdn_type": "IPv4v6"})]
        if a == "RRC_CONNECTION_RECONFIGURATION":
            ue_ip = env.get("payload", {}).get("UE_IP")
            print(f"[{self.name}] Default bearer activado. IP asignada: {ue_ip}")
            return [
                ("RRC_CONNECTION_RECONFIGURATION_COMPLETE", "eNB", {}),
                ("UPLINK_DIRECT_TRANSFER", "eNB", {"nas": "ACTIVATE_DEFAULT_BEARER_ACCEPT"}),
            ]
        return []


if __name__ == "__main__":
    UE2(NODE).run()
