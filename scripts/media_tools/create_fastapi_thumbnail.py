# -*- coding: utf-8 -*-
"""
FastAPI 썸네일 이미지 생성 스크립트
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 이미지 크기
WIDTH, HEIGHT = 800, 450

# FastAPI 컬러 (공식 컬러)
FASTAPI_GREEN = "#009688"
FASTAPI_DARK = "#004D40"
BACKGROUND_GRADIENT_START = "#1a1a2e"
BACKGROUND_GRADIENT_END = "#16213e"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#00d4aa"

# 이미지 생성
image = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND_GRADIENT_START)
draw = ImageDraw.Draw(image)

# 그라디언트 배경 (수직)
for y in range(HEIGHT):
    r = int(BACKGROUND_GRADIENT_START[1:3], 16) + (int(BACKGROUND_GRADIENT_END[1:3], 16) - int(BACKGROUND_GRADIENT_START[1:3], 16)) * y // HEIGHT
    g = int(BACKGROUND_GRADIENT_START[3:5], 16) + (int(BACKGROUND_GRADIENT_END[3:5], 16) - int(BACKGROUND_GRADIENT_START[3:5], 16)) * y // HEIGHT
    b = int(BACKGROUND_GRADIENT_START[5:7], 16) + (int(BACKGROUND_GRADIENT_END[5:7], 16) - int(BACKGROUND_GRADIENT_START[5:7], 16)) * y // HEIGHT
    for x in range(WIDTH):
        image.putpixel((x, y), (r, g, b))

# FastAPI 로고 스타일의 "F" 그리기 (간소화된 버전)
# 왼쪽에 큰 "F" 문자
f_width = 180
f_height = 280
f_x = 80
f_y = (HEIGHT - f_height) // 2

# F 의 세 부분 (위, 중간, 아래)
# 위 부분
draw.rectangle([f_x, f_y, f_x + f_width, f_y + 50], fill=ACCENT_COLOR)
# 중간 부분
draw.rectangle([f_x, f_y + 115, f_x + f_width, f_y + 165], fill=ACCENT_COLOR)
# 세로 부분
draw.rectangle([f_x, f_y, f_x + 50, f_y + f_height], fill=ACCENT_COLOR)

# 오른쪽에 "FastAPI" 텍스트 (간단한 사각형으로 표현)
text_x = f_x + f_width + 60
text_y = f_y + 20

# "Fast" 부분
draw.rectangle([text_x, text_y, text_x + 200, text_y + 60], fill=TEXT_COLOR)
# "API" 부분 (초록색)
draw.rectangle([text_x + 220, text_y, text_x + 380, text_y + 60], fill=ACCENT_COLOR)

# 코드 스니펫 스타일 장식 (오른쪽 하단)
code_x = WIDTH - 280
code_y = HEIGHT - 120

# 코드 배경
draw.rectangle([code_x, code_y, WIDTH - 40, HEIGHT - 40], fill=(0, 0, 0, 128))

# 코드 라인 (간소화)
line_color = "#4a5568"
for i in range(5):
    y = code_y + 15 + i * 18
    line_width = 150 - i * 20
    draw.rectangle([code_x + 15, y, code_x + 15 + line_width, y + 10], fill=line_color)

# @app.get 데코레이터 스타일
draw.rectangle([code_x + 15, code_y + 15, code_x + 100, code_y + 30], fill=ACCENT_COLOR)

# 하단 그라디언트 오버레이
for y in range(HEIGHT - 60, HEIGHT):
    alpha = (y - (HEIGHT - 60)) / 60
    for x in range(WIDTH):
        r, g, b = image.getpixel((x, y))
        r = int(r * (1 - alpha * 0.5))
        g = int(g * (1 - alpha * 0.5))
        b = int(b * (1 - alpha * 0.5))
        image.putpixel((x, y), (r, g, b))

# 저장
output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'uploads')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'fastapi_thumbnail.png')

image.save(output_path, 'PNG')
print(f"[OK] FastAPI 썸네일 이미지 생성 완료: {output_path}")
print(f"   크기: {WIDTH}x{HEIGHT}")
