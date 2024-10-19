import RPi.GPIO as GPIO
import time

# 왼쪽 모터 핀 설정
PWMA = 18  # PWM 제어 핀 (왼쪽 모터)
AIN1 = 22  # 방향 제어 핀 1
AIN2 = 27  # 방향 제어 핀 2

# 오른쪽 모터 핀 설정
PWMB = 23  # PWM 제어 핀 (오른쪽 모터)
BIN1 = 24  # 방향 제어 핀 1
BIN2 = 25  # 방향 제어 핀 2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 왼쪽 모터 핀 설정
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)

# 오른쪽 모터 핀 설정
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

# PWM 설정
L_Motor = GPIO.PWM(PWMA, 500)  # 왼쪽 모터 PWM 주파수 500Hz
R_Motor = GPIO.PWM(PWMB, 500)  # 오른쪽 모터 PWM 주파수 500Hz

# PWM 시작 (모터 멈춤)
L_Motor.start(0)
R_Motor.start(0)

try:
    while True:
        # 왼쪽 모터와 오른쪽 모터 모두 정방향으로 설정 (앞으로 가도록 설정)
        GPIO.output(AIN1, 0)  # 왼쪽 모터: AIN1 = 0, AIN2 = 1 (정방향)
        GPIO.output(AIN2, 1)
        L_Motor.ChangeDutyCycle(50)  # 왼쪽 모터 50% 속도
        
        GPIO.output(BIN1, 1)  # 오른쪽 모터: BIN1 = 1, BIN2 = 0 (정방향)
        GPIO.output(BIN2, 0)
        R_Motor.ChangeDutyCycle(50)  # 오른쪽 모터 50% 속도
        
        print("왼쪽 및 오른쪽 모터: 정방향 50% 속도")
        
        time.sleep(2)  # 2초 동안 동작
        
        # 모터 정지
        L_Motor.ChangeDutyCycle(0)
        R_Motor.ChangeDutyCycle(0)
        print("왼쪽 및 오른쪽 모터: 정지")
        
        time.sleep(1)  # 1초 동안 정지

except KeyboardInterrupt:
    pass

finally:
    # 정리 작업
    L_Motor.stop()
    R_Motor.stop()
    GPIO.cleanup()
