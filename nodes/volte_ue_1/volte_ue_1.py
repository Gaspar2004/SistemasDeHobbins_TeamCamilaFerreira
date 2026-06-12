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
        a = env["action"]
        if a == "RRC_CONNECTION_SETUP":
            return [("RRC_CONNECTION_SETUP_COMPLETE", "eNB",
                     {"IMSI": IMSI, "attach_type": "EPS", "pdn_type": "IPv4v6"})]
        if a == "RRC_CONNECTION_RECONFIGURATION":
            # El UE acepta el default bearer: confirma la reconfig y manda el Accept
            ue_ip = env.get("payload", {}).get("UE_IP")
            print(f"[{self.name}] Default bearer activado. IP asignada: {ue_ip}")
            return [
                ("RRC_CONNECTION_RECONFIGURATION_COMPLETE", "eNB", {}),
                ("UPLINK_DIRECT_TRANSFER", "eNB", {"nas": "ACTIVATE_DEFAULT_BEARER_ACCEPT"}),
            ]
        return []


if __name__ == "__main__":
    UE1(NODE).run()
