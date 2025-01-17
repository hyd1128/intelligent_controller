#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2024/12/19 16:06
# @Author : limber
# @desc :
import json

example = '[["1", "2", "4"],["1", "2", "4"],["1", "2", "4"]]'

example_ = json.loads(example)
print(type(example_))
print(type(example_[0]))


# for i in range(10):
#     if i == 3:
#         break
#     print(i)

try:
    while True:
        print(1)
        break
except Exception as e:
    print(e)
finally:
    print("finally")



