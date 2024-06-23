# Display_TFT-ST7789_Stats
Script de visualización de estadísticas Dsiplay TFT-ST7789 para Raspberry Pi

El script está preconfigurado para una pantalla TFT-ST7789 de 170x320. Muestra las estadisticas de la Raspberry Pi.

## Hardware Requerido
- Raspberry Pi
- Cables jumper hembra-macho
- Pantalla LCD TFT-ST778 de 170x320
- Protoboard (placa de pruebas)

## Conexión
| Nombre LCD | Nombre PI | Pin GPIO PI  |
| ---------- | --------- | ------------ |
| GND        | GND       | 6            |
| VCC        | 3.3V      | 1            |
| SCL        | SCLK      | 23           |
| SDA        | MOSI      | 19           |
| RES        | GPIO 25   | 22           |
| DC         | GPIO 24   | 18           |
| CS         | CE0       | 24           |
| BLK        | GPIO 18   | 12           |

## Pines GPIO de la Raspberry PI
![PINES-RASPBERRY](https://github.com/Human-Technology/Display_TFT-ST7789_Stats/assets/41929896/b3a341eb-2613-4900-aba3-47340694235b)

## Pines LCD Utilizada
![lcd](https://github.com/Human-Technology/Display_TFT-ST7789_Stats/assets/41929896/4eece4a2-8113-43d7-85a2-6e6bd0410dfe)

