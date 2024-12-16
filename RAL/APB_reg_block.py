from common_imports import *
from APB_reg import *

class APB_reg_block(uvm_reg_block):
    def __init__(self, name="APB_reg_block"):
        super().__init__(name)
        self.def_map = uvm_reg_map('map')
        self.def_map.configure(self, 0)
        
        self.reg_SYS_STATUS_REG = SYS_STATUS_REG('reg_SYS_STATUS_REG')
        self.reg_SYS_STATUS_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_SYS_STATUS_REG, "0x00000000", "RW")
        
        self.reg_INT_CTRL_REG = INT_CTRL_REG('reg_INT_CTRL_REG')
        self.reg_INT_CTRL_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_INT_CTRL_REG, "0x00000004", "RW")
        
        self.reg_DEV_ID_REG = DEV_ID_REG('reg_DEV_ID_REG')
        self.reg_DEV_ID_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_DEV_ID_REG, "0x00000008", "RW")

        self.reg_MEM_CTRL_REG = MEM_CTRL_REG('reg_MEM_CTRL_REG')
        self.reg_MEM_CTRL_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_MEM_CTRL_REG, "0x0000000C", "RW")

        self.reg_TEMP_SENSOR_REG = TEMP_SENSOR_REG('reg_TEMP_SENSOR_REG')
        self.reg_TEMP_SENSOR_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_TEMP_SENSOR_REG, "0x00000010", "RW")

        self.reg_ADC_CTRL_REG = ADC_CTRL_REG('reg_ADC_CTRL_REG')
        self.reg_ADC_CTRL_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_ADC_CTRL_REG, "0x00000014", "RW")

        self.reg_DBG_CTRL_REG = DBG_CTRL_REG('reg_DBG_CTRL_REG')
        self.reg_DBG_CTRL_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_DBG_CTRL_REG, "0x00000018", "RW")

        self.reg_GPIO_DATA_REG = GPIO_DATA_REG('reg_GPIO_DATA_REG')
        self.reg_GPIO_DATA_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_GPIO_DATA_REG, "0x0000001C", "RW")
        
        self.reg_DAC_OUTPUT_REG = DAC_OUTPUT_REG('reg_DAC_OUTPUT_REG')
        self.reg_DAC_OUTPUT_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_DAC_OUTPUT_REG, "0x00000020", "RW")
        
        self.reg_VOLTAGE_CTRL_REG = VOLTAGE_CTRL_REG('reg_VOLTAGE_CTRL_REG')
        self.reg_VOLTAGE_CTRL_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_VOLTAGE_CTRL_REG, "0x00000024", "RW")

        self.reg_CLK_CONFIG_REG = CLK_CONFIG_REG('reg_CLK_CONFIG_REG')
        self.reg_CLK_CONFIG_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_CLK_CONFIG_REG, "0x00000028", "RW")

        self.reg_TIMER_COUNT_REG = TIMER_COUNT_REG('reg_TIMER_COUNT_REG')
        self.reg_TIMER_COUNT_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_TIMER_COUNT_REG,  "0x0000002C", "RW")

        self.reg_INPUT_DATA_REG = INPUT_DATA_REG('reg_INPUT_DATA_REG')
        self.reg_INPUT_DATA_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_INPUT_DATA_REG, "0x00000030", "RW")

        self.reg_OUTPUT_DATA_REG = OUTPUT_DATA_REG('reg_OUTPUT_DATA_REG')
        self.reg_OUTPUT_DATA_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_OUTPUT_DATA_REG,  "0x00000034", "RW")

        self.reg_DMA_CTRL_REG = DMA_CTRL_REG('reg_DMA_CTRL_REG')
        self.reg_DMA_CTRL_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_DMA_CTRL_REG, "0x00000038", "RW")

        self.reg_SYS_CTRL_REG = SYS_CTRL_REG('reg_SYS_CTRL_REG')
        self.reg_SYS_CTRL_REG.configure(self, "0x0", "", False, False)
        self.def_map.add_reg(self.reg_SYS_CTRL_REG, "0x0000003C", "RW")