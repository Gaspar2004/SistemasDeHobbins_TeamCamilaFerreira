"""Nodo HSS. Base de suscriptores. Parte A implementada (Update Location).
Cx/Sh (UAR/MAR/SAR/UDR) quedan como TODO para la Parte B (IMS). Correr:  python hss.py

Mensajes de este nodo (BORRADOR):
  - UPDATE_LOCATION_REQUEST de MME  -> UPDATE_LOCATION_ANSWER a MME      [Parte A, HECHO]
  - AUTH_INFO_REQUEST de MME        -> AUTH_INFO_ANSWER a MME            [TODO auth]
  - UAR de I-CSCF -> UAA a I-CSCF   |  MAR de S-CSCF -> MAA a S-CSCF     [TODO Parte B]
  - SAR de S-CSCF -> SAA a S-CSCF   |  UDR de TAS    -> UDA a TAS        [TODO Parte B]
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


class HSS(Node):
    def handle(self, env):
        a = env["action"]
        p = env.get("payload", {})
        if a == "UPDATE_LOCATION_REQUEST":
            imsi = p.get("IMSI")
            prof = SUBSCRIBERS.get(imsi, {})
            print(f"[{self.name}] Update Location de IMSI={imsi} ({prof.get('nombre')})")
            return [("UPDATE_LOCATION_ANSWER", "MME",
                     {"IMSI": imsi, "msisdn": prof.get("msisdn"), "perfil": prof.get("perfil")})]
        # TODO Parte B (IMS): UAR->UAA, MAR->MAA, SAR->SAA, UDR->UDA, AUTH_INFO_REQUEST->ANSWER
        print(f"[{self.name}] (TODO) sin regla para {a} de {env['Node_origin']}")
        return []


if __name__ == "__main__":
    HSS(NODE).run()
