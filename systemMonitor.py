'''
Show system status on a 2x16 LCD display
'''
import os
import status
import math
import serial
from time import sleep

def checkLcd(lcd, throw = True):
  if not len(lcd) == 2:
    if throw:
      raise RuntimeError('Invalid LCD character array')
    return False
  for l in lcd:
    if not len(l) == 16:
      if throw:
        raise RuntimeError('Invalid LCD character array')
      return False
  return True
  
def makeLcd():
  lcd = []
  lcd.append(['' for _ in range(16)])
  lcd.append(['' for _ in range(16)])
  checkLcd(lcd)
  return lcd
  
def writeLcdCol(txt):
  txt = str(txt)
  col = ''
  if len(txt) <= 16:
    col = txt
    for i in range(16-len(txt)):
      col += ' '
  else:
    col = txt[:16]
  return col
  
def writeLcd(lcd, top = '', bottom = ''):
  lcd[0] = writeLcdCol(top)
  lcd[1] = writeLcdCol(bottom)
  return lcd
  
def removeCOutLine():
  # CURSOR_UP_ONE = '\x1b[1A'
  # ERASE_LINE = '\x1b[2K'
  # print(CURSOR_UP_ONE + ERASE_LINE)
  os.system('cls')
  
def printLcd(lcd):
  removeCOutLine()
  print()
  for row in range(4):
    prnt = ' #'
    if row == 1 or row == 2:
      for c in lcd[row-1]:
        prnt += c
    else:
      for i in range(16):
        prnt += '#'
    prnt += '#'
    print( prnt)
  print()
    
def updateLcd(ser, lcd, timeout=0):
  if not ser:
    printLcd(lcd)
    return
  try:
    out = ''
    for col in range(2):
      for c in lcd[col]:
        out += c
    ser.write(out.encode())
    sleep(timeout)
  except:
    print("Exception sending data over serial connection")
    pass
    
def main(port=3):
  periode_s = 3
  state = 0
  disk_state = 0
  
  try:
    ser = serial.Serial( 'COM'+str(int(port)), 9600, writeTimeout=1000)
    print('Opening '+str(ser.name))
    sleep(2)
    print(str(ser.readline()))
  except:
    print('Exception: No serial port opened')
    ser = None
  
  lcd = makeLcd()
  
  while True:
    if state == 0:
      lcd = writeLcd(lcd, status.hostName(), status.now())
      sleep(periode_s)
      state += 1
    elif state == 1:
      if disk_state <= 0:
        drvs = status.parseDrives()
      d = drvs[disk_state]
      lcd = writeLcd(lcd, d["Letter"]+' '+d["Name"], d["Free"].string(0)+'/ '+d["Size"].string(0))
      sleep(periode_s)
      if disk_state < len(drvs)-1:
        disk_state += 1
      else:
        disk_state = 0
        state += 1
    elif state == 2:
      lcd = writeLcd(lcd, 'IP', status.ip()[0])
      sleep(periode_s)
      state += 1
    elif state == 3:
      load = status.cpuLoad(math.ceil(periode_s))
      lcd = writeLcd(lcd, 'CPU Load', str(math.ceil(sum(load)/len(load)))+'%')
      #sleep(periode_s)
      state += 1
    elif state == 4:
      lcd = writeLcd(lcd, 'Uptime', status.uptime())
      sleep(periode_s)
      state = 0
    
    if not ser:
      printLcd(lcd)
    else:
      updateLcd(ser, lcd)
    
if __name__ == '__main__':
  main()