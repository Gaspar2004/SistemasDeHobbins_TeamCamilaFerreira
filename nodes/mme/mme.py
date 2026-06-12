"""Nodo MME. Maquina de Attach (sin el bloque de Authentication, que queda pendiente).
Correr:  python mme.py"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "MME"


class MME(Node):
    def handle(self, env):
        a = env["action"]
        p = env.get("payload", {})
        if a == "ATTACH_REQUEST":
            # TODO pendiente: bloque Authentication/Security con HSS y UE (A05-A08).
            print(f"[{self.name}] Attach de IMSI={p.get('IMSI')} -> Update Location")
            return [("UPDATE_LOCATION_REQUEST", "HSS", {"IMSI": p.get("IMSI")})]
        if a == "UPDATE_LOCATION_ANSWER":
            return [("CREATE_SESSION_REQUEST", "SGW",
                     {"IMSI": p.get("IMSI"), "APN": "ims", "QCI": 5, "ARP": 1, "APN_AMBR": "100M"})]
        if a == "CREATE_SESSION_RESPONSE":
            # Ya tenemos la IP del UE -> activar el default bearer por la radio
            return [("E_RAB_SETUP_REQUEST", "eNB",
                     {"UE_IP": p.get("UE_IP"), "QCI": 5, "ARP": 1, "bearer": "default"})]
        if a == "E_RAB_SETUP_RESPONSE":
            return []   # se espera el Attach Complete del UE (via eNB)
        if a == "ATTACH_COMPLETE":
            return [("MODIFY_BEARER_REQUEST", "SGW", {})]
        if a == "MODIFY_BEARER_RESPONSE":
            print(f"[{self.name}] *** DEFAULT BEARER ESTABLECIDO -- Attach COMPLETO ***")
            return []
        return []


if __name__ == "__main__":
    MME(NODE).run()
