# this file is broken lol

# sed -r "s/methionyl/1/g; s/threonyl/2/g; s/glutaminyl/3/g; s/phenylalanyl/6/g; s/alanyl/4/g; s/prolyl/5/g; s/isoleucyl/D/g; s/leucyl/7/g; s/seryl/8/g; s/valyl/9/g; s/glutamyl/A/g; s/glycyl/B/g; s/histidyl/C/g; s/tryptophyl/E/g; s/arginyl/F/g; s/aspartyl/G/g; s/lysyl/H/g; s/asparaginyl/I/g; s/tyrosyl/J/g; s/cysteinyl/K/g; s/isoleucine/L/g; "  titin > titincode
# LANG=C sed -i 's/[\d128-\d255]//g' titincode

# duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 audio.mp3)
# ffmpeg -y -t $duration -f concat -safe 0 -i concat.txt -c:a libmp3lame -t $duration concat_acc.mp3
# didn't work lmao, half of the audio is missing

# ffmpeg -y -i audio.mp3 -i concat_acc.mp3 -filter_complex amix=inputs=2:duration=longest merged.mp3

ffmpeg -y -framerate 5 -i ./images/%07d.png -i merged.mp3 -c:a aac -b:a 192k -c:v libx264 -pix_fmt yuv420p -shortest -loop 1 out.mp4
# ffmpeg -f concat -safe 0 -i concat2 -c copy final.mp4
# doesn't work, either speeds the video up or slows the audio down

ffmpeg -i start.mp4 -i out.mp4 \
-filter_complex "[0:v] [0:a] [1:v] [1:a] \
concat=n=2:v=1:a=1 [v] [a]" \
-map "[v]" -map "[a]" final.mp4
