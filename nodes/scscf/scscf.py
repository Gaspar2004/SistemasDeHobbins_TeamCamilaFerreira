"""Nodo S-CSCF. STUB: completar handle() segun docs/01_secuencia_mensajes.md.

Mensajes de este nodo (BORRADOR; nombres de 'action' tentativos, cerrar con el equipo):
  - SIP_REGISTER (1er) de I-CSCF -> MAR a HSS
  - MAA de HSS                   -> 401 a I-CSCF
  - SIP_REGISTER (2do) de I-CSCF -> SAR a HSS
  - SAA de HSS                   -> 200_OK a I-CSCF + SIP_REGISTER(3rd-party) a TAS
  - SIP_SUBSCRIBE de P-CSCF      -> 200_OK_SUBSCRIBE + SIP_NOTIFY a P-CSCF
  - 200_OK_NOTIFY de P-CSCF (ULTIMO) -> ademas: self.notify_raw({'message': 'fin'})
  NOTA: distinguir 1er vs 2do REGISTER requiere estado por 'session'.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "common")))
from volte_common import Node  # noqa: E402

NODE = "S-CSCF"


class SCSCF(Node):
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
    SCSCF(NODE).run()
