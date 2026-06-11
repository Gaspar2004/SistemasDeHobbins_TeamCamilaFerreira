# `common/` — librería compartida (Python)

Código que usan **todos** los nodos por igual, para que el envelope, las notificaciones y
el timing sean idénticos en los 12. **La construye el integrador en la Fase 1** y el resto
la importa. Nadie reimplementa esto por su cuenta.

## Módulos previstos

### `common/config.py`
- `load_config(path="config/nodes.json") -> dict` — carga el registro de nodos.
- `node_info(name) -> {ip, port, apellido}` y `examiner() -> {ip, port}`.

### `common/transport.py` (UDP)
- `send_message(envelope: dict, dst_name: str)` — serializa a JSON y manda el datagrama al
  `ip:port` del destino (según config).
- `Receiver(node_name, on_message)` — abre el socket UDP del nodo y llama
  `on_message(envelope, addr)` por cada mensaje entrante (en un hilo).

### `common/notify.py` (notificaciones al examinador, con timing)
- `notify_received(node, msg, src_name)` — espera 1 s y manda la notificación
  `sentido="recibido"`.
- `notify_to_send(node, msg, dst_name, extra=None)` — espera 1 s y manda
  `sentido="a_enviar"` (con `extra` para el caso TAS).
- `notify_raw(obj)` — manda un JSON arbitrario (caso S-CSCF `{"message":"fin"}`).
- Construyen el JSON exacto de `docs/02_contratos.md §2` (mismas claves para todos).

### `common/node.py` — clase base / plantilla
Encapsula el patrón "recibir → notificar → decidir → notificar → enviar":

```python
class Node:
    def __init__(self, name): ...
    def run(self): ...                       # levanta el Receiver y queda escuchando
    def handle(self, msg, src):              # LO IMPLEMENTA CADA NODO
        """Devuelve lista de (mensaje_saliente, destino) a enviar, o []."""
        raise NotImplementedError

    # provisto por la base (no tocar):
    def _on_message(self, env, addr):
        notify_received(self.name, env["msg"], env["src"])      # +1s
        for (out_msg, dst, params) in self.handle(env, env["src"]):
            notify_to_send(self.name, out_msg, dst)             # +1s
            send_message(build_envelope(...), dst)
```

Cada integrante solo escribe el método `handle(...)` de sus nodos: la lógica de la máquina
de estados según `docs/01_secuencia_mensajes.md`. El timing, el formato y el transporte ya
vienen resueltos por la base.

## Decisiones técnicas (recordatorio)
- **Lenguaje:** Python 3 (probado: 3.11).
- **Transporte entre nodos:** UDP (mismo modelo que las notificaciones).
- **Despliegue:** cada integrante corre sus nodos en su laptop, en la LAN. Direcciones por
  `config/nodes.json`. Para probar solo, se puede correr todo en localhost (puertos ya son
  distintos por nodo).
- **Concurrencia:** un hilo receptor por nodo; los `sleep(1)` del timing no deben frenar la
  recepción de otros mensajes (usar un hilo/cola por transacción si hace falta con 2 UE).
