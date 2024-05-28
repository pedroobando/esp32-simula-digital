# Cliente ESP32 - LCD 16x2

Una sencilla aplicacion que crea un numero random cada 2.5 segundos segun el intervalo indicado, mostrandolo por el display LCD 16x02 y envia el mismo por el puerto RS232 a TTL conectado al ESP32, cuenta con un boton touch de reset.

Microcontrolador: _ESP32 Devkitc_v4_

Programa escrito en micropython

## Conexion Pines de LCD 16x2 HD44780 a ESP32

```
  VCC => 5V
  SDA => GPIO21
  SLC => GPIO22
  GND => GND
```

## Conexion Pines de RS232 a ESP32

```
  VCC => 3V
  RXD => GPIO16
  TXD => GPIO17
  GND => GND
```

## Conexion Pines del LED a ESP32

```
  ANODO  => GPIO33 (Dato enviado)
  ANODO  => GPIO32 (Encendido)
  CATODO => GND
```

## Conexion Pines TOUCH a ESP32

```
  RESET  => GPIO4
```

## Variables

```
	TOUCH_GPIO4 = GPIO del Sensor Tactil
	MIN_RANGE = Rango minimo del numero
	MAX_RANGE = Rango maximo del numero
	SLEEP_RANGE = tiempo de retardo de semilla.
```
