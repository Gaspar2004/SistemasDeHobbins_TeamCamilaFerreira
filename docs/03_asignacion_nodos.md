# Asignación de nodos y fichas técnicas

## Propuesta de reparto (6 integrantes × 2 nodos = 12 instancias)

Hay **12 instancias** porque `VoLTE UE` se cuenta **dos veces** (UE1 y UE2). La propuesta
**balancea la carga** (suma de Recibe+Emite) emparejando un nodo pesado con uno liviano.
**Es ajustable**: reordenen a gusto, pero traten de mantener el balance.

| Par | Nodos del integrante      | Carga (R+E)      | Total | Integrante (a completar) |
|:---:|---------------------------|------------------|:-----:|--------------------------|
| A   | **S-CSCF** + **PCRF**     | 22 + 4           | 26    | _________________ |
| B   | **P-CSCF** + **PGW**      | 21 + 4           | 25    | _________________ |
| C   | **HSS** + **I-CSCF**      | 13 + 12          | 25    | _________________ |
| D   | **MME** + **eNB**         | 14 + 10          | 24    | _________________ |
| E   | **VoLTE UE 2** + **TAS**  | 15 + 8           | 23    | _________________ |
| F   | **VoLTE UE 1** + **SGW**  | 15 + 6           | 21    | _________________ |

Criterios usados:
- **Balance:** todos entre 21 y 26 de carga.
- **Coherencia:** D agrupa el enlace de acceso EPC (eNB↔MME, interfaz S1). C agrupa HSS con
  I-CSCF (se hablan por Cx: UAR/UAA). B agrupa el lado de políticas/bearer.
- Los **dos operadores de UE** (pares E y F) son quienes figuran con su `apellido` en las
  notificaciones de cada UE — coordinen quién es UE1 y quién UE2.

> Recordatorio: cada integrante pone **su propio apellido** en las notificaciones de los
> dos nodos que opera. El campo `apellido` se configura por nodo (ver `config/nodes`).

---

## Fichas técnicas por nodo

Para cada nodo: con qué vecinos habla, qué estado guarda y sus mensajes clave. Los números
de mensaje (`A##`, `B##`) remiten a `01_secuencia_mensajes.md`.

### VoLTE UE (UE1 / UE2) — R7 / E8
- **Vecinos:** eNB (radio), P-CSCF (SIP).
- **Estado:** su IMS Public User Identity (`tel:+598...`), su IP asignada, estado de attach
  y de registro.
- **Origina:** A01 (RRC Conn Request), B01/B11 (REGISTER), B25 (SUBSCRIBE).
- **Termina** recibiendo 200 OK (B20) y NOTIFY (B30). Es un **extremo** del flujo.

### eNB — R5 / E5
- **Vecinos:** VoLTE UE (radio), MME (S1-MME).
- **Estado:** prácticamente *stateless* (relay radio↔NAS); correlación por UE.
- **Clave:** traduce entre mensajes RRC (lado UE) y NAS/S1 (lado MME). A02, A04, A17→A18,
  A20, A22.

### MME — R8 / E6
- **Vecinos:** eNB (S1), HSS (S6a), SGW (S11).
- **Estado:** contexto EPS por UE (sesión, bearer).
- **Clave:** Auth/Security con HSS+UE (A05–A08), Update Location (A09/A10), Create Session
  (A11), E-RAB Setup (A17), Modify Bearer (A23).

### SGW — R3 / E3
- **Vecinos:** MME (S11), PGW (S5).
- **Estado:** sesión/bearer por UE.
- **Clave:** relay de Create Session (A11→A12, A15→A16) y Modify Bearer (A23→...).

### PGW — R2 / E2
- **Vecinos:** SGW (S5), PCRF (Gx).
- **Estado:** asigna **IP@** al UE; sesión.
- **Clave:** Create Session (A12), dispara CCR→PCRF (A13), responde A15 con la IP.

### PCRF — R2 / E2
- **Vecinos:** PGW (Gx), P-CSCF (Rx).
- **Estado:** reglas de política (QoS).
- **Clave:** CCR/CCA (A13/A14) en Gx; AAR/AAA (B-R1/B-R2) en Rx.

### HSS — R7 / E6
- **Vecinos:** MME (S6a), I-CSCF y S-CSCF (Cx), TAS (Sh).
- **Estado:** **base de datos de suscriptores** (por IMSI/MSISDN/IMS Public Id). Guarda los
  "datos del usuario" que el TAS reporta al final. **Definir un perfil simulado por UE.**
- **Clave:** Auth Info (A05/A06), Update Location (A09/A10), UAR/UAA (B03/B04, B13/B14),
  MAR/MAA (B06/B07), SAR/SAA (B16/B17), UDR/UDA (B22/B23).

### P-CSCF — R11 / E10  (nodo más cargado)
- **Vecinos:** VoLTE UE (Mw/SIP), I-CSCF (Mw), S-CSCF (Mw para SUBSCRIBE/NOTIFY), PCRF (Rx).
- **Estado:** asociación UE↔S-CSCF (vía el path), suscripción.
- **Clave:** primer punto de contacto SIP del UE; proxea REGISTER (B01/B02, B11/B12), 401
  y 200 OK de vuelta al UE, AAR/AAA (Rx), SUBSCRIBE/NOTIFY (B25–B32).

### I-CSCF — R6 / E6
- **Vecinos:** P-CSCF (Mw), HSS (Cx), S-CSCF (Mw).
- **Estado:** poco; consulta HSS para asignar S-CSCF.
- **Clave:** UAR/UAA con HSS (B03/B04, B13/B14), reenvía REGISTER al S-CSCF, devuelve
  401/200 OK al P-CSCF.

### S-CSCF — R11 / E11  (nodo más cargado)
- **Vecinos:** I-CSCF (Mw), HSS (Cx), TAS (ISC), P-CSCF (Mw para SUBSCRIBE/NOTIFY).
- **Estado:** **registro del usuario** (binding), iFC.
- **Clave:** MAR/MAA y SAR/SAA con HSS, emite 401 (B08) y 200 OK (B18), **third-party
  REGISTER al TAS** (B21), maneja SUBSCRIBE/NOTIFY (B26/B27/B29/B32).
- **Regla final:** tras notificar la **recepción** de su último mensaje, manda
  `{"message":"fin"}` al examinador.

### TAS — R4 / E4
- **Vecinos:** S-CSCF (ISC), HSS (Sh).
- **Estado:** **lista de UE registrados** con su IMS Public Id, IP y datos del HSS.
- **Clave:** recibe third-party REGISTER (B21), descarga datos vía UDR/UDA (B22/B23),
  responde 200 OK (B24).
- **Regla final:** en la notificación de **envío** de su último mensaje adjunta los datos de
  todos los UE registrados (ver `02_contratos.md` §2.1).

---

## Datos simulados a acordar antes del examen
- **Perfil de cada UE en el HSS** (MSISDN, nombre, perfil VoLTE, lo que el TAS deba reportar).
- **IP@ que el PGW asigna a cada UE** (puede ser fija por UE para simplificar).
- **Credenciales/claves de autenticación** simuladas (pueden ser dummy: el 401 lleva un
  `nonce` y el segundo REGISTER lo "resuelve" sin criptografía real).
