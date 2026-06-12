#!/usr/bin/env python3
"""Genera los stubs de los nodos que faltan (plumbing listo + handle() con TODO)."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = os.path.join(ROOT, "nodes")

SERVER = '''"""Nodo __NAME__. STUB: completar handle() segun docs/01_secuencia_mensajes.md.

Mensajes de este nodo (BORRADOR; nombres de 'action' tentativos, cerrar con el equipo):
__HINTS__
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "__NAME__"


class __CLS__(Node):
    def handle(self, env):
        action = env["action"]
        src = env["Node_origin"]
        payload = env.get("payload", {})
        # TODO: implementar segun 'action' (y a veces 'src').
        #       Devolver lista de (accion_saliente, nodo_destino, payload_dict).
        #       [] si este nodo no reenvia nada para ese mensaje.
        print(f"[{self.name}] (TODO) sin regla para {action} de {src}")
        return []


if __name__ == "__main__":
    __CLS__(NODE).run()
'''

SERVERS = [
    ("sgw", "sgw.py", "SGW", "SGW",
     "  - CREATE_SESSION_REQUEST de MME   -> CREATE_SESSION_REQUEST a PGW\n"
     "  - CREATE_SESSION_RESPONSE de PGW  -> CREATE_SESSION_RESPONSE a MME\n"
     "  - MODIFY_BEARER_REQUEST de MME    -> MODIFY_BEARER_RESPONSE a MME"),
    ("pgw", "pgw.py", "PGW", "PGW",
     "  - CREATE_SESSION_REQUEST de SGW   -> CCR a PCRF  (y asigna IP@ al UE)\n"
     "  - CCA de PCRF                     -> CREATE_SESSION_RESPONSE a SGW"),
    ("pcrf", "pcrf.py", "PCRF", "PCRF",
     "  - CCR de PGW     -> CCA a PGW     (Gx)\n"
     "  - AAR de P-CSCF  -> AAA a P-CSCF  (Rx)"),
    ("hss", "hss.py", "HSS", "HSS",
     "  - AUTH_INFO_REQUEST de MME        -> AUTH_INFO_ANSWER a MME\n"
     "  - UPDATE_LOCATION_REQUEST de MME  -> UPDATE_LOCATION_ANSWER a MME\n"
     "  - UAR de I-CSCF -> UAA a I-CSCF   |  MAR de S-CSCF -> MAA a S-CSCF\n"
     "  - SAR de S-CSCF -> SAA a S-CSCF   |  UDR de TAS    -> UDA a TAS (datos del usuario)\n"
     "  NOTA: el HSS guarda el perfil de cada UE (lo reporta el TAS al final)."),
    ("pcscf", "pcscf.py", "P-CSCF", "PCSCF",
     "  - SIP_REGISTER de UEx     -> SIP_REGISTER a I-CSCF\n"
     "  - 401 de I-CSCF           -> 401 a UEx\n"
     "  - 200_OK de I-CSCF        -> 200_OK a UEx   (ademas AAR a PCRF por Rx)\n"
     "  - SIP_SUBSCRIBE de UEx    -> SIP_SUBSCRIBE a S-CSCF\n"
     "  - 200_OK_SUBSCRIBE de S-CSCF -> a UEx\n"
     "  - SIP_NOTIFY de S-CSCF    -> SIP_NOTIFY a UEx\n"
     "  - 200_OK_NOTIFY de UEx    -> 200_OK_NOTIFY a S-CSCF"),
    ("icscf", "icscf.py", "I-CSCF", "ICSCF",
     "  - SIP_REGISTER de P-CSCF  -> UAR a HSS\n"
     "  - UAA de HSS              -> SIP_REGISTER a S-CSCF\n"
     "  - 401 de S-CSCF           -> 401 a P-CSCF\n"
     "  - 200_OK de S-CSCF        -> 200_OK a P-CSCF"),
    ("scscf", "scscf.py", "S-CSCF", "SCSCF",
     "  - SIP_REGISTER (1er) de I-CSCF -> MAR a HSS\n"
     "  - MAA de HSS                   -> 401 a I-CSCF\n"
     "  - SIP_REGISTER (2do) de I-CSCF -> SAR a HSS\n"
     "  - SAA de HSS                   -> 200_OK a I-CSCF + SIP_REGISTER(3rd-party) a TAS\n"
     "  - SIP_SUBSCRIBE de P-CSCF      -> 200_OK_SUBSCRIBE + SIP_NOTIFY a P-CSCF\n"
     "  - 200_OK_NOTIFY de P-CSCF (ULTIMO) -> ademas: self.notify_raw({'message': 'fin'})\n"
     "  NOTA: distinguir 1er vs 2do REGISTER requiere estado por 'session'."),
    ("tas", "tas.py", "TAS", "TAS",
     "  - SIP_REGISTER de S-CSCF  -> UDR a HSS\n"
     "  - UDA de HSS              -> 200_OK a S-CSCF\n"
     "  ULTIMO ENVIO: en la notify_a_enviar del 200_OK incluir extra={'ues_registrados': [...]}\n"
     "  (IMS Public Id + IP de cada UE + datos del usuario que vinieron del HSS)."),
]

UE2 = '''"""Nodo UE2. Inicia el Attach (mirror de UE1). Correr:  python volte_ue_2.py [auto]"""
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "UE2"
SESSION = "ue2-attach"
IMSI = "748010000000002"


class UE2(Node):
    def on_start(self):
        if "auto" in sys.argv:
            time.sleep(2)
        else:
            input(f"[{self.name}] Enter para iniciar el Attach...")
        self.originate("RRC_CONNECTION_REQUEST", "eNB", {"IMSI": IMSI}, session=SESSION)

    def handle(self, env):
        if env["action"] == "RRC_CONNECTION_SETUP":
            return [("RRC_CONNECTION_SETUP_COMPLETE", "eNB",
                     {"IMSI": IMSI, "attach_type": "EPS", "pdn_type": "IPv4v6"})]
        return []


if __name__ == "__main__":
    UE2(NODE).run()
'''


def main():
    for d, fname, name, cls, hints in SERVERS:
        content = SERVER.replace("__NAME__", name).replace("__CLS__", cls).replace("__HINTS__", hints)
        path = os.path.join(N, d, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("escrito:", path)
    p = os.path.join(N, "volte_ue_2", "volte_ue_2.py")
    with open(p, "w", encoding="utf-8") as f:
        f.write(UE2)
    print("escrito:", p)


if __name__ == "__main__":
    main()
