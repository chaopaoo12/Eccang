# -*- encoding: utf-8 -*-
'''
@File    :   setup.py
@Time    :   2024/12/13 13:54:25
@Author  :   chaopaoo12 
@Version :   1.0
@Contact :   chaopaoo12@hotmail.com
'''

# here put the import lib

from setuptools import setup, find_packages

setup(
    name="Eccang",
    version="1.0",
    author="chaopaoo12",
    author_email="chaopaoo12@hotmail.com",
    description="Eccang",

    # 项目主页

    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages(),
)
