import threading
import serial
import RPi.GPIO as GPIO
import time

# Bluetooth 시리얼 포트 설정
bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)

# 전역 변수
gData = ""

# GPIO 핀 설정 (모터 제어)
PWMA = 18  # 왼쪽 모터 PWM 제어 핀
AIN1 = 22  # 왼쪽 모터 방향 제어 핀 1
AIN2 = 27  # 왼쪽 모터 방향 제어 핀 2
PWMB = 23  # 오른쪽 모터 PWM 제어 핀
BIN1 = 24  # 오른쪽 모터 방향 제어 핀 1
BIN2 = 25  # 오른쪽 모터 방향 제어 핀 2

# GPIO 기본 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 모터 핀 설정
GPIO.setup(PWMA, GPIO.OUT)  # 왼쪽 모터 PWM 출력 핀 설정
GPIO.setup(AIN1, GPIO.OUT)  # 왼쪽 모터 방향 제어 핀 1 설정
GPIO.setup(AIN2, GPIO.OUT)  # 왼쪽 모터 방향 제어 핀 2 설정
GPIO.setup(PWMB, GPIO.OUT)  # 오른쪽 모터 PWM 출력 핀 설정
GPIO.setup(BIN1, GPIO.OUT)  # 오른쪽 모터 방향 제어 핀 1 설정
GPIO.setup(BIN2, GPIO.OUT)  # 오른쪽 모터 방향 제어 핀 2 설정

# PWM 설정
L_Motor = GPIO.PWM(PWMA, 500)  # 왼쪽 모터 PWM, 500Hz
R_Motor = GPIO.PWM(PWMB, 500)  # 오른쪽 모터 PWM, 500Hz

# PWM 시작 (모터 멈춤)
L_Motor.start(0)  # 왼쪽 모터 정지 상태에서 시작
R_Motor.start(0)  # 오른쪽 모터 정지 상태에서 시작

# 시리얼 데이터를 읽는 스레드 함수
def serial_thread():
    global gData
    while True:
        data = bleSerial.readline()  # Bluetooth에서 데이터 읽기
        data = data.decode().strip() # 디코딩 후 양 끝의 공백 제거
        gData = data                 # 전역 변수에 할당

# 명령에 따른 동작 정의
def go():
    print("go")
    GPIO.output(AIN1, 0)  # 왼쪽 모터 정방향
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 1)  # 오른쪽 모터 정방향
    GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(50)  # 왼쪽 모터 50% 속도
    R_Motor.ChangeDutyCycle(50)  # 오른쪽 모터 50% 속도

def back():
    print("back")
    GPIO.output(AIN1, 1)  # 왼쪽 모터 후진
    GPIO.output(AIN2, 0)
    GPIO.output(BIN1, 0)  # 오른쪽 모터 후진
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(50)  # 왼쪽 모터 50% 속도
    R_Motor.ChangeDutyCycle(50)  # 오른쪽 모터 50% 속도

def left():
    print("left")
    GPIO.output(AIN1, 1)  # 왼쪽 모터 후진
    GPIO.output(AIN2, 0)
    GPIO.output(BIN1, 1)  # 오른쪽 모터 정방향
    GPIO.output(BIN2, 0)
    L_Motor.ChangeDutyCycle(50)  # 왼쪽 모터 50% 속도
    R_Motor.ChangeDutyCycle(50)  # 오른쪽 모터 50% 속도

def right():
    print("right")
    GPIO.output(AIN1, 0)  # 왼쪽 모터 정방향
    GPIO.output(AIN2, 1)
    GPIO.output(BIN1, 0)  # 오른쪽 모터 후진
    GPIO.output(BIN2, 1)
    L_Motor.ChangeDutyCycle(50)  # 왼쪽 모터 50% 속도
    R_Motor.ChangeDutyCycle(50)  # 오른쪽 모터 50% 속도

def stop():
    print("Stop")
    L_Motor.ChangeDutyCycle(0)  # 왼쪽 모터 정지
    R_Motor.ChangeDutyCycle(0)  # 오른쪽 모터 정지

# 메인 함수: 받은 명령에 따라 함수 호출
def main():
    global gData
    try:
        while True:
            # gData 값을 확인하여 적절한 함수 호출
            if "go" in gData:
                gData = ""
                go()
            elif "back" in gData:
                gData = ""
                back()
            elif "left" in gData:
                gData = ""
                left()
            elif "right" in gData:
                gData = ""
                right()
            elif "stop" in gData:
                gData = ""
                stop()
                
            time.sleep(0.1)  # CPU 사용량을 줄이기 위해 대기 시간 추가

    except KeyboardInterrupt:
        pass

# 프로그램 시작
if __name__ == "__main__":
    # 시리얼 스레드 시작
    task1 = threading.Thread(target=serial_thread)
    task1.start()
    
    # 메인 함수 실행
    main()
    
    # 프로그램 종료 시 시리얼 포트 닫기 및 GPIO 정리
    bleSerial.close()
    L_Motor.stop()  # 왼쪽 모터 PWM 중지
    R_Motor.stop()  # 오른쪽 모터 PWM 중지
    GPIO.cleanup()  # GPIO 핀 정리
