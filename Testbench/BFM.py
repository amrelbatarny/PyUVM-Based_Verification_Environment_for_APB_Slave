import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge
from pyuvm import utility_classes

class ApbBfm(metaclass=utility_classes.Singleton):
	def __init__(self):
		self.dut = cocotb.top
		
	# Clock generation
	async def generate_clock(self):
		c = Clock(cocotb.top.PCLK, 2, 'ns')
		await cocotb.start(c.start())

	async def reset(self):
		self.dut.PRESETn.value  = 0			# Assert reset
		self.dut.PENABLE.value  = 0
		self.dut.PADDR.value    = 0
		self.dut.PWDATA.value   = 0
		self.dut.PWRITE.value   = 0
		self.dut.PSTRB.value    = 0
		await FallingEdge(self.dut.PCLK)	# Hold reset for some cycles
		self.dut.PRESETn.value  = 1			# Deassert reset

	async def write(self, addr, data):
		self.dut.PADDR.value	= addr
		self.dut.PWDATA.value	= data
		self.dut.PWRITE.value	= 1
		self.dut.PSELx.value	= 1
		self.dut.PSTRB.value	= 15
		await RisingEdge(self.dut.PCLK)
		self.dut.PENABLE.value	= 1
		await RisingEdge(self.dut.PREADY)
		self.dut.PSELx.value	= 0
		self.dut.PENABLE.value	= 0

	async def read(self, addr):
		self.dut.PADDR.value	= addr
		self.dut.PWRITE.value	= 0
		self.dut.PSELx.value	= 1
		await RisingEdge(self.dut.PCLK)
		self.dut.PENABLE.value	= 1
		await RisingEdge(self.dut.PCLK)
		self.dut.PSELx.value	= 0
		self.dut.PENABLE.value	= 0
		return self.dut.PRDATA.value