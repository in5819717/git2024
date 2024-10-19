import RPi.GPIO as GPIO
import time

# GPIO 핀 설정 (4개의 스위치)
switch_pins = [5, 6, 13, 19]  # SW1: 앞, SW2: 오른쪽, SW3: 왼쪽, SW4: 뒤
switch_states = [0, 0, 0, 0]  # 이전 스위치 상태 저장 리스트

# 모터 핀 설정
PWMA = 18  # 왼쪽 모터 PWM 제어 핀
AIN1 = 22  # 왼쪽 모터 방향 제어 핀 1
AIN2 = 27  # 왼쪽 모터 방향 제어 핀 2
PWMB = 23  # 오른쪽 모터 PWM 제어 핀
BIN1 = 24  # 오른쪽 모터 방향 제어 핀 1
BIN2 = 25  # 오른쪽 모터 방향 제어 핀 2

# GPIO 기본 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 스위치 핀들을 입력으로 설정
for pin in switch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 풀다운 저항 사용

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

try:
    while True:
        for i, pin in enumerate(switch_pins):
            current_state = GPIO.input(pin)

            if current_state == 1 and switch_states[i] == 0:
                # 어느 스위치가 눌렸는지 출력
                print(f'SW{i+1} clicked')

                if i == 0:  # SW1: 앞으로 이동
                    GPIO.output(AIN1, 0)  # 왼쪽 모터 정방향
                    GPIO.output(AIN2, 1)
                    GPIO.output(BIN1, 1)  # 오른쪽 모터 정방향
                    GPIO.output(BIN2, 0)
                    L_Motor.ChangeDutyCycle(50)  # 왼쪽 모터 50% 속도
                    R_Motor.ChangeDutyCycle(50)  # 오른쪽 모터 50% 속도
                    print("Moving forward")

                elif i == 1:  # SW2: 오른쪽 회전
                    GPIO.output(AIN1, 0)  # 왼쪽 모터 정방향
                    GPIO.output(AIN2, 1)
                    GPIO.output(BIN1, 0)  # 오른쪽 모터 후진
                    GPIO.output(BIN2, 1)
                    L_Motor.ChangeDutyCycle(50)  # 왼쪽 모터 50% 속도
                    R_Motor.ChangeDutyCycle(50)  # 오른쪽 모터 50% 속도
                    print("Turning right")

                elif i == 2:  # SW3: 왼쪽 회전
                    GPIO.output(AIN1, 1)  # 왼쪽 모터 후진
                    GPIO.output(AIN2, 0)
                    GPIO.output(BIN1, 1)  # 오른쪽 모터 정방향
                    GPIO.output(BIN2, 0)
                    L_Motor.ChangeDutyCycle(50)  # 왼쪽 모터 50% 속도
                    R_Motor.ChangeDutyCycle(50)  # 오른쪽 모터 50% 속도
                    print("Turning left")

                elif i == 3:  # SW4: 뒤로 이동
                    GPIO.output(AIN1, 1)  # 왼쪽 모터 후진
                    GPIO.output(AIN2, 0)
                    GPIO.output(BIN1, 0)  # 오른쪽 모터 후진
                    GPIO.output(BIN2, 1)
                    L_Motor.ChangeDutyCycle(50)  # 왼쪽 모터 50% 속도
                    R_Motor.ChangeDutyCycle(50)  # 오른쪽 모터 50% 속도
                    print("Moving backward")
            
            # 이전 상태를 업데이트
            switch_states[i] = current_state

        time.sleep(0.1)  # CPU 사용량을 줄이기 위해 딜레이 추가

except KeyboardInterrupt:
    pass

finally:
    L_Motor.stop()  # 왼쪽 모터 PWM 중지
    R_Motor.stop()  # 오른쪽 모터 PWM 중지
    GPIO.cleanup()  # GPIO 핀 정리
