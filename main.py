from machine import  Pin, SoftI2C, TouchPad, reset
from i2c_lcd import I2cLcd
import uasyncio as asyncio
import urandom
import time


def configure_LED():
	GPIO32_LED = 32
	led_pin32 = Pin(GPIO32_LED, Pin.OUT)
	return led_pin32

def configure_LCD_16x2():
	# Parametros del LCD 16x2
	I2C_ADDR = 0X27
	TOTAL_ROWS = 2
	TOTAL_COLS = 16

	SCL_GPIO_22 = Pin(22)
	SDA_GPIO_21 = Pin(21)
	FREQ = 10000

	i2c = SoftI2C(scl=SCL_GPIO_22, sda=SDA_GPIO_21, freq=FREQ)
	lcd = I2cLcd(i2c, I2C_ADDR, TOTAL_ROWS, TOTAL_COLS)
	# lcd.backlight_off()
	lcd.backlight_on()
	lcd.clear()
	return lcd

def ledReady(led_pin, activo):
	led_pin.value(activo)


def lcdprint(lcd, line, col, message, isclear=False):
	if(isclear):
		lcd.clear()
	lcd.move_to(col,line)
	lcd.putstr(message)

def lcdprint_right(lcd, row, datanumber):
	number_str = '  '+str(datanumber)
	spaces = 16 - len(number_str)
	lcdprint(lcd, row, spaces, number_str)

async def reset_app(lcd, touch_pin, threshold=300):
	touch_value = touch_pin.read()
	if touch_value < threshold:
		lcdprint(lcd, line=0, col=1,message="Resettig...",isclear=True)
		await asyncio.sleep(.5)  # Añade un pequeño retraso antes de resetear
		reset()

async def testing_display(lcd):
	for i in [0,1,2,3,4,5,6,7,8,9]:
		data = str(i)*16
		print(data)
		lcdprint(lcd,0,0,data)
		lcdprint(lcd,1,0,data)
		await asyncio.sleep(.2)

def random_number(min_range,max_range):
	return urandom.randint(min_range, max_range)

async def read_and_send(lcd, gpio_touch,min_range,max_range,sleep_range):
	touch_pin = TouchPad(Pin(gpio_touch))
	lcdprint(lcd, 0, 0, 'TARA:', True)
	while True:
		data = random_number(min_range,max_range)
		lcdprint_right(lcd,0, data)
		print(data)
		await reset_app(lcd,touch_pin)		
		await asyncio.sleep(sleep_range)


# async def main():
async def main():

	TOUCH_GPIO4 = 4
	MIN_RANGE = 8000
	MAX_RANGE = 15000
	SLEEP_RANGE = 2.5
	
	pinled = configure_LED()
	ledReady(pinled,0)
	lcd = configure_LCD_16x2()
	time.sleep(0.5)
	# await testing_display(lcd)
	lcdprint(lcd,0,0,"Ready...",True)
	# lcdprint(lcd,1,0,"ESP32 Devkitc_V4")
	time.sleep(0.5)
	ledReady(pinled,1)
	await read_and_send(lcd, TOUCH_GPIO4,min_range=MIN_RANGE,max_range=MAX_RANGE,sleep_range=SLEEP_RANGE)

# Ejecuta la función principal
asyncio.run(main())
