# Nodo: I-CSCF   (R6 / E6)

**Operado por:** _________________  (poné tu apellido también en `config/nodes.json`)

**Rol:** Interrogating CSCF. UAR/UAA con HSS, asigna y reenvia al S-CSCF.

## Qué implementar
- Solo el método `handle(msg, src)` usando `common/` (ver `common/README.md`).
- Lógica según la máquina de estados de `docs/01_secuencia_mensajes.md`.
- Estado y vecinos: ficha de este nodo en `docs/03_asignacion_nodos.md`.
- Envelope y notificaciones: `docs/02_contratos.md` (NO reimplementar, usar `common/`).

## Checklist
- [ ] `handle()` cubre todos los mensajes que este nodo recibe
- [ ] por cada recibido: notifica `recibido` (+1s) y `a_enviar` (+1s) antes de enviar
- [ ] estado por UE correcto (el flujo corre 2 veces, una por UE)
- [ ] probado contra `mock_examiner` y stubs de los vecinos
- [ ] casos especiales (si aplica: TAS reporta UEs / S-CSCF emite `fin`)

> Código del nodo: agregar `icscf.py` en esta carpeta al arrancar la Fase 3.
