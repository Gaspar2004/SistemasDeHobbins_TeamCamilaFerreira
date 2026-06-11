# Secuencia de mensajes (Figure 3) — BORRADOR a reconciliar con GSMA V1.1

> **ESTO ES UN BORRADOR** reconstruido de las figuras del enunciado. Es el **contrato
> más importante** del proyecto: define qué mensaje recibe cada nodo y qué mensaje envía
> a continuación. **Tarea de Fase 1:** contrastarlo con *GSMA VoLTE Service Description
> and Implementation Guide V1.1, §3.2.1.3.1 y §3.2.1.3.2* y dejarlo **definitivo**, de
> modo que las cuentas Recibe/Emite por nodo coincidan con la tabla objetivo (al final).
> Hasta que no esté cerrado, **nadie debe codificar la lógica de mensajes**, solo el
> esqueleto.

Notación: `N -> M : Mensaje [parámetros]`. Cada flecha es **un** mensaje de señalización
UDP entre nodos. El flujo corre **una vez por cada VoLTE UE** (ver "Ejecución con 2 UE").

---

## Parte A — VoLTE UE Attach (§3.2.1.3.1)

Objetivo: establecer el **Default Bearer** para señalización IMS (APN de IMS, QCI 5).

| #   | Origen   | Destino | Mensaje                                   | Parámetros / notas |
|-----|----------|---------|-------------------------------------------|--------------------|
| A01 | VoLTE UE | eNB     | RRC Connection Request                    | |
| A02 | eNB      | VoLTE UE| RRC Connection Setup                      | |
| A03 | VoLTE UE | eNB     | RRC Connection Setup Complete             | = Attach Req; lleva `[Dedicated NAS][PDN Connectivity Request]` |
| A04 | eNB      | MME     | Attach req (Uplink NAS Transport)         | `[NAS PDU][EPS SM: PDN Connectivity Request]` |
| A05 | MME      | HSS     | Authentication Information Request         | **(bloque Auth/Security — simplificado, ver nota)** |
| A06 | HSS      | MME     | Authentication Information Answer          | vectores de autenticación |
| A07 | MME      | VoLTE UE| Authentication Request / Security Mode     | challenge |
| A08 | VoLTE UE | MME     | Authentication Response / Security Complete| response |
| A09 | MME      | HSS     | Update Location Request                    | |
| A10 | HSS      | MME     | Update Location Answer                     | perfil de suscriptor |
| A11 | MME      | SGW     | Create Session Request                     | `IMS-APN; QCI:5; ARP; APN-AMBR` |
| A12 | SGW      | PGW     | Create Session Request                     | `IMS-APN; QCI:5; ARP; APN-AMBR` |
| A13 | PGW      | PCRF    | CCR (Credit Control Request)               | `IP@; QCI:5; ARP; APN-AMBR` (Gx) |
| A14 | PCRF     | PGW     | CCA (Credit Control Answer)                | `QCI:5; ARP; APN-AMBR; IP default rule TFT` |
| A15 | PGW      | SGW     | Create Session Response                    | `IP@; QCI:5; ARP; APN-AMBR` |
| A16 | SGW      | MME     | Create Session Response                    | `IP@; QCI:5; ARP; APN-AMBR` |
| A17 | MME      | eNB     | E-RAB Setup Request                        | `QCI:5; ARP; UE-AMBR` + `[Activate Default Bearer Request][IMS-APN; IP@; QCI:5; APN-AMBR]` |
| A18 | eNB      | VoLTE UE| RRC Connection Reconfiguration             | `[Activate Default Bearer Request]` |
| A19 | VoLTE UE | eNB     | RRC Connection Reconfiguration Complete    | |
| A20 | eNB      | MME     | E-RAB Setup Response                        | |
| A21 | VoLTE UE | eNB     | Uplink Direct Transfer                      | `[Activate Default Bearer Accept]` |
| A22 | eNB      | MME     | Attach Complete (Uplink NAS Transport)      | `[Activate Default Bearer Accept]` |
| A23 | MME      | SGW     | Modify Bearer Request                        | |
| A24 | SGW      | MME     | Modify Bearer Response                        | → **Default Bearer establecido** |

> **Nota Auth/Security (A05–A08):** la Figure 3 abstrae todo esto como una sola flecha
> bidireccional "Authentication/Security" entre UE y HSS (vía MME). Acá se modeló como 4
> mensajes para que el UE y el MME tengan tráfico de autenticación. **El número exacto de
> mensajes de este bloque hay que ajustarlo** para que las cuentas por nodo cuadren con la
> tabla objetivo. Es el punto más ambiguo de la Parte A.

---

## Parte B — IMS Registration (§3.2.1.3.2)

Objetivo: registrar el UE en el IMS (doble REGISTER con desafío 401, registro de tercera
parte al TAS, y suscripción al estado de registro). SIP sobre el bearer ya establecido.

### B.1 — Primer REGISTER → 401 Unauthorised
| #   | Origen   | Destino | Mensaje            | Notas |
|-----|----------|---------|--------------------|-------|
| B01 | VoLTE UE | P-CSCF  | SIP REGISTER       | sin credenciales |
| B02 | P-CSCF   | I-CSCF  | SIP REGISTER       | |
| B03 | I-CSCF   | HSS     | UAR                | User Authorization Request (Cx) |
| B04 | HSS      | I-CSCF  | UAA                | devuelve capacidades / S-CSCF |
| B05 | I-CSCF   | S-CSCF  | SIP REGISTER       | I-CSCF asigna S-CSCF |
| B06 | S-CSCF   | HSS     | MAR                | Multimedia Auth Request (Cx) |
| B07 | HSS      | S-CSCF  | MAA                | vectores de autenticación |
| B08 | S-CSCF   | I-CSCF  | 401 Unauthorised   | challenge |
| B09 | I-CSCF   | P-CSCF  | 401 Unauthorised   | |
| B10 | P-CSCF   | VoLTE UE| 401 Unauthorised   | |

### B.2 — Segundo REGISTER → 200 OK
| #   | Origen   | Destino | Mensaje            | Notas |
|-----|----------|---------|--------------------|-------|
| B11 | VoLTE UE | P-CSCF  | SIP REGISTER       | con credenciales |
| B12 | P-CSCF   | I-CSCF  | SIP REGISTER       | |
| B13 | I-CSCF   | HSS     | UAR                | |
| B14 | HSS      | I-CSCF  | UAA                | |
| B15 | I-CSCF   | S-CSCF  | SIP REGISTER       | |
| B16 | S-CSCF   | HSS     | SAR                | Server Assignment Request (Cx) |
| B17 | HSS      | S-CSCF  | SAA                | descarga perfil de usuario |
| B18 | S-CSCF   | I-CSCF  | 200 OK             | |
| B19 | I-CSCF   | P-CSCF  | 200 OK             | |
| B20 | P-CSCF   | VoLTE UE| 200 OK             | UE queda registrado |

### B.3 — Rx (política de medios, dashed en Figure 3)
| #    | Origen | Destino | Mensaje | Notas |
|------|--------|---------|---------|-------|
| B-R1 | P-CSCF | PCRF    | AAR     | Authorization/Auth Request (Rx) |
| B-R2 | PCRF   | P-CSCF  | AAA     | Authorization/Auth Answer (Rx) |

### B.4 — Registro de tercera parte (TAS) + Sh
| #   | Origen | Destino | Mensaje      | Notas |
|-----|--------|---------|--------------|-------|
| B21 | S-CSCF | TAS     | SIP REGISTER | third-party registration (iFC) |
| B22 | TAS    | HSS     | UDR          | User Data Request (Sh) — **verificar endpoint** |
| B23 | HSS    | TAS     | UDA          | User Data Answer (Sh) → TAS guarda datos del usuario |
| B24 | TAS    | S-CSCF  | 200 OK       | |

### B.5 — SUBSCRIBE / NOTIFY al estado de registro (reg event package)
| #   | Origen   | Destino | Mensaje              | Notas |
|-----|----------|---------|----------------------|-------|
| B25 | VoLTE UE | P-CSCF  | SIP SUBSCRIBE        | reg event |
| B26 | P-CSCF   | S-CSCF  | SIP SUBSCRIBE        | |
| B27 | S-CSCF   | P-CSCF  | 200 OK (Subscribe)   | |
| B28 | P-CSCF   | VoLTE UE| 200 OK (Subscribe)   | |
| B29 | S-CSCF   | P-CSCF  | SIP NOTIFY           | estado = registrado |
| B30 | P-CSCF   | VoLTE UE| SIP NOTIFY           | |
| B31 | VoLTE UE | P-CSCF  | 200 OK (Notify)      | |
| B32 | P-CSCF   | S-CSCF  | 200 OK (Notify)      | **último mensaje del flujo** |

> **Último mensaje:** el "último mensaje de señalización" que disparan las reglas del
> enunciado (TAS reporta UEs registrados; S-CSCF emite `{"message":"fin"}`) depende de cuál
> sea efectivamente el último en la secuencia definitiva. Definir esto con precisión:
> - **TAS:** su último **envío** es B24 (200 OK al S-CSCF) → ahí adjunta los datos de los
>   UE registrados.
> - **S-CSCF:** tras notificar la **recepción** de su último mensaje recibido (candidato:
>   B32, 200 OK Notify) emite la notificación extra `{"message":"fin"}`.

---

## Puntos a reconciliar contra GSMA V1.1 (cierre de Fase 1)

1. **Bloque Authentication/Security (A05–A08):** cantidad y sentido exactos de mensajes.
2. **UDR/UDA (B22/B23):** confirmar que es **TAS ⇄ HSS** por Sh (y no S-CSCF ⇄ HSS).
3. **AAR/AAA (Rx):** confirmar si entran en la corrida y en qué punto exacto.
4. **SUBSCRIBE/NOTIFY:** confirmar el camino (¿pasa por I-CSCF o va P-CSCF ⇄ S-CSCF
   directo?) y si hay uno o más NOTIFY.
5. **Cuál es el último mensaje** de cada nodo (afecta a TAS y S-CSCF).

## Tabla objetivo de validación (Recibe / Emite por nodo, por flujo de 1 UE)

La secuencia definitiva **debe** producir exactamente estas cuentas:

| Nodo     | Recibe | Emite |   | Nodo   | Recibe | Emite |
|----------|:------:|:-----:|---|--------|:------:|:-----:|
| VoLTE UE |   7    |   8   |   | HSS    |   7    |   6   |
| eNB      |   5    |   5   |   | P-CSCF |   11   |  10   |
| MME      |   8    |   6   |   | I-CSCF |   6    |   6   |
| SGW      |   3    |   3   |   | S-CSCF |   11   |  11   |
| PGW      |   2    |   2   |   | TAS    |   4    |   4   |
| PCRF     |   2    |   2   |   |        |        |       |

> Cuando cierren la secuencia, **tachen mensaje por mensaje** y verifiquen que cada nodo
> reciba/emita exactamente esos números. Si no cuadra, falta o sobra un mensaje (lo más
> probable: el bloque de autenticación o el de subscribe/notify).

---

## Ejecución con 2 VoLTE UE

El examinador asigna identidad a **dos** UE. Decisión de equipo (recomendada): **correr el
flujo completo de forma secuencial** — primero UE1 hace Attach + Registration de punta a
punta, y al terminar, UE2. Así:

- Los nodos compartidos (eNB, MME, SGW, PGW, PCRF, HSS, P-CSCF, I-CSCF, S-CSCF, TAS)
  procesan **dos veces** la secuencia (una por UE) → su tráfico real es el doble de la
  tabla. Deben llevar **estado por UE** (correlación por `session` / `ue`).
- El **TAS** termina con **2 UE registrados** y los reporta a ambos en su última
  notificación de envío.
- Alternativa (más difícil): correr ambos UE en paralelo/intercalado. Solo si el examinador
  lo exige. Requiere manejo concurrente de sesiones más cuidadoso.
