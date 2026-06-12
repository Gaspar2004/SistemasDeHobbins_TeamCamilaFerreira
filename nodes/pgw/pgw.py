"""Nodo PGW. Asigna IP@ al UE y dispara la politica (Gx). Correr:  python pgw.py"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "PGW"


def _ip_para(session):
    return "10.0.0.11" if (session or "").startswith("ue1") else "10.0.0.12"


class PGW(Node):
    def handle(self, env):
        a = env["action"]
        p = env.get("payload", {})
        if a == "CREATE_SESSION_REQUEST":      # de SGW -> CCR a PCRF (Gx)
            return [("CCR", "PCRF",
                     {"IMSI": p.get("IMSI"), "QCI": p.get("QCI"), "ARP": p.get("ARP")})]
        if a == "CCA":                          # de PCRF -> responde a SGW con la IP del UE
            ue_ip = _ip_para(env.get("session"))
            return [("CREATE_SESSION_RESPONSE", "SGW",
                     {"UE_IP": ue_ip, "QCI": 5, "ARP": 1, "APN_AMBR": "100M"})]
        print(f"[{self.name}] (TODO) sin regla para {a} de {env['Node_origin']}")
        return []


if __name__ == "__main__":
    PGW(NODE).run()
