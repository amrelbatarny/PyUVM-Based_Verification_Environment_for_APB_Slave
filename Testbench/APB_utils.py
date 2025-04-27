"""
File   : APB_utils.py
Author : Amr El Batarny
Brief  : Defines the APBType enumeration and related utility functions for APB transactions.
"""

import enum

@enum.unique
class APBType(enum.IntEnum):
	READ = 0
	WRITE = 1