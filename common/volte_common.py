"""
Libreria compartida de los nodos VoLTE (Team-C).

Resuelve, igual para todos los nodos:
  - carga del registro de nodos (config/nodes.json)
  - transporte UDP (envelope acordado: Node_origin/IP_origin/.../session/action/payload)
  - notificaciones al examinador (UDP 55555) con el timing de 1 segundo

Cada nodo solo define on_start() (si origina algo) y handle(env) (que devuelve la lista
de mensajes a enviar a continuacion).
"""
import json
import os
import socket
import time
from datetime import datetime, timezone, timedelta

# Uruguay UTC-3 (la notificacion pide "hora del nodo")
TZ = timezone(timedelta(hours=-3))


def _now_iso():
    return datetime.now(TZ).isoformat(timespec="milliseconds")


def _now_hora():
    return datetime.now(TZ).strftime("%H:%M:%S.%f")[:-3]


def load_config(path=None):
    if path is None:
        path = os.environ.get("VOLTE_CONFIG")   # permite probar con otro config
    if path is None:
        here = os.path.dirname(os.path.abspath(__file__))
        path = os.path.abspath(os.path.join(here, "..", "config", "nodes.json"))
    with open(path, encoding="utf-8") as f:
        return json.load(f)


class Node:
    def __init__(self, name, config_path=None):
        self.name = name
        self.cfg = load_config(config_path)
        self.nodes = self.cfg["nodes"]
        if name not in self.nodes:
            raise SystemExit(f"El nodo '{name}' no esta en config/nodes.json")
        self.me = self.nodes[name]
        self.examiner = self.cfg["examiner"]
        self.delay = self.cfg.get("notify_delay_seconds", 1)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.me["port"]))
        self.notif_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # ---------- envelope entre nodos (formato acordado) ----------
    def _build(self, action, dst, payload, session):
        d = self.nodes[dst]
        return {
            "Node_origin": self.name,
            "IP_origin": self.me["ip"],
            "Node_dest": dst,
            "IP_dest": d["ip"],
            "timestamp": _now_iso(),
            "session": session,
            "action": action,
            "payload": payload or {},
        }

    def _send(self, action, dst, payload, session):
        d = self.nodes[dst]
        env = self._build(action, dst, payload, session)
        self.sock.sendto(json.dumps(env).encode("utf-8"), (d["ip"], d["port"]))

    # ---------- notificaciones al examinador (UDP 55555) ----------
    # OJO: los nombres de clave de la notificacion son PROVISORIOS (el equipo
    # todavia tiene que cerrar este esquema). Cambiarlos solo aca afecta a todos.
    def _notify(self, obj):
        self.notif_sock.sendto(
            json.dumps(obj, ensure_ascii=False).encode("utf-8"),
            (self.examiner["ip"], self.examiner["port"]),
        )

    def _notif_base(self, sentido, mensaje, contraparte, contraparte_ip):
        return {
            "hora": _now_hora(),
            "nodo": self.name,
            "ip": self.me["ip"],
            "apellido": self.me.get("apellido", ""),
            "sentido": sentido,                 # "recibido" | "a_enviar"
            "mensaje": mensaje,
            "contraparte": contraparte,
            "contraparte_ip": contraparte_ip,
        }

    def notify_recibido(self, mensaje, contraparte, contraparte_ip):
        time.sleep(self.delay)
        self._notify(self._notif_base("recibido", mensaje, contraparte, contraparte_ip))

    def notify_a_enviar(self, mensaje, contraparte, contraparte_ip, extra=None):
        time.sleep(self.delay)
        n = self._notif_base("a_enviar", mensaje, contraparte, contraparte_ip)
        if extra:
            n.update(extra)
        self._notify(n)

    def notify_raw(self, obj):
        self._notify(obj)

    # ---------- API para los nodos ----------
    def originate(self, action, dst, payload=None, session=None):
        """Enviar un mensaje que este nodo ORIGINA (sin haberlo disparado un recibido)."""
        d = self.nodes[dst]
        self.notify_a_enviar(action, dst, d["ip"])
        self._send(action, dst, payload, session)
        print(f"[{self.name}] -> (origina) {action} a {dst}")

    def on_start(self):
        """Override: se ejecuta una vez al arrancar (para nodos que inician un flujo)."""
        pass

    def handle(self, env):
        """Override: devolver lista de (action, destino, payload) a enviar. [] si nada."""
        return []

    # ---------- loop principal ----------
    def run(self):
        print(f"[{self.name}] escuchando UDP {self.me['ip']}:{self.me['port']}  "
              f"-> examinador {self.examiner['ip']}:{self.examiner['port']}")
        self.on_start()
        while True:
            data, _addr = self.sock.recvfrom(65535)
            try:
                env = json.loads(data.decode("utf-8"))
            except Exception as e:
                print(f"[{self.name}] JSON invalido descartado: {e}")
                continue
            self._process(env)

    def _process(self, env):
        action = env.get("action")
        src = env.get("Node_origin")
        src_ip = env.get("IP_origin")
        print(f"[{self.name}] <- {action} de {src}")
        self.notify_recibido(action, src, src_ip)        # +1s
        for out in (self.handle(env) or []):
            # cada salida: (action, destino, payload) o (action, destino, payload, extra_notif)
            extra = None
            if len(out) == 4:
                out_action, dst, payload, extra = out
            else:
                out_action, dst, payload = out
            dst_ip = self.nodes[dst]["ip"]
            self.notify_a_enviar(out_action, dst, dst_ip, extra=extra)  # +1s
            self._send(out_action, dst, payload, env.get("session"))
            print(f"[{self.name}] -> {out_action} a {dst}")
