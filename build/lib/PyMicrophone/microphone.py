# -*- coding: utf-8 -*-

import pyaudio
import wave
import time
import threading


class Microphone(object):
    """
    class Microphone can use the system's microphone to record sounds to a file
    parameter:
    output_file: audio file save path
    record_time: record duration, in second

    usage:
        import microphone

        m = microphone.Microphone("test.wav", 30)
        m.record()
        m.save()

    """
    instance = None  # 定义类属性，记录实例对象引用
    init_flag = False  # 记录初始化方法执行状态

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self, output_file, record_time,
                 chunk=1024, __format=pyaudio.paInt16, channels=2, rate=44100):
        if not Microphone.init_flag:
            Microphone.init_flag = True
            self.CHUNK = chunk  # 缓冲区大小
            self.FORMAT = __format
            self.CHANNELS = channels  # 声道
            self.RATE = rate  # 比特率
            self.RECORD_TIME = record_time
            self.OUTPUT = output_file
            self.audio = pyaudio.PyAudio()
            self.frames = []
        else:
            return

    def __timer(self):
        print("开始录音……")
        for t in range(int(self.RECORD_TIME)):
            print("\r剩余时间：%d" % (int(self.RECORD_TIME) - t), end='')
            time.sleep(1)

    def __record(self):
        """use this method to complete recording"""

        stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_TIME)):
            self.frames.append(stream.read(self.CHUNK))
        print("\n录音结束！")
        stream.stop_stream()
        stream.close()
        self.audio.terminate()

    def record(self):
        records = threading.Thread(target=self.__record)
        timer = threading.Thread(target=self.__timer)
        timer.start()
        records.start()
        records.join()
        timer.join()

    def save(self):
        """use this method to save audio stream"""

        with wave.open(self.OUTPUT, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()
        return 0


if __name__ == '__main__':
    m = Microphone('test.wav', 10)
    m.record()
    m.save()
