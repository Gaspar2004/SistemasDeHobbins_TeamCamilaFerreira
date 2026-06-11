#!/usr/bin/env python3
"""Genera/regenera el README.md de cada carpeta de nodo en nodes/."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NODES_DIR = os.path.join(ROOT, "nodes")

NODES = [
    ("volte_ue_1", "VoLTE UE 1", "R7 / E8",
     "Equipo de usuario 1. Origina Attach y REGISTER/SUBSCRIBE. Extremo del flujo."),
    ("volte_ue_2", "VoLTE UE 2", "R7 / E8",
     "Equipo de usuario 2. Igual que UE1 con otra identidad IMS."),
    ("enb", "eNB", "R5 / E5",
     "Estacion base. Relay radio (RRC) <-> NAS/S1 (MME)."),
    ("mme", "MME", "R8 / E6",
     "Mobility Mgmt. Auth con HSS+UE, Update Location, Create/Modify Session."),
    ("sgw", "SGW", "R3 / E3",
     "Serving GW. Relay de Create Session y Modify Bearer entre MME y PGW."),
    ("pgw", "PGW", "R2 / E2",
     "Packet GW. Asigna IP al UE, dispara CCR al PCRF (Gx)."),
    ("pcrf", "PCRF", "R2 / E2",
     "Politicas. CCR/CCA (Gx) con PGW y AAR/AAA (Rx) con P-CSCF."),
    ("hss", "HSS", "R7 / E6",
     "Base de suscriptores. Auth, Update Location, Cx (UAR/MAR/SAR), Sh (UDR)."),
    ("pcscf", "P-CSCF", "R11 / E10",
     "Proxy SIP de entrada del UE. REGISTER/401/200, Rx, SUBSCRIBE/NOTIFY. NODO MAS CARGADO."),
    ("icscf", "I-CSCF", "R6 / E6",
     "Interrogating CSCF. UAR/UAA con HSS, asigna y reenvia al S-CSCF."),
    ("scscf", "S-CSCF", "R11 / E11",
     "Serving CSCF. Registro, 401/200, third-party REGISTER al TAS. Emite {message:fin}. NODO MAS CARGADO."),
    ("tas", "TAS", "R4 / E4",
     "App server. Recibe third-party REGISTER, descarga datos (Sh), reporta UEs registrados al final."),
]

TMPL = """# Nodo: {name}   ({re})

**Operado por:** _________________  (poné tu apellido también en `config/nodes.json`)

**Rol:** {rol}

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

> Código del nodo: agregar `{dir}.py` en esta carpeta al arrancar la Fase 3.
"""


def main():
    for d, name, re, rol in NODES:
        path = os.path.join(NODES_DIR, d, "README.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(TMPL.format(name=name, re=re, rol=rol, dir=d))
        print("escrito:", path)


if __name__ == "__main__":
    main()
