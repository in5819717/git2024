import RPi.GPIO as GPIO
import time

# GPIO 핀 설정 (4개의 스위치)
switch_pins = [5, 6, 13, 19]  # 사용할 GPIO 핀 번호
switch_states = [0, 0, 0, 0]  # 이전 스위치 상태 저장 리스트
switch_clicks = [0, 0, 0, 0]  # 각 스위치별 클릭 수 저장 리스트

# GPIO 기본 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# 스위치 핀들을 입력으로 설정
for pin in switch_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # PUD_DOWN은 내부 풀다운 저항 사용

try:
    click_count = 0
    while True:
        for i, pin in enumerate(switch_pins):
            current_state = GPIO.input(pin)
            
            # 스위치 상태가 0 -> 1로 바뀌었을 때 (눌림)
            if current_state == 1 and switch_states[i] == 0:
                click_count += 1
                switch_clicks[i] += 1  # 해당 스위치의 클릭 수 증가
                # 출력 형식을 ('SW1 click', 1) 형태로 변경
                print((f'SW{i+1} click', switch_clicks[i]))
            
            # 이전 상태를 업데이트
            switch_states[i] = current_state
        
        time.sleep(0.1)  # CPU 사용량을 줄이기 위해 약간의 딜레이 추가

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
