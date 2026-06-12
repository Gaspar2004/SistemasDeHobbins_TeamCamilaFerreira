"""Nodo SGW. STUB: completar handle() segun docs/01_secuencia_mensajes.md.

Mensajes de este nodo (BORRADOR; nombres de 'action' tentativos, cerrar con el equipo):
  - CREATE_SESSION_REQUEST de MME   -> CREATE_SESSION_REQUEST a PGW
  - CREATE_SESSION_RESPONSE de PGW  -> CREATE_SESSION_RESPONSE a MME
  - MODIFY_BEARER_REQUEST de MME    -> MODIFY_BEARER_RESPONSE a MME
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "SGW"


class SGW(Node):
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
    SGW(NODE).run()
