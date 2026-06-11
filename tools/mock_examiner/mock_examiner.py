#!/usr/bin/env python3
"""
Examinador de prueba: escucha en UDP 55555 e imprime/loguea las notificaciones JSON
que mandan los nodos. Sirve para probar localmente sin el PC real del examinador.

Uso:
    python tools/mock_examiner/mock_examiner.py [puerto]

Por defecto escucha en 0.0.0.0:55555 (todas las interfaces, para que lleguen
notificaciones desde otras laptops de la LAN). Guarda un log en notificaciones.log.
"""
import json
import socket
import sys
from datetime import datetime

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 55555
LOGFILE = "notificaciones.log"


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", PORT))
    print(f"[mock_examiner] escuchando en UDP 0.0.0.0:{PORT} ... (Ctrl+C para salir)\n")

    n = 0
    with open(LOGFILE, "a", encoding="utf-8") as log:
        log.write(f"\n===== sesion iniciada {datetime.now().isoformat()} =====\n")
        while True:
            try:
                data, addr = sock.recvfrom(65535)
            except KeyboardInterrupt:
                break
            n += 1
            recv_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            try:
                obj = json.loads(data.decode("utf-8"))
                pretty = json.dumps(obj, ensure_ascii=False, indent=2)
            except Exception:
                obj, pretty = None, data.decode("utf-8", "replace")

            # Resaltar casos especiales del enunciado
            tag = ""
            if isinstance(obj, dict):
                if obj.get("message") == "fin":
                    tag = "  <<< FIN (S-CSCF) >>>"
                elif "ues_registrados" in obj:
                    tag = "  <<< TAS: UEs registrados >>>"

            line = f"#{n:03d} [{recv_time}] desde {addr[0]}:{addr[1]}{tag}"
            print(line)
            print(pretty)
            print("-" * 60)
            log.write(line + "\n" + pretty + "\n")
            log.flush()

    print(f"\n[mock_examiner] {n} notificaciones recibidas. Log: {LOGFILE}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[mock_examiner] detenido.")
