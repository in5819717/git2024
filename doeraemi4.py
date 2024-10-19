import RPi.GPIO as GPIO
import time

# BUZZER와 SWITCH 핀 설정
BUZZER = 12
switch_pins = [5, 6, 13, 19]  # 스위치 1, 2, 3, 4에 대응되는 핀

# 도레미솔 음계 주파수 (Hz)
notes = [261, 294, 330, 392]  # 도, 레, 미, 솔

# GPIO 기본 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

for pin in switch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 스위치 핀을 입력 모드로 설정

# PWM 객체 생성 (버저 핀, 주파수)
p = GPIO.PWM(BUZZER, 261)  # 초기 주파수는 도(261 Hz)로 설정
p.start(0)  # 처음에는 PWM을 정지 상태로 시작

def play_tone(frequency):
    """특정 주파수(frequency)를 재생"""
    p.ChangeFrequency(frequency)  # 주파수를 변경
    p.start(50)  # 50% 듀티 사이클로 소리 재생
    time.sleep(0.5)  # 0.5초 동안 재생
    p.stop()  # 소리를 끔

try:
    while True:
        for i, pin in enumerate(switch_pins):
            if GPIO.input(pin) == GPIO.HIGH:  # 스위치가 눌렸을 때
                play_tone(notes[i])  # 해당하는 음계를 재생
                time.sleep(0.2)  # 중복 입력 방지용 딜레이

except KeyboardInterrupt:
    pass

# 종료 처리
p.stop()
GPIO.cleanup()

