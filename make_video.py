import json

with open('sequence.json') as f:
    announcements = json.load(f)

total_duration = 31 * 60

segments = []
for i, (t, num) in enumerate(announcements):
    start = t
    end = announcements[i+1][0] if i+1 < len(announcements) else total_duration
    segments.append((start, end, num))

bg_hex = {1: '8B0000', 2: '006400', 3: '00008B', 4: 'FF8C00'}

drawbox_filters = []
drawtext_filters = []

for num in [1, 2, 3, 4]:
    times = [(s, e) for (s, e, n) in segments if n == num]
    enable_expr = '+'.join([f'between(t,{s},{e})' for (s, e) in times])

    drawbox_filters.append(
        f"drawbox=x=0:y=0:w=iw:h=ih:color=0x{bg_hex[num]}:t=fill:enable='{enable_expr}'"
    )
    drawtext_filters.append(
        f"drawtext=text='{num}':fontsize=300:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:enable='{enable_expr}'"
    )

timer_text = "drawtext=text='%{pts\\:hms}':fontsize=40:fontcolor=white@0.7:x=20:y=20"

all_filters = drawbox_filters + drawtext_filters + [timer_text]
filter_str = ','.join(all_filters)

cmd = f"""ffmpeg -y \\
  -f lavfi -i color=c=black:size=720x720:rate=1 \\
  -i audio.wav \\
  -filter_complex "[0:v]{filter_str}[v]" \\
  -map "[v]" -map 1:a \\
  -t {total_duration} \\
  -c:v libx264 -preset ultrafast -crf 28 \\
  -c:a aac -b:a 64k \\
  random_numbers.mp4"""

import os
os.system(cmd)
