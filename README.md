# Display_TFT-ST7789_Stats
Script de visualización de estadísticas Dsiplay TFT-ST7789 para Raspberry Pi

El script está preconfigurado para una pantalla TFT-ST7789 de 170x320. Muestra las estadisticas de la Raspberry Pi.

## Hardware Requerido
- Raspberry Pi
- Cables jumper hembra-macho
- Pantalla LCD TFT-ST778 de 170x320
- Protoboard (placa de pruebas)

## 1. Conexión
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

## 2. Actualización del Sistema
Primero antes de todo hay que actualizar nuestro sistema Linux con el siguiente comando:
```bash
sudo apt update && sudo apt upgrade -y
```
Para una actualización completa podemos ejecutar también el comando:
```bash
sudo apt full-upgrade
```

## 3. Instalación de PIP
Con el sistema actualización debemos instalar PIP, es un sistema de gestión de paquetes utilizado para instalar paquetes escritos en Python, para instalarlo ejecutamos el comando:
```bash
sudo apt install python3-pip
```

## 4. Instalación de Paquetes Necesarios
Primero hay que instalar Git para poder clonar este repositorio y obtener el programa y los archivos necesarios para ello ejecutamos el comando:
```bash
sudo apt install git
```
Ahora debemos eliminar un archivo que nos provocara un error al utilizar pip, para ello ejecutamos el comando:
```bash
sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED
```

Si no tienes problemas con utilizar pip, puedes saltarte este paso, de igual manera si no cuentas con este archivo en la carpeta especificada anteriormente.

Ahora podemos instalar los paquetes que requiere nuestro programa con los siguientes comandos:
```bash
pip install Adafruit-Blinka

pip install pillow

pip install adafruit-circuitpython-rgb-display
```

## 5. Descargar Recursos
Ahora puedes descargar los recursos de este repositorio con el siguiente comando:
```bash
git clone https://github.com/Human-Technology/Display_TFT-ST7789_Stats.git
```
Este comando te dejará una carpeta con el contenido de este repositorio. Para movernos a esta carpeta ejecutamos el comando:
```bash
cd Display_TFT-ST7789_Stats/
```
## 6. Iniciar Programa al encender Raspberry
Para esto necesitamos la ruta absoluta de nuestro programa que se encuentra en el directorio Display_TFT-ST7789_Stats, para ello podemos usar el comando:
```bash
pwd
```
Esto nos retornara algo como lo siguiente:
```bash
/home/human/Display_TFT-ST7789_Stats
```
en mi caso "human" es mi nombre de usuario, una vez que ya tenemos esta ruta podemos agregarla a crontab, para ello ejecutamos:
```bash
crontab -e
```
en la parte de hasta abajo, colocamos lo siguiente:
```bash
@reboot cd DIR/Display_TFT-ST7789_Stats && python dataDisplay.py &
```
en este caso "DIR", es la ruta absoluta obtenida anteriormente con el comando pwd, para mi queda de la siguiente manera:
```bash
@reboot cd /home/human/Display_TFT-ST7789_Stats && python dataDisplay.py &
```
Por último guardamos cambios con ctrl+o y cerramos el documento con ctrl+x
---------------------------------------------
Con esto al apagar y encender la raspberry pi o reiniciarla, el progrmama se ejecutara y mostrara los datos por pantalla.
