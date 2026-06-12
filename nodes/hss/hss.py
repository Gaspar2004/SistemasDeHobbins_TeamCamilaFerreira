"""Nodo HSS. Base de suscriptores. Parte A (Update Location) + Parte B (Cx/Sh).
Correr:  python hss.py

Mensajes:
  - UPDATE_LOCATION_REQUEST de MME  -> UPDATE_LOCATION_ANSWER a MME   [Parte A]
  - UAR de I-CSCF -> UAA a I-CSCF    |  MAR de S-CSCF -> MAA a S-CSCF  [Parte B, Cx]
  - SAR de S-CSCF -> SAA a S-CSCF    |  UDR de TAS    -> UDA a TAS     [Parte B, Cx/Sh]
  (AUTH_INFO del bloque de Authentication queda pendiente.)
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "HSS"

# Perfil simulado de cada suscriptor (lo que el TAS reportara al final).
SUBSCRIBERS = {
    "748010000000001": {"msisdn": "59899111111", "ims_public_id": "tel:+59899111111",
                        "nombre": "Usuario UE1", "perfil": "VoLTE"},
    "748010000000002": {"msisdn": "59899222222", "ims_public_id": "tel:+59899222222",
                        "nombre": "Usuario UE2", "perfil": "VoLTE"},
}
BY_IMS = {v["ims_public_id"]: v for v in SUBSCRIBERS.values()}


class HSS(Node):
    def handle(self, env):
        a = env["action"]
        p = env.get("payload", {})
        # ---- Parte A ----
        if a == "UPDATE_LOCATION_REQUEST":
            prof = SUBSCRIBERS.get(p.get("IMSI"), {})
            print(f"[{self.name}] Update Location de IMSI={p.get('IMSI')} ({prof.get('nombre')})")
            return [("UPDATE_LOCATION_ANSWER", "MME",
                     {"IMSI": p.get("IMSI"), "msisdn": prof.get("msisdn"), "perfil": prof.get("perfil")})]
        # ---- Parte B: Cx ----
        if a == "UAR":
            return [("UAA", "I-CSCF", {"ims_id": p.get("ims_id"), "scscf": "S-CSCF"})]
        if a == "MAR":
            return [("MAA", "S-CSCF", {"ims_id": p.get("ims_id"), "av": "auth-vector"})]
        if a == "SAR":
            return [("SAA", "S-CSCF", {"ims_id": p.get("ims_id"), "perfil": "VoLTE"})]
        # ---- Parte B: Sh (datos de usuario que reportara el TAS) ----
        if a == "UDR":
            prof = BY_IMS.get(p.get("ims_id"), {})
            print(f"[{self.name}] UDR de TAS para {p.get('ims_id')} -> envio perfil")
            return [("UDA", "TAS", {"msisdn": prof.get("msisdn"), "nombre": prof.get("nombre"),
                                    "perfil": prof.get("perfil")})]
        print(f"[{self.name}] (TODO) sin regla para {a} de {env['Node_origin']}")
        return []


if __name__ == "__main__":
    HSS(NODE).run()
