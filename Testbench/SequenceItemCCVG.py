"""
Author : Amr El Batarny
File   : SequenceItemCov.py
Brief  : Defines the APB sequence item using cocotb-coverage's CRV (crv.Randomized),
		 with functional‐coverage hooks disabled here (focus on randomization).
"""
import cocotb
from pyuvm import uvm_sequence_item
from cocotb_coverage.crv import Randomized
import random
from APB_utils import APBType

class ApbSeqItemCCVG(uvm_sequence_item, Randomized):
	"""
	Cocotb-coverage CRV version of the APB sequence item.
	Fields:
	  - type   : APBType enum (READ or WRITE)
	  - addr   : 32-bit address, aligned on 4B, [0x00–0x3C]
	  - data   : 32-bit data
	  - strobe : 4-bit byte-enable mask
	"""

	# --- Complex piecewise constraint on data ---
	def complex_c(data, tmp, sq, root):
		A, B = 0x1000, 0x8000
		# Branch 1
		if data < A and data == (3*tmp + 5):
			return 1
		# Branch 2
		elif data < B and (sq*sq - 7 == data) and (root*root == data + 7):
			return 1
		# Branch 3
		elif data >= B and (data % 12345) == 0:
			return 1
		# all other combinations disallowed
		return 0

	def __init__(self, name="ApbSeqItemCov"):
		super().__init__(name)
		Randomized.__init__(self)     

		# Pre-declare every member, even if its value will be randomized
		self.type   = None
		self.addr   = None
		self.strobe = None
		self.data   = None
		self.tmp    = None
		self.sq     = None
		self.root   = None

		# stype: either READ or WRITE
		self.add_rand("type", domain=list(APBType))
		# addr: 0x0,4,8,…,0x3C
		aligned_addrs = list(range(0x00, 0x40, 4))
		self.add_rand("addr", domain=aligned_addrs)
		# data: 32-bit, use Python’s random module instead
		self.data  = random.randint(0, (1 << cocotb.top.PWDATA.value.n_bits) - 1)

		# strobe: 4-bit
		self.add_rand("strobe", domain=list(range(0, 2**4)))

		# Auxiliary vars for piecewise constraint
		# self.add_rand("tmp",  domain=list(range(0, 2**29)))
		# self.add_rand("sq",   domain=list(range(0, 2**16)))
		# self.add_rand("root", domain=list(range(0, 2**32)))

		# Define the weighted‐distribution function
		def strobe_dist(strobe):
			# [1:5]:/10 → total weight 10 ÷ 5 values = 2 per value
			if 1 <= strobe <= 5:
				return 10 / (5 - 1 + 1)
			# [6:10]:/20 → total weight 20 ÷ 5 values = 4 per value
			elif 6 <= strobe <= 10:
				return 20 / (10 - 6 + 1)
			# [11:14]:/70 → total weight 70 ÷ 4 values = 17.5 per value
			elif 11 <= strobe <= 14:
				return 70 / (14 - 11 + 1)
			# 15:/90 → weight 90 on strobe==15
			elif strobe == 15:
				return 90
			# Any other value gets zero weight (optional)
			else:
				return 0


		# Register the constraints
		self.add_constraint(strobe_dist)
		# self.add_constraint(self.complex_c) # cocotb-coverage can’t handle a full 32-bit domain (memory error), so commented the complex_c
		
	def post_randomize(self):
		# pick a full 32-bit unsigned integer
		self.data = random.randint(0, 2**32 - 1)

	# Override do_copy() to perform deep copying
	def do_copy(self, rhs):
		super().do_copy(rhs)
		self.addr   = rhs.addr
		self.data   = rhs.data
		self.strobe = rhs.strobe
		self.type   = rhs.type

	def __str__(self):
		return (
			f"\nName:   {self.get_full_name()}"
			f"\nADDR:   {self.addr}"
			f"\nDATA:   {self.data}"
			f"\nSTROBE: {self.strobe}"
			f"\nTYPE:   {self.type.name}"
		)

