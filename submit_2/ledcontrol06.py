import RPi.GPIO as GPIO
import sys
import dht11
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, QStringListModel
from PyQt5.QtGui import QImage, QPixmap
import time

form_class = uic.loadUiType("./test01.ui")[0]

# GPIO 초기화
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 핀 설정
LED_RED = 19
LED_BLUE = 13
LED_GREEN = 6
DHT_PIN = 17
PIEZO_PIN = 18  # buzzer

# 센서 및 부저 설정
dht_sensor = dht11.DHT11(pin=DHT_PIN)
GPIO.setup(PIEZO_PIN, GPIO.OUT)
Buzz = GPIO.PWM(PIEZO_PIN, 440)

# LED 핀 설정
GPIO.setup(LED_RED, GPIO.OUT)
GPIO.setup(LED_BLUE, GPIO.OUT)
GPIO.setup(LED_GREEN, GPIO.OUT)

class DHTSensorReader(QThread):
    update_signal = pyqtSignal(list)

    def __init__(self, dht_sensor):
        super().__init__()
        self.dht_sensor = dht_sensor
        self.running = True

    def run(self):
        while self.running:
            result = self.dht_sensor.read()
            if result.is_valid():
                temperature = f"Temperature: {result.temperature:.1f}"
                humidity = f"Humidity: {result.humidity:.1f}%"
                self.update_signal.emit([temperature, humidity])
            else:
                self.update_signal.emit(["Failed to get reading. Try again!"])
            time.sleep(2)

    def stop(self):
        self.running = False
        self.wait()

class WindowClass(QMainWindow, form_class):
   def __init__(self):
      super().__init__()
      self.setupUi(self)
      
      self.Btn_ON.clicked.connect(self.btnOnFunction)
      self.Btn_OFF.clicked.connect(self.btnOffFunction)

      self.Btn_RED.clicked.connect(self.btnRedFunction)
      self.Btn_BLUE.clicked.connect(self.btnBlueFunction)
      self.Btn_GREEN.clicked.connect(self.btnGreenFunction)
      self.Btn_WHITE.clicked.connect(self.btnWhiteFunction)

      self.sensor_reader = DHTSensorReader(dht_sensor)
      self.sensor_reader.update_signal.connect(self.update_list_view)
      
      # QListView 설정
      self.model = QStringListModel()
      self.listView.setModel(self.model)
      self.sensor_reader = None 

      self.is_running = False

      self.Stbtn.clicked.connect(self.start_clicked)
      self.Spbtn.clicked.connect(self.stop_clicked)

   def btnOnFunction(self):
      print("LED가 활성화 되었습니다")

   def update_list_view(self, data):
      self.model.setStringList(data)
      if len(data) > 1 and "Humidity" in data[1]:
         humidity = float(data[1].split(':')[1].strip('%'))
         if humidity < 50:
            Buzz.stop()
         else:
            Buzz.start(50)

   def btnOffFunction(self):
      GPIO.output(LED_RED, True)
      GPIO.output(LED_BLUE, True)
      GPIO.output(LED_GREEN, True)
      print("LED가 종료되었습니다")

   def btnRedFunction(self):
      GPIO.output(LED_RED, False)
      GPIO.output(LED_BLUE, True)
      GPIO.output(LED_GREEN, True)
      print("빨간불이 켜졌습니다")

   def btnBlueFunction(self):
      GPIO.output(LED_RED, True)
      GPIO.output(LED_BLUE, False)
      GPIO.output(LED_GREEN, True)
      print("파란불이 켜졌습니다")

   def btnGreenFunction(self):
      GPIO.output(LED_RED, True)
      GPIO.output(LED_BLUE, True)
      GPIO.output(LED_GREEN, False)
      print("초록불이 켜졌습니다")

   def start_clicked(self):
      if not self.is_running:
         self.is_running = True
         self.sensor_reader = DHTSensorReader(dht_sensor)
         self.sensor_reader.update_signal.connect(self.update_list_view)
         self.sensor_reader.start()
         print("start")
            
   def stop_clicked(self):
      if self.is_running:
         self.is_running = False
         self.sensor_reader.stop()
         Buzz.stop()
         print("stop")

   def btnWhiteFunction(self):
      GPIO.output(LED_RED, False)
      GPIO.output(LED_BLUE, False)
      GPIO.output(LED_GREEN, False)
      print("흰색불이 켜졌습니다")
   
   def closeEvent(self, event):
      if self.sensor_reader and self.sensor_reader.isRunning():
         self.sensor_reader.stop()
         self.sensor_reader.wait()
      GPIO.cleanup()
      event.accept()

if __name__ == "__main__":
   app = QApplication(sys.argv)
   myWindow = WindowClass()
   myWindow.show()
   app.exec_()
