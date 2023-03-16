from pedalboard.io import AudioFile as AF
import os
import numpy as np
from stftpitchshift import StftPitchShift
from PIL import Image, ImageDraw, ImageFont
table = {'1': 'methionyl', '2': 'threonyl', '3': 'glutaminyl', '4': 'alanyl', '5': 'prolyl', '6': 'phenylalanyl', '7': 'leucyl', '8': 'seryl', '9': 'valyl',
         'A': 'glutamyl', 'B': 'glycyl', 'C': 'histidyl', 'D': 'isoleucyl', 'E': 'tryptophyl', 'F': 'arginyl', 'G': 'aspartyl', 'H': 'lysyl', 'I': 'asparaginyl', 'J': 'tyrosyl', 'K': 'cysteinyl', 'L': 'isoleucine'}
sample_rate = 44100
pshift = StftPitchShift(2048, 128, sample_rate)
q = 0.004  # wtf is a quefrency?
padding = 600  # to prevent artifacts
gain = 1.5

with open('./titincode') as f:  # why did sed give me invisible chars?
    code = f.readline()
with open('./miku') as f2:
    notes = []
    for i in range(256):
        notes.append(int(f2.readline()))

font_lg = ImageFont.truetype('./KeeponTruckin.ttf', 64)
font_sm = ImageFont.truetype('./KeeponTruckin.ttf', 42)
echo1 = Image.new('RGB', (640, 480), '#2B2A2B')
echo2 = Image.new('RGB', (640, 480), '#2B2A2B')
echo1.paste(Image.open('./echos/echo1.png'),
            (195, 250), Image.open('./echos/echo1.png'))
echo2.paste(Image.open('./echos/echo2.png'),
            (195, 250), Image.open('./echos/echo2.png'))
imgs = [echo1, echo2]

table2 = {}  # stores audio info
for k, v in table.items():
    segments = 4
    if k == '6' or k == 'I':  # names too long
        segments = 6
    with AF(f'./processed/{table[k]}.wav', 'r') as f:
        full_word = f.read(f.frames-1)

    table2[k] = []
    for i in range(segments):  # grab 0.2s segments
        l_seg = i*sample_rate//5 - padding * (i != 0)
        r_seg = (i+1)*sample_rate//5 + padding * (i != segments-1)
        table2[k].append(np.array([full_word[0][l_seg:r_seg],
                         full_word[1][l_seg:r_seg]]))

counter = 0
with AF('./audio.mp3', 'w', num_channels=2, samplerate=sample_rate) as fw:
    for j, e in enumerate(code):
        for i, e2 in enumerate(table2.get(e)):
            segnum = len(table2.get(e))
            if notes[counter % 256] != 0:
                ratio = pow(2, notes[counter % 256]/12)  # music theory moment
                l = np.array(pshift.shiftpitch(
                    e2[0], factors=ratio, quefrency=q)) * gain
                r = np.array(pshift.shiftpitch(
                    e2[1], factors=ratio, quefrency=q)) * gain
            else:
                l = e2[0]
                r = e2[1]
            l = l[padding * (i != 0):len(l)-padding * (i != (segnum-1))]
            r = r[padding * (i != 0):len(r)-padding * (i != (segnum-1))]
            fw.write(np.array([l, r]))

            tmp_img = imgs[(counter//2) % 2].copy()
            tdraw = ImageDraw.Draw(tmp_img)
            tdraw.text((320, 60), f'{j+1}',
                       fill='#FEE879', anchor='mm', font=font_lg)

            tdraw.text((320, 165), f'{table[code[j]]}',
                       fill='white', anchor='ms', font=font_lg)
            if j != 0:
                tdraw.text((320-font_lg.getsize(table[code[j]])[0]//2-20, 165),
                           f'{table[code[j-1]]}', fill='#CCCBCC', anchor='rs', font=font_sm)
            if j != len(code) - 1:
                tdraw.text((320+font_lg.getsize(table[code[j]])[0]//2+20, 165),
                           f'{table[code[j+1]]}', fill='#CCCBCC', anchor='ls', font=font_sm)
            tmp_img.save(f'./images/{counter:07}.png')

            counter += 1
os.system('sh ./render.sh')
