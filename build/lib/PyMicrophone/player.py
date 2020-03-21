# -*- coding: utf-8 -*-

import wave
import time
import threading
import pyaudio


class Player(object):
    """
    Player类接受一个wav文件名作为传入参数，可以类似调用函数那样调用实例对象，可以实现文件的播放。
    注意：
    Player类并未实现为单例模式，但为了获取良好的播放效果，请确保在同一时间只有一个对象被调用！
    用法：
        from PyMicrophone import player

        p = player.Player('test.wav')
        p()
    """

    def __init__(self, file, chunk=1024):
        self.file = file
        self.CHUNK = chunk

    def get_duration(self):
        """获取文件时长"""

        with wave.open(self.file) as df:
            rate = df.getframerate()
            frames = df.getnframes()
            return round(frames / float(rate))

    def __play(self):
        with wave.open(self.file) as wf:
            player = pyaudio.PyAudio()
            stream = player.open(format=player.get_format_from_width(wf.getsampwidth()),
                                 channels=wf.getnchannels(),
                                 rate=wf.getframerate(),
                                 output=True)
            data = wf.readframes(self.CHUNK)
            while data:
                stream.write(data)
                data = wf.readframes(self.CHUNK)
            stream.stop_stream()
            stream.close()
            player.terminate()

    def __timer(self):
        print("正在播放……")
        for t in range(int(self.get_duration())):
            print("\r剩余时间：%d" % (int(self.get_duration()) - t), end='')
            time.sleep(1)
        print("\r播放结束！")

    def __call__(self, *args, **kwargs):

        player = threading.Thread(target=self.__play)
        timer = threading.Thread(target=self.__timer)
        player.start()
        timer.start()
        player.join()
        timer.join()


if __name__ == '__main__':
    p = Player('test.wav')

    p()
