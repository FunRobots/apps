from luma.core.serial import spi
from luma.core.render import canvas
from luma.lcd.device import st7735

serial = spi(port=0, device=0, gpio_DC=23, gpio_RST=24)
device = st7735(serial)

with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((30, 40), "Hello World", fill="red"