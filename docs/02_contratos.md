# Contratos de datos (envelope, notificación, timing)

Estos formatos los usan **todos** los nodos por igual. Viven en `common/` como código
compartido para que nadie los implemente distinto. **No cambiar sin avisar al equipo.**

---

## 1. Envelope de mensaje entre nodos (UDP, JSON)

Cada mensaje de señalización entre nodos viaja como un datagrama UDP con este JSON:

```json
{
  "msg":     "Create Session Request",
  "src":     "MME",
  "src_ip":  "192.168.1.21",
  "dst":     "SGW",
  "dst_ip":  "192.168.1.22",
  "ue":      "tel:+59899111111",
  "session": "ue1-attach",
  "params":  { "IMS-APN": "ims", "QCI": 5, "ARP": 1, "APN-AMBR": "100M" },
  "ts":      "2026-06-11T20:00:00.123"
}
```

| Campo     | Tipo   | Significado |
|-----------|--------|-------------|
| `msg`     | string | Nombre **exacto** del mensaje según `01_secuencia_mensajes.md` (ej. `"SIP REGISTER"`). |
| `src`     | string | Nombre del nodo emisor (ej. `"MME"`). |
| `src_ip`  | string | IP del nodo emisor. |
| `dst`     | string | Nombre del nodo destino. |
| `dst_ip`  | string | IP del nodo destino. |
| `ue`      | string | IMS Public User Identity del UE al que pertenece el flujo (`tel:+598...`). |
| `session` | string | Correlador del flujo/transacción (ej. `"ue1-attach"`, `"ue1-imsreg"`). |
| `params`  | objeto | Parámetros propios del mensaje (los de la tabla de secuencia). Libre por mensaje. |
| `ts`      | string | Marca de tiempo ISO-8601 del envío (opcional, útil para debug). |

**Regla de oro:** un nodo decide **qué enviar** mirando `msg` + `src` (de qué nodo vino) +
su propio estado. La tabla de `01_secuencia_mensajes.md` es la máquina de estados.

---

## 2. Notificación al PC del examinador (UDP 55555, JSON)

El enunciado fija los **campos requeridos**; los **nombres de clave** los definimos
nosotros, pero **deben ser idénticos en todos los nodos**. Esquema acordado:

```json
{
  "hora":           "20:00:01.123",
  "nodo":           "MME",
  "ip":             "192.168.1.21",
  "apellido":       "Roure",
  "sentido":        "recibido",
  "mensaje":        "Attach req",
  "contraparte":    "eNB",
  "contraparte_ip": "192.168.1.11"
}
```

| Campo            | Requerido por consigna | Significado |
|------------------|------------------------|-------------|
| `hora`           | hora del nodo que notifica | hora local del nodo, formato `HH:MM:SS.mmm`. |
| `nodo`           | nombre del nodo que notifica | ej. `"MME"`. |
| `ip`             | dirección IP del nodo que notifica | IP propia. |
| `apellido`       | apellido del alumno que opera el nodo | ej. `"Roure"`. |
| `sentido`        | recibido o será enviado | `"recibido"` o `"a_enviar"`. |
| `mensaje`        | nombre del mensaje de señalización | recibido o a punto de enviar. |
| `contraparte`    | nombre del nodo origen o destino | **origen** si `recibido`; **destino** si `a_enviar`. |
| `contraparte_ip` | IP del nodo origen o destino | IP de la contraparte. |

### 2.1 — Caso especial TAS (último envío)
En la notificación de **envío** de su **último** mensaje, el TAS agrega los datos de cada
UE registrado:

```json
{
  "hora": "20:01:30.000", "nodo": "TAS", "ip": "192.168.1.40", "apellido": "Silva",
  "sentido": "a_enviar", "mensaje": "200 OK", "contraparte": "S-CSCF",
  "contraparte_ip": "192.168.1.33",
  "ues_registrados": [
    { "ims_public_id": "tel:+59899111111", "ip": "10.0.0.11",
      "datos_hss": { "msisdn": "59899111111", "nombre": "UE1", "perfil": "VoLTE" } },
    { "ims_public_id": "tel:+59899222222", "ip": "10.0.0.12",
      "datos_hss": { "msisdn": "59899222222", "nombre": "UE2", "perfil": "VoLTE" } }
  ]
}
```

### 2.2 — Caso especial S-CSCF (fin)
Tras notificar la **recepción** de su último mensaje, el S-CSCF envía **una notificación
adicional** con exactamente:

```json
{ "message": "fin" }
```

---

## 3. Regla de timing (la "W" del diagrama = 1 segundo)

El enunciado describe el caso encadenado "recibo X → envío Y". La regla **general** y
uniforme que cubre todos los casos:

- **Al recibir** un mensaje X (de A): esperar **1 s** y enviar notificación
  `sentido="recibido"`, `mensaje=X`, `contraparte=A`.
- **Antes de enviar** un mensaje Y (a B): esperar **1 s más** (desde la notificación
  anterior) y enviar notificación `sentido="a_enviar"`, `mensaje=Y`, `contraparte=B`;
  **recién entonces** mandar Y al nodo B.

Pseudocódigo del handler de cada nodo:

```
al_recibir(X, desde=A):
    esperar(1s)
    notificar(sentido="recibido", mensaje=X, contraparte=A)
    (Y, B) = decidir_siguiente(X, A, estado)     # según tabla de secuencia
    si hay Y:
        esperar(1s)
        notificar(sentido="a_enviar", mensaje=Y, contraparte=B)
        enviar(Y, a=B)
```

**Casos borde (confirmar con el examinador):**
- **Mensaje que origina un nodo sin haber recibido nada** (ej. el primer
  `RRC Connection Request` del UE): no hay notificación `recibido`; solo se emite la de
  `a_enviar` 1 s antes de mandarlo. *Verificar si el examinador lo espera así.*
- **Mensaje terminal** (un nodo recibe algo y no reenvía nada, ej. el UE recibe el último
  `200 OK`/`NOTIFY`): solo la notificación `recibido`.
- **Un recibido que dispara varios envíos** (fan-out): emitir una notificación `a_enviar`
  por cada mensaje saliente, cada una 1 s antes de su envío.

> Implicancia de rendimiento: con 1 s + 1 s por salto y ~64 mensajes por UE, una corrida
> dura **varios minutos**. Es esperado. No "optimizar" sacando los sleeps.
