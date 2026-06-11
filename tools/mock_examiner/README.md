# mock_examiner

Examinador **de prueba**: simula el PC del examinador escuchando en **UDP 55555** e
imprimiendo las notificaciones JSON que mandan los nodos. Para probar localmente sin
depender del PC real.

## Correr
```
python tools/mock_examiner/mock_examiner.py
```
Escucha en `0.0.0.0:55555` (recibe desde otras laptops de la LAN). Loguea en
`notificaciones.log`. Resalta los casos especiales: `{"message":"fin"}` del S-CSCF y la
lista `ues_registrados` del TAS.

## Probar que llega una notificación (desde otra terminal)
```
python -c "import socket,json; socket.socket(2,2).sendto(json.dumps({'nodo':'TEST','mensaje':'hola'}).encode(),('127.0.0.1',55555))"
```

> En el examen real, apuntar `examiner.ip` de `config/nodes.json` a la IP del PC del
> examinador. Este mock solo es para desarrollo y ensayos.
