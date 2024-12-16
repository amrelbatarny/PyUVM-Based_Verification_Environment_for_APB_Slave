from common_imports import *
logger = logging.getLogger("coroutines")
logging.basicConfig(level=logging.NOTSET)
logger.setLevel(logging.INFO)

class APB_bfm(metaclass=utility_classes.Singleton):
    def __init__(self):
        self.dut = cocotb.top
        
    async def reset(self):
        # logger.info("Entered the bfm reset method")
        self.dut.PRESETn.value  = 0        # Assert reset
        self.dut.PENABLE.value  = 0
        self.dut.PADDR.value    = 0
        self.dut.PWDATA.value   = 0
        self.dut.PWRITE.value   = 0
        await FallingEdge(self.dut.PCLK)   # Hold reset for some cycles
        self.dut.PRESETn.value  = 1        # Deassert reset

    async def idle(self):
        await RisingEdge(self.dut.PCLK)
        self.dut.PENABLE.value  =   0
        while (self.dut.PREADY.value == 1):
            await RisingEdge(self.dut.PCLK)

    async def prepare_data(self, item):
        self.dut.PWDATA.value   = item.PWDATA
        self.dut.PWRITE.value   = int(item.PWRITE)
        self.dut.PADDR.value    = item.PADDR
        await RisingEdge(self.dut.PCLK)

    async def setup(self, item):
        self.dut.PENABLE.value  = int(item.PENABLE)
        await RisingEdge(self.dut.PCLK)
        while self.dut.PENABLE.value and self.dut.PREADY.value == 0:
            await RisingEdge(self.dut.PCLK)

    async def access(self):
        while (self.dut.PREADY.value == 1):
            await RisingEdge(self.dut.PCLK)