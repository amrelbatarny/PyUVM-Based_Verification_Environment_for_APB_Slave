"""
File   : Registers.py
Author : Amr El Batarny
Brief  : Contains individual register definitions and field configurations
         for the APB slave device.
"""

from pyuvm import uvm_reg, uvm_reg_field, predict_t

class SYS_STATUS_REG(uvm_reg):
    def __init__(self, name="SYS_STATUS_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.SYS_ERR    = uvm_reg_field('SYS_ERR')
        self.INT_EN     = uvm_reg_field('INT_EN')
        self.PWR_GOOD   = uvm_reg_field('PWR_GOOD')
        self.CLK_STAT   = uvm_reg_field('CLK_STAT')

    def build(self):
        self.CLK_STAT.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.PWR_GOOD.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.INT_EN.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.SYS_ERR.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class INT_CTRL_REG(uvm_reg):
    def __init__(self, name="INT_CTRL_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.INT_EN = uvm_reg_field('INT_EN')
        self.PERI_INT_EN = uvm_reg_field('PERI_INT_EN')
        self.TMR_INT_EN = uvm_reg_field('TMR_INT_EN')
        self.EXT_INT_EN = uvm_reg_field('EXT_INT_EN') 
  
    def build(self):
        self.EXT_INT_EN.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.TMR_INT_EN.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.PERI_INT_EN.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.INT_EN.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class DEV_ID_REG(uvm_reg):
    def __init__(self, name="DEV_ID_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.DEV_MFG_ID = uvm_reg_field('DEV_MFG_ID')
        self.DEV_MOD_ID = uvm_reg_field('DEV_MOD_ID')
        self.DEV_REV = uvm_reg_field('DEV_REV')
        self.RESERVED = uvm_reg_field('RESERVED')

    def build(self):
        self.RESERVED.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.DEV_REV.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.DEV_MOD_ID.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.DEV_MFG_ID.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class MEM_CTRL_REG(uvm_reg):
    def __init__(self, name="MEM_CTRL_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.CACHE_EN = uvm_reg_field('CACHE_EN')
        self.MEM_MODE = uvm_reg_field('MEM_MODE')
        self.PRE_FETCH = uvm_reg_field('PRE_FETCH')
        self.ECC_CTRL = uvm_reg_field('ECC_CTRL')

    def build(self):
        self.ECC_CTRL.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.PRE_FETCH.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.MEM_MODE.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.CACHE_EN.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class TEMP_SENSOR_REG(uvm_reg):
    def __init__(self, name="TEMP_SENSOR_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.TEMP_HB = uvm_reg_field('TEMP_HB')
        self.TEMP_LB = uvm_reg_field('TEMP_LB')
        self.OVR_TEMP_WARN = uvm_reg_field('OVR_TEMP_WARN')
        self.UND_TEMP_WARN = uvm_reg_field('UND_TEMP_WARN')

    def build(self):
        self.UND_TEMP_WARN.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.OVR_TEMP_WARN.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.TEMP_LB.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.TEMP_HB.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class ADC_CTRL_REG(uvm_reg):
    def __init__(self, name="ADC_CTRL_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.ADC_START = uvm_reg_field('ADC_START')
        self.ADC_READY = uvm_reg_field('ADC_READY')
        self.ADC_CH_SEL = uvm_reg_field('ADC_CH_SEL')
        self.ADC_REF_SEL = uvm_reg_field('ADC_REF_SEL')

    def build(self):
        self.ADC_REF_SEL.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.ADC_CH_SEL.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.ADC_READY.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.ADC_START.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class DBG_CTRL_REG(uvm_reg):
    def __init__(self, name="DBG_CTRL_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.DBG_EN = uvm_reg_field('DBG_EN')
        self.BRKPT_EN = uvm_reg_field('BRKPT_EN')
        self.WDT_CTRL = uvm_reg_field('WDT_CTRL')
        self.STEP_EN = uvm_reg_field('STEP_EN')

    def build(self):
        self.STEP_EN.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.WDT_CTRL.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.BRKPT_EN.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.DBG_EN.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class GPIO_DATA_REG(uvm_reg):
    def __init__(self, name="GPIO_DATA_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.GPIO_OUT3 = uvm_reg_field('GPIO_OUT3')
        self.GPIO_OUT2 = uvm_reg_field('GPIO_OUT2')
        self.GPIO_OUT1 = uvm_reg_field('GPIO_OUT1')
        self.GPIO_OUT0 = uvm_reg_field('GPIO_OUT0')

    def build(self):
        self.GPIO_OUT0.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.GPIO_OUT1.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.GPIO_OUT2.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.GPIO_OUT3.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class DAC_OUTPUT_REG(uvm_reg):
    def __init__(self, name="DAC_OUTPUT_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.DAC_EN = uvm_reg_field('DAC_EN')
        self.DAC_MODE = uvm_reg_field('DAC_MODE')
        self.DAC_GAIN = uvm_reg_field('DAC_GAIN')
        self.DAC_PWR_MODE = uvm_reg_field('DAC_PWR_MODE')

    def build(self):
        self.DAC_PWR_MODE.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.DAC_GAIN.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.DAC_MODE.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.DAC_EN.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class VOLTAGE_CTRL_REG(uvm_reg):
    def __init__(self, name="VOLTAGE_CTRL_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.VOLTAGE_EN = uvm_reg_field('VOLTAGE_EN')
        self.VOLTAGE_SEL = uvm_reg_field('VOLTAGE_SEL')
        self.VOLTAGE_SET = uvm_reg_field('VOLTAGE_SET')
        self.VOLTAGE_MON = uvm_reg_field('VOLTAGE_MON')
    
    def build(self):
        self.VOLTAGE_MON.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.VOLTAGE_SET.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.VOLTAGE_SEL.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.VOLTAGE_EN.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class CLK_CONFIG_REG(uvm_reg):
    def __init__(self, name="CLK_CONFIG_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.CLK_SRC = uvm_reg_field('CLK_SRC')
        self.CLK_DIV = uvm_reg_field('CLK_DIV')
        self.CLK_EN = uvm_reg_field('CLK_EN')
        self.CLK_RST = uvm_reg_field('CLK_RST')
    
    def build(self):
        self.CLK_RST.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.CLK_EN.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.CLK_DIV.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.CLK_SRC.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class TIMER_COUNT_REG(uvm_reg):
    def __init__(self, name="TIMER_COUNT_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.TIMER_CNT_MSB = uvm_reg_field('TIMER_CNT_MSB')
        self.TIMER_CNT_LSB = uvm_reg_field('TIMER_CNT_LSB')
        self.TIMER_EN = uvm_reg_field('TIMER_EN')
        self.TIMER_MODE = uvm_reg_field('TIMER_MODE')
    
    def build(self):
        self.TIMER_MODE.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.TIMER_EN.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.TIMER_CNT_LSB.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.TIMER_CNT_MSB.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class INPUT_DATA_REG(uvm_reg):
    def __init__(self, name="INPUT_DATA_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.DATA_MSB = uvm_reg_field('DATA_MSB')
        self.DATA_LSB = uvm_reg_field('DATA_LSB')
        self.STATUS = uvm_reg_field('STATUS')
        self.RESERVED = uvm_reg_field('RESERVED')
    
    def build(self):
        self.RESERVED.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.STATUS.configure(
            parent=self, size=8, lsb_pos=8,
            access="RO", reset=0, is_volatile=0
        )

        self.DATA_LSB.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.DATA_MSB.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class OUTPUT_DATA_REG(uvm_reg):
    def __init__(self, name="OUTPUT_DATA_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.DATA_MSB = uvm_reg_field('DATA_MSB')
        self.DATA_LSB = uvm_reg_field('DATA_LSB')
        self.STATUS = uvm_reg_field('STATUS')
        self.RESERVED = uvm_reg_field('RESERVED')
    
    def build(self):
        self.RESERVED.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.STATUS.configure(
            parent=self, size=8, lsb_pos=8,
            access="RO", reset=0, is_volatile=0
        )

        self.DATA_LSB.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.DATA_MSB.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class DMA_CTRL_REG(uvm_reg):
    def __init__(self, name="DMA_CTRL_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.DMA_EN = uvm_reg_field('DMA_EN')
        self.DMA_SRC = uvm_reg_field('DMA_SRC')
        self.DMA_DST = uvm_reg_field('DMA_DST')
        self.DMA_SIZE = uvm_reg_field('DMA_SIZE')
    
    def build(self):
        self.DMA_SIZE.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.DMA_DST.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.DMA_SRC.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.DMA_EN.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)


class SYS_CTRL_REG(uvm_reg):
    def __init__(self, name="SYS_CTRL_REG", reg_width=32):
        super().__init__(name, reg_width)
        self.SYS_RST = uvm_reg_field('SYS_RST')
        self.SYS_PWR = uvm_reg_field('SYS_PWR')
        self.SYS_MODE = uvm_reg_field('SYS_MODE')
        self.SYS_STATUS = uvm_reg_field('SYS_STATUS')
    
    def build(self):
        self.SYS_STATUS.configure(
            parent=self, size=8, lsb_pos=0,
            access='RW', reset=0, is_volatile=0
        )

        self.SYS_MODE.configure(
            parent=self, size=8, lsb_pos=8,
            access='RW', reset=0, is_volatile=0
        )

        self.SYS_PWR.configure(
            parent=self, size=8, lsb_pos=16,
            access='RW', reset=0, is_volatile=0
        )

        self.SYS_RST.configure(
            parent=self, size=8, lsb_pos=24,
            access='RW', reset=0, is_volatile=0
        )

        self._set_lock()
        self.set_prediction(predict_t.PREDICT_DIRECT)
