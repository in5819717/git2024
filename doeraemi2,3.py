import RPi.GPIO as GPIO
import time

# BUZZER와 SWITCH 핀 설정
BUZZER = 12
SWITCH = 5  # 스위치 1번 핀 설정

# 미레도레미미미 음계 주파수 (Hz)
notes = [330, 294, 261, 294, 330, 330, 330]  # 미, 레, 도, 레, 미, 미, 미

# GPIO 기본 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 스위치 1번을 입력 모드로 설정

# PWM 객체 생성 (버저 핀, 주파수)
p = GPIO.PWM(BUZZER, 330)  # 초기 주파수는 미(330 Hz)로 설정
p.start(0)  # 처음에는 PWM을 정지 상태로 시작

def play_horn():
    """미레도레미미미 경적 소리 재생 후 종료"""
    for note in notes:
        p.ChangeFrequency(note)  # 주파수를 변경하여 해당 음을 재생
        p.start(50)  # 50% 듀티 사이클로 소리 재생
        time.sleep(0.4)  # 각 음을 0.4초 동안 재생
    p.stop()  # 소리를 끕니다

try:
    while True:
        if GPIO.input(SWITCH) == GPIO.HIGH:  # 스위치 1번이 눌렸을 때
            play_horn()  # 미레도레미미미 경적 소리 출력
            break  # 경적 소리 출력 후 프로그램 종료

except KeyboardInterrupt:
    pass

# 종료 처리
p.stop()
GPIO.cleanup()
