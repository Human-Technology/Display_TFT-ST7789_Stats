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


def serviceJellyfin():
    """
        Funcion retorno del estatus de Jellyfin

        :return:
            d1 -> str -> Cadena de texto con el estatus de Jellfin (Activo o desactivado)
    """
    command = "systemctl is-active jellyfin.service"
    d1 = str(subprocess.check_output(command, shell=True), 'utf-8')
    return d1


def serviceApache():
    """
        Funcion retorno del estatus de Apache

        :return:
            d1 -> str -> Cadena de texto con el estatus de Apache (Activo o desactivado)
    """
    command = "systemctl is-active apache2"
    d1 = str(subprocess.check_output(command, shell=True), 'utf-8')
    return d1

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

#Bucle Infinito
while True:
    draw.rectangle((0, 0, display.height, display.width), fill=(0, 0, 0))  # limpiar la pantalla

    #Textos en coordenadas
    draw.text((10, 10), "IP: " + ip(), font=font, fill=(255, 255, 255))
    draw.text((10, 35), "Jellyfin: " + serviceJellyfin(), font=font, fill=(255,255,255))
    draw.text((10, 60), "Apache: " + serviceApache(), font=font, fill=(255,255,255))
    draw.text((10, 75), "-----------------------", font=font, fill=(255, 255, 255))
    draw.text((10, 90), cpu(), font=font, fill=(255, 255, 255))
    draw.text((10, 115), mem(), font=font, fill=(255, 255, 255))
    draw.text((10, 140), disk(), font=font, fill=(255, 255, 255))

    # Muestra contendio en el display
    display.image(image)

    #Tiempo de espera en segundos
    time.sleep(1)