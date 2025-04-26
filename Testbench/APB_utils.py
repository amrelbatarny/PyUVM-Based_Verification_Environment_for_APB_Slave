import enum

@enum.unique
class APBType(enum.IntEnum):
	READ = 0
	WRITE = 1