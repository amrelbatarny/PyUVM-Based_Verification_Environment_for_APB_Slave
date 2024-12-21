from common_imports import *
from APB_seq_item import *

class APB_coverage(uvm_component):
    def build_phase(self):
        self.cov_fifo = uvm_tlm_analysis_fifo("cov_fifo", self)
        self.cov_get_port = uvm_get_port("cov_get_port", self)
        self.cov_export = self.cov_fifo.analysis_export

    def connect_phase(self):
        self.cov_get_port.connect(self.cov_fifo.get_export)

    @CoverPoint(
        "APB.PADDR",
        vname="PADDR",
        xf=lambda PADDR, PWRITE: PADDR,
        bins=[x for x in range(0x3C + 1) if x % 4 == 0]
    )

    @CoverPoint(
        "APB.PWRITE",
        vname="PADDR",
        xf=lambda PADDR, PWRITE: PWRITE,
        bins=[0, 1]
    )

    def sample_coverage(self, PADDR, PWRITE):
        """Function to sample coverage."""
        pass

    async def run_phase(self):
        while True:
            await RisingEdge(cocotb.top.PCLK)
            try:
                # Wait for an item from the FIFO
                item = await self.cov_get_port.get()

                # Extract and convert attributes
                PADDR = int(getattr(item, "PADDR", 0))
                PWRITE = int(getattr(item, "PWRITE", 0))

                # Log sampling details
                self.logger.info(f"Sampling coverage: PADDR={PADDR}, PWRITE={PWRITE}")

                # Perform coverage sampling
                self.sample_coverage(PADDR, PWRITE)

            except Exception as e:
                self.logger.error(f"Error during coverage sampling: {e}")

    def report_phase(self):
        # Define the desired export path
        export_path = "../Reports"

        # Make sure the directory exists, if not create it
        os.makedirs(export_path, exist_ok=True)

        # print coverage report
        coverage_db.report_coverage(self.logger.info, bins=False)

        # Export to XML and YAML at the specified path
        coverage_db.export_to_xml(filename=os.path.join(export_path, "coverage_apb.xml"))
        coverage_db.export_to_yaml(filename=os.path.join(export_path, "coverage_apb.yml"))