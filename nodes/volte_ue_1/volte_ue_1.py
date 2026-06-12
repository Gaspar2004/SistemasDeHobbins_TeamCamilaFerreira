"""Nodo VoLTE UE 1. Attach + IMS Registration. Correr:  python volte_ue_1.py [auto]"""
import os
import sys
import threading
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "UE1"
ATTACH_SESSION = "ue1-attach"
IMSREG_SESSION = "ue1-imsreg"
IMSI = "748010000000001"
IMS_ID = "tel:+59899111111"


class UE1(Node):
    def __init__(self, name):
        super().__init__(name)
        self.ue_ip = None

    def on_start(self):
        if "auto" in sys.argv:
            print(f"[{self.name}] auto-start en 2s...")
            time.sleep(2)
        else:
            input(f"[{self.name}] Enter para iniciar el Attach...")
        self.originate("RRC_CONNECTION_REQUEST", "eNB", {"IMSI": IMSI}, session=ATTACH_SESSION)

    def _start_register(self):
        print(f"[{self.name}] Bearer listo -> inicio IMS Registration")
        self.originate("SIP_REGISTER", "P-CSCF",
                       {"ims_id": IMS_ID, "imsi": IMSI, "ip": self.ue_ip},
                       session=IMSREG_SESSION)

    def handle(self, env):
        a = env["action"]
        p = env.get("payload", {})
        # ---- Attach ----
        if a == "RRC_CONNECTION_SETUP":
            return [("RRC_CONNECTION_SETUP_COMPLETE", "eNB",
                     {"IMSI": IMSI, "attach_type": "EPS", "pdn_type": "IPv4v6"})]
        if a == "RRC_CONNECTION_RECONFIGURATION":
            self.ue_ip = p.get("UE_IP")
            print(f"[{self.name}] Default bearer activado. IP asignada: {self.ue_ip}")
            threading.Timer(2, self._start_register).start()   # tras el attach, registrar
            return [
                ("RRC_CONNECTION_RECONFIGURATION_COMPLETE", "eNB", {}),
                ("UPLINK_DIRECT_TRANSFER", "eNB", {"nas": "ACTIVATE_DEFAULT_BEARER_ACCEPT"}),
            ]
        # ---- IMS Registration ----
        if a == "401_UNAUTHORIZED":
            return [("SIP_REGISTER", "P-CSCF",
                     {"ims_id": IMS_ID, "imsi": IMSI, "ip": self.ue_ip, "auth": "response"})]
        if a == "200_OK_REGISTER":
            print(f"[{self.name}] *** REGISTRADO en el IMS ***")
            return [("SIP_SUBSCRIBE", "P-CSCF", {"ims_id": IMS_ID})]
        if a == "200_OK_SUBSCRIBE":
            return []
        if a == "SIP_NOTIFY":
            return [("200_OK_NOTIFY", "P-CSCF", {})]
        return []


if __name__ == "__main__":
    UE1(NODE).run()
