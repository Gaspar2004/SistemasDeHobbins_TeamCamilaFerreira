#!/usr/bin/env python3
"""
Inyecta UN mensaje a un nodo, para probarlo aislado (sin levantar toda la cadena).

Uso:
    python tools/inject.py <NODO_DEST> <ACTION> [NODO_ORIGEN] [session]

Ejemplos:
    python tools/inject.py P-CSCF SIP_REGISTER UE1 ue1-imsreg
    python tools/inject.py SGW CREATE_SESSION_REQUEST MME ue1-attach

Lee config/nodes.json para saber a que IP:puerto mandar. El payload va vacio (agregarlo
a mano en el codigo si tu nodo lo necesita).
"""
import json
import os
import socket
import sys
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    dest = sys.argv[1]
    action = sys.argv[2]
    origin = sys.argv[3] if len(sys.argv) > 3 else "UE1"
    session = sys.argv[4] if len(sys.argv) > 4 else "test"

    cfg = json.load(open(os.path.join(ROOT, "config", "nodes.json"), encoding="utf-8"))
    nodes = cfg["nodes"]
    if dest not in nodes:
        print(f"Nodo destino '{dest}' no esta en nodes.json"); sys.exit(1)
    d = nodes[dest]
    o = nodes.get(origin, {"ip": "127.0.0.1"})

    env = {
        "Node_origin": origin,
        "IP_origin": o.get("ip", "127.0.0.1"),
        "Node_dest": dest,
        "IP_dest": d["ip"],
        "timestamp": datetime.now(timezone(timedelta(hours=-3))).isoformat(timespec="milliseconds"),
        "session": session,
        "action": action,
        "payload": {},
    }
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(json.dumps(env).encode("utf-8"), (d["ip"], d["port"]))
    print(f"Enviado {action} -> {dest} ({d['ip']}:{d['port']}) como si viniera de {origin}")


if __name__ == "__main__":
    main()
