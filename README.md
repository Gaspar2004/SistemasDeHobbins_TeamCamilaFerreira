# Proyecto Final VoLTE — Team-C

Simulación del proceso **VoLTE UE Attachment and IMS Registration** (GSMA VoLTE V1.1,
§3.2.1). Red de **12 nodos** en Python que intercambian señalización por **UDP** y notifican
al PC del examinador (**UDP 55555**, JSON). Cada integrante opera **2 nodos**.

## Empezá por acá

1. **Leé el plan:** [PLAN.md](PLAN.md) (o [PLAN.pdf](PLAN.pdf) para compartir).
2. **Enunciado:** [docs/00_consigna.md](docs/00_consigna.md).
3. **Tu nodo:** mirá [docs/03_asignacion_nodos.md](docs/03_asignacion_nodos.md) y el README
   de tu carpeta en [nodes/](nodes/).

## Documentos clave (contratos — no cambiar sin avisar)

| Archivo | Contenido |
|---------|-----------|
| [docs/00_consigna.md](docs/00_consigna.md) | Enunciado del examen reconstruido. |
| [docs/01_secuencia_mensajes.md](docs/01_secuencia_mensajes.md) | Secuencia de mensajes (Figure 3) — **BORRADOR a cerrar**. |
| [docs/02_contratos.md](docs/02_contratos.md) | Envelope, JSON de notificación, regla de timing 1 s. |
| [docs/03_asignacion_nodos.md](docs/03_asignacion_nodos.md) | Reparto de nodos y fichas técnicas. |
| [common/README.md](common/README.md) | Especificación de la librería compartida. |

## Quick start

```powershell
pip install markdown pygments
copy config\nodes.example.json config\nodes.json   # editar IPs y apellidos
python tools\mock_examiner\mock_examiner.py        # examinador de prueba (UDP 55555)
```

Regenerar el PDF del plan tras editar `PLAN.md`:
```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
```

## Decisiones técnicas
**Python 3** · mensajes entre nodos por **UDP** · despliegue en **LAN** (una laptop por
persona; direcciones en `config/nodes.json`). Detalle en [PLAN.md](PLAN.md) §3.

## Estado
- [x] Estructura del repo + documentación de contexto + plan (este commit).
- [ ] Fase 1: librería `common/` + secuencia definitiva.
- [ ] Fase 2: implementación de los 12 nodos.
- [ ] Fases 3–5: integración, ensayo y examen.
