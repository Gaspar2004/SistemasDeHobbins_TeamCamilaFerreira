"""Nodo TAS. App server. Recibe el 3rd-party REGISTER, baja datos del HSS (Sh) y, en su
ultimo envio, reporta los UE registrados. Correr:  python tas.py"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "TAS"


class TAS(Node):
    def __init__(self, name):
        super().__init__(name)
        self.pending = {}       # por session: datos del REGISTER (ims_id, ip)
        self.registrados = {}   # ims_id -> {ims_public_id, ip, datos_hss}

    def handle(self, env):
        a = env["action"]
        p = env.get("payload", {})
        s = env.get("session")
        if a == "SIP_REGISTER":          # del S-CSCF -> bajo datos del usuario al HSS (Sh)
            self.pending[s] = p
            return [("UDR", "HSS", {"ims_id": p.get("ims_id")})]
        if a == "UDA":                   # del HSS -> guardo y respondo OK (ULTIMO ENVIO)
            reg = self.pending.get(s, {})
            self.registrados[reg.get("ims_id")] = {
                "ims_public_id": reg.get("ims_id"),
                "ip": reg.get("ip"),
                "datos_hss": p,
            }
            extra = {"ues_registrados": list(self.registrados.values())}
            print(f"[{self.name}] UE registrado: {reg.get('ims_id')} (total {len(self.registrados)})")
            return [("200_OK_THIRDPARTY", "S-CSCF", {}, extra)]
        print(f"[{self.name}] (TODO) sin regla para {a} de {env['Node_origin']}")
        return []


if __name__ == "__main__":
    TAS(NODE).run()
