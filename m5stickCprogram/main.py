from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
from m5mqtt import M5mqtt
import json
import time
import unit
from secrets import WIFI

setScreenColor(0x111111)
env20 = unit.get(unit.ENV2, unit.PORTA)

wifiCfg.doConnect(WIFI["ap"], WIFI["pw"])

label0 = M5TextBox(21, 68, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label1 = M5TextBox(21, 95, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label2 = M5TextBox(21, 125, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)

data = None
counter = None


from numbers import Number


m5mqtt = M5mqtt('id-au15572-1234', 'itwot.cs.au.dk', 1883, '', '', 300)
m5mqtt.set_last_will(str('au602716/M5SC0/status'),str('disconnected'))
m5mqtt.start()
m5mqtt.publish(str('au602716/M5SC0/status'),str('connected'))
counter = 0
data = counter
while True:
  label0.setText(str("%.1f"%float((env20.temperature))))
  label1.setText(str("%.1f"%float((env20.humidity))))
  label2.setText(str("%.0f"%float((env20.pressure))))
  m5mqtt.publish(str('au602716/M5SC0/measurements/json'),str((json.dumps({"temp":env20.temperature,"hum":env20.humidity,"pres":env20.pressure}))))
  counter = (counter if isinstance(counter, Number) else 0) + 1
  wait(60)
  data = counter
  wait_ms(2)