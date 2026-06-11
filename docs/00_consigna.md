# Consigna del examen (reconstruida del PDF `evaluacionFinal_planteo.pdf`)

> El PDF original no estaba en el repositorio al crear esta carpeta; este documento
> reproduce su contenido textual para tener el enunciado versionado junto al trabajo.
> **Si conseguís el PDF original, copialo a `docs/evaluacionFinal_planteo.pdf`.**

## Proyecto Final

La GSMA, en el capítulo **3.2.1** de su documento *"GSMA VoLTE Service Description and
Implementation Guide (V1.1)"*, describe el proceso de **"VoLTE UE Attachment and IMS
Registration"**.

Dicho proceso se compone de **dos subprocesos**:

- **VoLTE UE Attach** a la red móvil, que se describe en **3.2.1.3.1**, y
- **IMS Registration** a la red IMS, que se describe en **3.2.1.3.2**.

> La V2.0 también se puede utilizar, pero tiene problemas con las referencias
> automáticas dentro del documento.

Figuras de referencia del enunciado:
- **Figure 2:** Intra-PMN VoLTE deployment (arquitectura de nodos e interfaces).
- **Figure 3:** VoLTE UE Attachment and IMS Registration message sequence (diagrama de
  secuencia que hay que implementar).

## Control – al inicio

El examinador asignará al inicio un **IMS Public User Identity** a cada uno de **dos VoLTE
UE** en formato **MSISDN as Tel-URI** (e.g. `tel:+59899999999`).

## Control – durante el proceso

El PC del examinador llevará un **log de los mensajes** que viajan por la red. Para ello
el PC del examinador tendrá un **puerto UDP 55555** con un socket esperando recibir
notificaciones desde cada nodo de la red.

Cada nodo de la red deberá enviar **dos notificaciones al PC del examinador cada vez que
reciba un mensaje X** de señalización:

1. Información del **mensaje X recibido**, **1 segundo después** de recibir el mensaje X.
2. Información del **mensaje Y que enviará**, **1 segundo después de la primera
   notificación**, pero **antes** de enviar el mensaje Y de señalización a otro nodo.

Dichas notificaciones deberán estar **codificadas en JSON** y deberán **contener**:

- hora del nodo que notifica
- nombre del nodo que notifica
- dirección IP del nodo que notifica
- apellido del alumno que está operando el nodo
- indicación de si este mensaje que está siendo notificado es **recibido** o **será enviado**
- nombre del mensaje de señalización que se recibió (o del que está a punto de enviar)
- nombre del nodo origen (o del nodo destino)
- dirección IP del nodo origen (o del nodo destino)

(Diagrama del enunciado: Nodo A envía *Mensaje X* a Nodo B; Nodo B espera 1s y emite
*Notify "X" (recibido)*, espera 1s más y emite *Notify "Y" (a enviar)*, y recién entonces
envía *Mensaje Y*. Las "W" representan esperas de 1 segundo.)

## Control – al final

- El nodo **TAS** incluirá en la **notificación de envío** de su **último** mensaje de
  señalización la siguiente información de **cada VoLTE UE que tenga registrado**:
  - IMS Public User Identity del VoLTE UE
  - dirección IP del VoLTE UE
  - cualquier dato del usuario que tenga almacenado el HSS
- El nodo **S-CSCF**, luego de enviar la **notificación de recepción** del **último**
  mensaje de señalización, enviará una **notificación adicional** conteniendo únicamente
  `{"message": "fin"}`.

## Equipos

**Subgrupo 1: Team-C** (nuestro equipo)

- Abreu, Juan Lucas
- Birenbaum, Gaspar
- Ferreira, Camila
- Guasch, Felipe
- Roure, Santiago
- Silva, Nicolás

**Subgrupo 2: Team-M**

- Dellapiazza, Magalí
- Hobbins, Patrick
- Lasala, Martín
- Seré, Nicolás
- Tauber, Juan Francisco
- Vázquez, Juan Manuel

**Cada integrante (de cada grupo) deberá resolver dos nodos.**

## Nodos y cantidad de mensajes (Figure del enunciado)

La red tiene **12 instancias de nodo**: `VoLTE UE` aparece **dos veces** (UE1 y UE2) más
los 10 nodos de red. Las cantidades de mensajes por nodo (Recibe / Emite) son:

| Nodo       | Recibe | Emite | Total (R+E) |
|------------|:------:|:-----:|:-----------:|
| VoLTE UE   |   7    |   8   |     15      |
| eNB        |   5    |   5   |     10      |
| MME        |   8    |   6   |     14      |
| SGW        |   3    |   3   |      6      |
| PGW        |   2    |   2   |      4      |
| PCRF       |   2    |   2   |      4      |
| HSS        |   7    |   6   |     13      |
| P-CSCF     |   11   |  10   |     21      |
| I-CSCF     |   6    |   6   |     12      |
| S-CSCF     |   11   |  11   |     22      |
| TAS        |   4    |   4   |      8      |

El enunciado agrupa: **22 msgs** del lado red móvil (UE…PCRF) y **42 msgs** del lado IMS
(HSS…TAS). Estos números son **por flujo de un UE**; con dos UE el tráfico se duplica
sobre los nodos compartidos.
