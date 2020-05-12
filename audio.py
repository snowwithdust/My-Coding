'''
利用python的第三方库PyAudio实现录音然后进行傅里叶变换得到频谱图
'''

import wave
import pyaudio
import numpy
from pyaudio import PyAudio
import matplotlib.pyplot as plt

# 定义数据流块
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
# 录音时间
RECORD_SECONDS = 10
# 要写入的文件名
WAVE_OUTPUT_FILENAME = "output.wav"
# 创建PyAudio对象
p = pyaudio.PyAudio()

# 打开数据流
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

# 开始录音
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

# 停止数据流
stream.stop_stream()
stream.close()

# 关闭PyAudio
p.terminate()

# 写入录音文件
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


# 只读方式打开WAV文件
wf = wave.open('./output.wav', 'rb')


nframes = wf.getnframes()
framerate = wf.getframerate()


# 读取完整的帧数据到str_data中，这是一个string类型的数据
str_data = wf.readframes(nframes)
wf.close()

# 将波形数据转换成数组
wave_data = numpy.frombuffer(str_data, dtype=numpy.short)
# 将wave_data数组改为2列，行数自动匹配
wave_data.shape = -1,2
# 将数组转置
wave_data = wave_data.T


plt.figure()
# time也是一个数组，与wave_data[0]或wave_data[1]配对形成系列点坐标
time = numpy.arange(0, nframes)*(1.0/framerate)
# 绘制波形图
plt.subplot(211)
plt.plot(time, wave_data[0], c='r')
plt.subplot(212)
plt.plot(time, wave_data[1], c='g')
plt.xlabel('time (seconds)')


plt.figure()
# 采样点数，修改采样点数和起始位置进行不同位置和长度的音频波形分析
N = 44100
start = 0  # 开始采样位置
df = framerate/(N-1)  # 分辨率
freq = [df*n for n in range(0, N)]  # N个元素
wave_data2 = wave_data[0][start:start+N]
c = numpy.fft.fft(wave_data2)*2/N
# 常规显示采样频率一半的频谱
d = int(len(c)/2)
# 仅显示频率在4000以下的频谱
while freq[d] > 4000:
    d -= 10
plt.plot(freq[:d-1], abs(c[:d-1]), 'r')
plt.show()

