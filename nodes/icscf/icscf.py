"""Nodo I-CSCF. Interrogating CSCF. Correr:  python icscf.py"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "I-CSCF"


class ICSCF(Node):
    def __init__(self, name):
        super().__init__(name)
        self.pending_reg = {}   # por session: el SIP_REGISTER en curso

    def handle(self, env):
        a = env["action"]
        p = env.get("payload", {})
        s = env.get("session")
        if a == "SIP_REGISTER":        # del P-CSCF -> consulto al HSS quien es el S-CSCF
            self.pending_reg[s] = p
            return [("UAR", "HSS", {"ims_id": p.get("ims_id")})]
        if a == "UAA":                 # del HSS -> reenvio el REGISTER al S-CSCF
            return [("SIP_REGISTER", "S-CSCF", self.pending_reg.get(s, {}))]
        if a == "401_UNAUTHORIZED":    # del S-CSCF -> al P-CSCF
            return [("401_UNAUTHORIZED", "P-CSCF", p)]
        if a == "200_OK_REGISTER":     # del S-CSCF -> al P-CSCF
            return [("200_OK_REGISTER", "P-CSCF", p)]
        print(f"[{self.name}] (TODO) sin regla para {a} de {env['Node_origin']}")
        return []


if __name__ == "__main__":
    ICSCF(NODE).run()
