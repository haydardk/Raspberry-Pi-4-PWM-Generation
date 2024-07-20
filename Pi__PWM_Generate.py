import pigpio
import time
import threading

GPIO_PIN = 12
PWM_FRQ = 90  # 90 Hz

# Duty cycle değerleri
DUTY_CYCLE_10 = 100000  # 10%
DUTY_CYCLE_17 = 170000  # 17%

# pigpio instance oluştur
pi = pigpio.pi()

if not pi.connected:
    print("Can't connect to pigpio daemon. Make sure it's running.")
    exit(0)

# PWM sinyalini ayarla
pi.set_mode(GPIO_PIN, pigpio.OUTPUT)

def set_pwm(duty_cycle):
    pi.hardware_PWM(GPIO_PIN, PWM_FRQ, duty_cycle)

def monitor_keyboard():
    try:
        while True:
            user_input = input("Press 'A' to set 10% duty cycle or 'B' to set 17% duty cycle: ")
            if user_input.lower() == 'a':
                print("Setting duty cycle to 10%")
                set_pwm(DUTY_CYCLE_10)
            elif user_input.lower() == 'b':
                print("Setting duty cycle to 17%")
                set_pwm(DUTY_CYCLE_17)
    except KeyboardInterrupt:
        pass

# Klavyeyi dinlemek için yeni bir thread başlat
keyboard_thread = threading.Thread(target=monitor_keyboard)
keyboard_thread.start()

try:
    while True:
        time.sleep(0.0001)
except KeyboardInterrupt:
    pass
finally:
    pi.set_mode(GPIO_PIN, pigpio.INPUT)  # GPIO pinini giriş olarak ayarla
    pi.stop()
