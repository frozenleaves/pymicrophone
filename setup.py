# -*- coding: utf-8 -*-

import setuptools

setuptools.setup(
    name="PyMicrophone",
    version="1.0.1",
    py_modules=['microphone'],
    packages=setuptools.find_packages(),
    author="幽若",
    author_email="914814442@qq.com",
    description="使用python录音",
    install_requires=['PyAudio>=0.2.11'],

    url="http://frozenleaves.cn/pymicrophone",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
