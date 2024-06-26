# Created by: José Sánchez - Human Technology

import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import time
import subprocess


def cpu():
    """
        Funcion retorno de datos sobre la CPU

        :return
            d1 -> str -> Carga Promedio del sistema
            d2 -> str -> Temperatura de la CPU
    """
    command = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
    d1 = str(subprocess.check_output(command, shell=True), 'utf-8')

    command = "vcgencmd measure_temp | cut -f 2 -d '='"
    d2 = str(subprocess.check_output(command, shell=True), 'utf-8')

    return d1 + "    " + d2

def mem():
    """
        Funcion retorno de datos sobre la Memoria RAM

        :return:
            d1 -> str -> Cadena de texto que mustra el uso en MB de la memoria RAM y el Porcentaje de uso
    """
    command = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB    %.2f%%\", $3,$2,$3*100/$2 }'"
    d1 = str(subprocess.check_output(command, shell=True), 'utf-8')
    return d1


def disk():
    """
        Funcion retorno de datos sobre el disco duro o almacenamiento.

        :return:
            d1 -> str -> Cadena de texto que muestra el uso en GB del almacenamiento y el porcentaje de uso
    """
    command = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB    %s\", $3,$2,$5}'"
    d1 = str(subprocess.check_output(command, shell=True), 'utf-8')
    return d1


def ip():
    """
        Funcion retorno de direccion IP

        :return:
            d1 -> str -> Cadena de texto que muestra la direccion IP
    """

    command = "hostname -I | cut -d\' \' -f1"
    d1 = str(subprocess.check_output(command, shell=True), 'utf-8')
    return d1


def service_status(service_name):
    try:
        command = f"systemctl is-active {service_name}"
        status = str(subprocess.check_output(command, shell=True), 'utf-8').strip()
        return status
    except subprocess.CalledProcessError:
        return None

def service_installed(service_name):
    try:
        command = f"systemctl list-units --full -all | grep -Fq {service_name}"
        subprocess.check_output(command, shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

#espera 60 segundos para asegurar de que el sistema se ha inicializado completamente
time.sleep(60)

# Configuración de pines
cs_pin = digitalio.DigitalInOut(board.CE0)  # Pin CS (Chip Select)
dc_pin = digitalio.DigitalInOut(board.D24)  # Pin DC (Data/Command)
reset_pin = digitalio.DigitalInOut(board.D25)  # Pin RESET

# Inicialización de la interfaz SPI
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Creación del objeto display
display = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=32000000,
    width=170,
    height=320,
    x_offset=35,
    y_offset=0,
    rotation=90  # Rotar la pantalla 90 grados
)

# Configurar la retroiluminación (BLK)
backlight = digitalio.DigitalInOut(board.D18)
backlight.direction = digitalio.Direction.OUTPUT
backlight.value = True  # Enciende la retroiluminación

# Creación de objeto de imagen
if display.rotation in (90, 270):
    # Si la pantalla está rotada 90 o 270 grados, la altura y el ancho se intercambian
    image = Image.new("RGB", (display.height, display.width))
else:
    image = Image.new("RGB", (display.width, display.height))

#Creacion de objeto de dibujo
draw = ImageDraw.Draw(image)

# Crea un objeto de fuente
font_path = "minecraft_font.ttf" #Path de la fuenta
font_size = 16                  #Tamaño del texto
font = ImageFont.truetype(font_path, font_size) #Objeto de la fuente

#Verifica si los servicion estan instalados
jellyfin_installed = service_installed("jellyfin.service")
apache_installed = service_installed("apache2")

# Bucle Infinito
while True:
    try:
        draw.rectangle((0, 0, display.height, display.width), fill=(0, 0, 0))  # limpiar la pantalla

        draw.text((10, 10), "IP: " + ip(), font=font, fill=(255, 255, 255)) #muestra la direccion IP

        #Verifica si Jellyfin esta instalado
        if jellyfin_installed:
            #Si lo esta entonces verifica si esta iniciado
            jellyfin_status = service_status("jellyfin.service")
            draw.text((10, 35), "Jellyfin: " + jellyfin_status, font=font, fill=(255, 255, 255))
        else:
            #Si no lo esta muestra mensaje no instalado
            draw.text((10, 35), "Jellyfin no instalado", font=font, fill=(255, 255, 255))

        #verifica si el servicio de apache esta instalado
        if apache_installed:
            #si lo esta entonces verifica si esta iniciado
            apache_status = service_status("apache2")
            draw.text((10, 60), "Apache: " + apache_status, font=font, fill=(255, 255, 255))
        else:
            #si no lo esta muestra mensaje de no instalado
            draw.text((10, 60), "Apache no instalado", font=font, fill=(255, 255, 255))

        draw.text((10, 75), "-----------------------", font=font, fill=(255, 255, 255))
        draw.text((10, 90), cpu(), font=font, fill=(255, 255, 255)) #Informacion de la CPU
        draw.text((10, 115), mem(), font=font, fill=(255, 255, 255)) #Informacion de la memoria
        draw.text((10, 140), disk(), font=font, fill=(255, 255, 255)) #Informacion del disco

        display.image(image)
        time.sleep(1)
    except subprocess.CalledProcessError:
        draw.rectangle((0, 0, display.height, display.width), fill=(0, 0, 0))  # limpiar la pantalla
        draw.text((10, 10), "Error en ejecución", font=font, fill=(255, 0, 0))
        display.image(image)
        time.sleep(1)
