import struct, wave
from pathlib import Path

root = Path(__file__).resolve().parent.parent
work = root / 'okr_video_work'
frames = sorted((work / 'frames').glob('frame-*.jpg'))
audio_path = work / 'narration.wav'
out = root / 'estrategia-okr-e-valoracao-ti.avi'
fps = 10
w, h = 1280, 720
with wave.open(str(audio_path), 'rb') as wav:
    channels, width, rate, samples, *_ = wav.getparams()
    audio = wav.readframes(samples)
assert channels == 1 and width == 2
assert len(frames) == 1770

def chunk(fcc, data):
    return fcc + struct.pack('<I', len(data)) + data + (b'\0' if len(data) & 1 else b'')

def list_chunk(kind, data):
    return chunk(b'LIST', kind + data)

def stream_header(kind, handler, scale, rate_value, length, suggested, sample_size, rect=(0,0,0,0)):
    return struct.pack('<4s4sIHHIIIIIIIIhhhh', kind, handler, 0, 0, 0, 0, scale, rate_value, 0,
                       length, suggested, 0xFFFFFFFF, sample_size, *rect)

max_frame = max(p.stat().st_size for p in frames)
# AVI headers: main stream plus MJPEG video and PCM audio.
avih = struct.pack('<14I', int(1_000_000/fps), max_frame*fps + rate*channels*width,
                   0, 0x10, len(frames), 0, 2, max_frame, w, h, 0, 0, 0, 0)
v_strh = stream_header(b'vids', b'MJPG', 1, fps, len(frames), max_frame, 0, (0,0,w,h))
v_strf = struct.pack('<IiiHH4sIiiII', 40, w, h, 1, 24, b'MJPG', 0, 0, 0, 0, 0)
a_strh = stream_header(b'auds', b'\0\0\0\0', channels*width, rate, samples, rate*channels*width, channels*width)
a_strf = struct.pack('<HHIIHHH', 1, channels, rate, rate*channels*width, channels*width, width*8, 0)
hdrl = list_chunk(b'hdrl', chunk(b'avih', avih) +
                  list_chunk(b'strl', chunk(b'strh', v_strh) + chunk(b'strf', v_strf)) +
                  list_chunk(b'strl', chunk(b'strh', a_strh) + chunk(b'strf', a_strf)))

movi = bytearray()
index = []
audio_pos = 0
samples_per_frame = rate // fps
for i, frame in enumerate(frames):
    jpeg = frame.read_bytes()
    offset = len(movi)
    c = chunk(b'00dc', jpeg)
    movi.extend(c)
    index.append((b'00dc', 0x10, offset, len(jpeg)))
    take = samples_per_frame if i < len(frames)-1 else samples-audio_pos
    block = audio[audio_pos*channels*width:(audio_pos+take)*channels*width]
    audio_pos += take
    if block:
        offset = len(movi)
        c = chunk(b'01wb', block)
        movi.extend(c)
        index.append((b'01wb', 0, offset, len(block)))
assert audio_pos == samples
movi_list = list_chunk(b'movi', bytes(movi))
idx1 = chunk(b'idx1', b''.join(struct.pack('<4sIII', *entry) for entry in index))
body = hdrl + movi_list + idx1
out.write_bytes(b'RIFF' + struct.pack('<I', len(body)+4) + b'AVI ' + body)
print(f'{out}: {out.stat().st_size/1_000_000:.1f} MB, {len(frames)} frames, {samples/rate:.3f} s audio, {rate} Hz PCM')
