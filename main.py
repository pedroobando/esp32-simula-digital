from machine import UART, Pin, SoftI2C, TouchPad, reset
from i2c_lcd import I2cLcd
import uasyncio as asyncio
import urandom
import time


def configure_LED(gpio_led):
	led_pin32 = Pin(gpio_led, Pin.OUT)
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

def configure_uart(tx_pin, rx_pin, baudrate=9600):
	uart = UART(1, baudrate=baudrate, tx=tx_pin, rx=rx_pin)
	return uart

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

async def read_and_send(uart,lcd,led_write, gpio_touch,min_range,max_range,sleep_range):
	touch_pin = TouchPad(Pin(gpio_touch))
	lcdprint(lcd, 0, 0, 'TARA:', True)
	while True:
		data = random_number(min_range,max_range)
		lcdprint_right(lcd, 0, data)
		ledReady(led_write,1)
		uart.write(str(data) + '\n')
		print(data)
		await asyncio.sleep(0.5)
		ledReady(led_write,0)
		await reset_app(lcd,touch_pin)		
		await asyncio.sleep(sleep_range)
		

async def main():
	GPIO32_LED = 32
	GPIO33_LED = 33


	TX_GPIO17 = 17
	RX_GPIO16 = 16

	TOUCH_GPIO4 = 4
	MIN_RANGE = 8000
	MAX_RANGE = 15000
	SLEEP_RANGE = 2
	
	pl_ready = configure_LED(GPIO32_LED)
	pl_writedata = configure_LED(GPIO33_LED)
	ledReady(pl_ready,0)
	ledReady(pl_writedata,0)
	lcd = configure_LCD_16x2()
	uart = configure_uart(tx_pin=TX_GPIO17, rx_pin=RX_GPIO16)  # Ajusta los pines TX y RX según tu configuración
	time.sleep(0.5)
	# await testing_display(lcd)
	lcdprint(lcd,0,0,"Ready...",True)
	# lcdprint(lcd,1,0,"ESP32 Devkitc_V4")
	time.sleep(0.5)
	ledReady(pl_ready,1)
	await read_and_send(uart, lcd, pl_writedata, TOUCH_GPIO4,min_range=MIN_RANGE,max_range=MAX_RANGE,sleep_range=SLEEP_RANGE)

# Ejecuta la función principal
asyncio.run(main())
