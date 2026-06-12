"""Nodo I-CSCF. STUB: completar handle() segun docs/01_secuencia_mensajes.md.

Mensajes de este nodo (BORRADOR; nombres de 'action' tentativos, cerrar con el equipo):
  - SIP_REGISTER de P-CSCF  -> UAR a HSS
  - UAA de HSS              -> SIP_REGISTER a S-CSCF
  - 401 de S-CSCF           -> 401 a P-CSCF
  - 200_OK de S-CSCF        -> 200_OK a P-CSCF
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "I-CSCF"


class ICSCF(Node):
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
    ICSCF(NODE).run()
