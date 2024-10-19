import RPi.GPIO as GPIO
import time

# BUZZER 핀 설정
BUZZER = 12

# 도레미파솔라시도 음계 주파수 (Hz)
notes = [261, 294, 330, 349, 392, 440, 494, 523]  # 도, 레, 미, 파, 솔, 라, 시, 높은 도

# GPIO 기본 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

# PWM 객체 생성 (버저 핀, 주파수)
p = GPIO.PWM(BUZZER, 261)  # 초기 주파수는 도(261 Hz)로 설정
p.start(50)  # 50% 듀티 사이클로 소리 재생

try:
    while True:
        for note in notes:
            p.ChangeFrequency(note)  # 음계 주파수를 변경
            time.sleep(0.5)  # 각 음을 0.5초 동안 재생
        time.sleep(1.0)  # 한 번 다 돌면 1초 대기

except KeyboardInterrupt:
    pass

# 종료 처리
p.stop()
GPIO.cleanup()
