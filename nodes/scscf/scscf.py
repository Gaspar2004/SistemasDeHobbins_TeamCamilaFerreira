"""Nodo S-CSCF. Serving CSCF. Registro del usuario + 3rd-party register al TAS.
Emite {"message":"fin"} al final. Correr:  python scscf.py"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "S-CSCF"


class SCSCF(Node):
    def __init__(self, name):
        super().__init__(name)
        self.reg_count = {}   # por session: cuantos REGISTER vimos (1ro=desafio, 2do=ok)
        self.pending = {}     # por session: el REGISTER en curso

    def handle(self, env):
        a = env["action"]
        p = env.get("payload", {})
        s = env.get("session")
        if a == "SIP_REGISTER":
            self.pending[s] = p
            n = self.reg_count.get(s, 0) + 1
            self.reg_count[s] = n
            if n == 1:                       # 1er REGISTER -> desafio (MAR)
                return [("MAR", "HSS", {"ims_id": p.get("ims_id")})]
            return [("SAR", "HSS", {"ims_id": p.get("ims_id")})]   # 2do -> asignacion
        if a == "MAA":                       # del HSS -> 401 con desafio
            return [("401_UNAUTHORIZED", "I-CSCF", {"nonce": "abc123"})]
        if a == "SAA":                       # del HSS -> OK al UE + registro 3rd-party al TAS
            reg = self.pending.get(s, {})
            return [("200_OK_REGISTER", "I-CSCF", {}),
                    ("SIP_REGISTER", "TAS", reg)]
        if a == "200_OK_THIRDPARTY":         # del TAS -> TAS quedo registrado
            return []
        if a == "SIP_SUBSCRIBE":             # del P-CSCF -> OK + NOTIFY con el estado
            return [("200_OK_SUBSCRIBE", "P-CSCF", {}),
                    ("SIP_NOTIFY", "P-CSCF", {"reg_state": "registered"})]
        if a == "200_OK_NOTIFY":             # ULTIMO mensaje recibido -> notificacion "fin"
            print(f"[{self.name}] *** Registration COMPLETA -> envio fin ***")
            self.notify_raw({"message": "fin"})
            return []
        print(f"[{self.name}] (TODO) sin regla para {a} de {env['Node_origin']}")
        return []


if __name__ == "__main__":
    SCSCF(NODE).run()
