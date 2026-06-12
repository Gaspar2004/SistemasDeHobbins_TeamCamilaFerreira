"""Nodo P-CSCF. STUB: completar handle() segun docs/01_secuencia_mensajes.md.

Mensajes de este nodo (BORRADOR; nombres de 'action' tentativos, cerrar con el equipo):
  - SIP_REGISTER de UEx     -> SIP_REGISTER a I-CSCF
  - 401 de I-CSCF           -> 401 a UEx
  - 200_OK de I-CSCF        -> 200_OK a UEx   (ademas AAR a PCRF por Rx)
  - SIP_SUBSCRIBE de UEx    -> SIP_SUBSCRIBE a S-CSCF
  - 200_OK_SUBSCRIBE de S-CSCF -> a UEx
  - SIP_NOTIFY de S-CSCF    -> SIP_NOTIFY a UEx
  - 200_OK_NOTIFY de UEx    -> 200_OK_NOTIFY a S-CSCF
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "P-CSCF"


class PCSCF(Node):
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
    PCSCF(NODE).run()
