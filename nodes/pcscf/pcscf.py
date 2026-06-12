"""Nodo P-CSCF. Proxy SIP de entrada del UE. Correr:  python pcscf.py"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "P-CSCF"


def _ue(session):
    return "UE1" if (session or "").startswith("ue1") else "UE2"


class PCSCF(Node):
    def handle(self, env):
        a = env["action"]
        p = env.get("payload", {})
        ue = _ue(env.get("session"))
        if a == "SIP_REGISTER":            # del UE -> al I-CSCF
            return [("SIP_REGISTER", "I-CSCF", p)]
        if a == "401_UNAUTHORIZED":        # del I-CSCF -> al UE
            return [("401_UNAUTHORIZED", ue, p)]
        if a == "200_OK_REGISTER":         # del I-CSCF -> reserva recursos (Rx) y avisa al UE
            return [("AAR", "PCRF", {"ims_id": p.get("ims_id")}),
                    ("200_OK_REGISTER", ue, {})]
        if a == "AAA":                     # del PCRF -> nada mas
            return []
        if a == "SIP_SUBSCRIBE":           # del UE -> al S-CSCF
            return [("SIP_SUBSCRIBE", "S-CSCF", p)]
        if a == "200_OK_SUBSCRIBE":        # del S-CSCF -> al UE
            return [("200_OK_SUBSCRIBE", ue, {})]
        if a == "SIP_NOTIFY":              # del S-CSCF -> al UE
            return [("SIP_NOTIFY", ue, p)]
        if a == "200_OK_NOTIFY":           # del UE -> al S-CSCF
            return [("200_OK_NOTIFY", "S-CSCF", {})]
        print(f"[{self.name}] (TODO) sin regla para {a} de {env['Node_origin']}")
        return []


if __name__ == "__main__":
    PCSCF(NODE).run()
