"""Nodo HSS. STUB: completar handle() segun docs/01_secuencia_mensajes.md.

Mensajes de este nodo (BORRADOR; nombres de 'action' tentativos, cerrar con el equipo):
  - AUTH_INFO_REQUEST de MME        -> AUTH_INFO_ANSWER a MME
  - UPDATE_LOCATION_REQUEST de MME  -> UPDATE_LOCATION_ANSWER a MME
  - UAR de I-CSCF -> UAA a I-CSCF   |  MAR de S-CSCF -> MAA a S-CSCF
  - SAR de S-CSCF -> SAA a S-CSCF   |  UDR de TAS    -> UDA a TAS (datos del usuario)
  NOTA: el HSS guarda el perfil de cada UE (lo reporta el TAS al final).
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "HSS"


class HSS(Node):
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
    HSS(NODE).run()
