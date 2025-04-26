import vsc
from vsc import (
	covergroup,
	uint32_t,
	bit_t,
	enum_t,
	coverpoint,
	cross,
	bin as vsc_bin,
	report_coverage,
	write_coverage_db,
)
from pyuvm import (
	uvm_subscriber,
	uvm_tlm_analysis_fifo,
	uvm_get_port,
)
from APB_utils import APBType # your APBType enum

@vsc.covergroup
class ApbCoverGroup(object):
	def __init__(self):
		self.with_sample(
			addr=vsc.uint32_t(),
			data=vsc.uint32_t(),
			strobe=vsc.bit_t(4),
			type=vsc.enum_t(APBType)
		)

		# Transfer type coverage
		self.cp_pwrite = vsc.coverpoint(self.type, bins=dict(
			read=vsc.bin(APBType.READ),
			write=vsc.bin(APBType.WRITE)
		))

		# Address coverage - 16 possible addresses (0x0 to 0x3C in steps of 4)
		addr_values = [i*4 for i in range(16)]
		self.cp_paddr = vsc.coverpoint(self.addr, bins=dict(
			[(f"address_{hex(address)}", vsc.bin(address)) for address in addr_values]
		))

		# Write data coverage (corrected range specification)
		self.cp_pwdata = vsc.coverpoint(self.data, bins=dict(
			zero=vsc.bin(0),
			all_ones=vsc.bin(0xFFFFFFFF)
		))

		# Cross coverage between key signals
		self.cross_rw_addr  = vsc.cross([self.cp_pwrite, self.cp_paddr])
		self.cross_rw_wdata = vsc.cross([self.cp_pwrite, self.cp_pwdata])

class ApbCoverage(uvm_subscriber):
	def build_phase(self):
		# self.cov_fifo = uvm_tlm_analysis_fifo("cov_fifo", self)
		# self.cov_get_port = uvm_get_port("cov_get_port", self)
		# self.cov_export = self.cov_fifo.analysis_export
		self.cg = ApbCoverGroup()

	# def connect_phase(self):
	# 	self.cov_get_port.connect(self.cov_fifo.get_export)

	def write(self, item):
		self.cg.sample(
					item.addr,
					item.data,
					item.strobe,
					item.type
				)
		self.logger.debug(f"{self.get_type_name()}: SAMPLED {item}")
		self.logger.debug(f"Instance Coverage = {self.cg.get_inst_coverage()}")

	# async def run_phase(self):
	#     while True:
	#         try:
	#             item = await self.cov_get_port.get()
	#             self.cg.sample(
	#                 item.addr,
	#                 item.data,
	#                 item.strobe,
	#                 item.type
	#             )
	#             self.logger.debug(f"{self.get_type_name()}: SAMPLED {item}")
	#             self.logger.debug(f"Instance Coverage = {self.cg.get_inst_coverage()}")
	#         except Exception as e:
	#             pass

	def report_phase(self):
		self.logger.info("cg total coverage=%f" % (self.cg.get_coverage()))
		vsc.report_coverage(details=False)
		vsc.write_coverage_db(filename="../Coverage_Reports/Exported_by_PyVSC/apb_coverage.xml",  fmt='xml',      libucis=None)
		vsc.write_coverage_db(filename="../Coverage_Reports/Exported_by_PyVSC/apb_coverage.ucdb", fmt='libucis',  libucis="/home/amrelbatarny/QuestaSim/questasim/linux_x86_64/libucis.so")