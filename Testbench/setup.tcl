# ----------------------------------------------------------------------------
# Author : Amr El Batarny
# File   : setup.tcl
# Brief  : QuestaSim waveform and simulation setup commands.
# ----------------------------------------------------------------------------

# APB Signals Waveforms
add wave -position insertpoint  \
sim:/APB_Wrapper/PCLK \
sim:/APB_Wrapper/PRESETn \
sim:/APB_Wrapper/PADDR \
sim:/APB_Wrapper/PWRITE \
sim:/APB_Wrapper/PWDATA \
sim:/APB_Wrapper/PENABLE \
sim:/APB_Wrapper/PSELx  \
sim:/APB_Wrapper/PSTRB \
sim:/APB_Wrapper/PRDATA \
sim:/APB_Wrapper/PREADY \
sim:/APB_Wrapper/RegisterFile_inst/write_en \
sim:/APB_Wrapper/RegisterFile_inst/read_en \
sim:/APB_Wrapper/RegisterFile_inst/addr \
sim:/APB_Wrapper/RegisterFile_inst/wdata \
sim:/APB_Wrapper/RegisterFile_inst/rdata \
sim:/APB_Wrapper/RegisterFile_inst/byte_strobe \
sim:/APB_Wrapper/RegisterFile_inst/mask

# Current and Next States Waveforms
add wave -position insertpoint  \
-color cyan sim:/APB_Wrapper/APB_Slave_inst/next_state \
-color cyan sim:/APB_Wrapper/APB_Slave_inst/current_state

# Assertions
add wave -position insertpoint \
sim:/APB_Wrapper/APB_SVA_inst/ASSERT_PREADY_ACCESS \
sim:/APB_Wrapper/APB_SVA_inst/ASSERT_ADDR_STABLE \
sim:/APB_Wrapper/APB_SVA_inst/ASSERT_CTRL_DATA_STABLE \
sim:/APB_Wrapper/APB_SVA_inst/ASSERT_SINGLE_CYCLE_READY \

# Registers Waveform
add wave -position insertpoint  \
-color gold sim:/APB_Wrapper/RegisterFile_inst/SYS_STATUS_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/INT_CTRL_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/DEV_ID_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/MEM_CTRL_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/TEMP_SENSOR_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/ADC_CTRL_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/DBG_CTRL_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/GPIO_DATA_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/DAC_OUTPUT_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/VOLTAGE_CTRL_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/CLK_CONFIG_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/TIMER_COUNT_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/INPUT_DATA_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/OUTPUT_DATA_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/DMA_CTRL_REG \
-color gold sim:/APB_Wrapper/RegisterFile_inst/SYS_CTRL_REG

.vcop Action toggleleafnames

# Saving coverage database in UCDB file for PyVSC
# coverage save -onexit ../Coverage_Reports/Exported_by_PyVSC/apb_coverage.ucdb

# Saving coverage database in UCDB file for PyQuesta
coverage save -onexit ../Coverage_Reports/Exported_by_PyQuesta/apb_coverage.ucdb

run -all

# quit -sim

# ====================== PyVSC collected coverage ======================

# Generate a TXT Coverage Report
# vcover report ../Coverage_Reports/Exported_by_PyVSC/apb_coverage.ucdb -details -annotate -all -output ../Coverage_Reports/Exported_by_PyVSC/coverage_report.txt

# Generate an HTML Coverage Report
# vcover report -html -output ../Coverage_Reports/Exported_by_PyVSC/coverage_report_by_questasim -details -annotate ../Coverage_Reports/Exported_by_PyVSC/apb_coverage.ucdb


# ===================== PyQuesta collected coverage =====================

# Generate a TXT Coverage Report
# vcover report ../Coverage_Reports/Exported_by_PyQuesta/apb_coverage.ucdb -details -annotate -all -output ../Coverage_Reports/Exported_by_PyQuesta/coverage_report.txt

# Generate an HTML Coverage Report
# vcover report -html -output ../Coverage_Reports/Exported_by_PyQuesta/coverage_report_by_questasim -details -annotate ../Coverage_Reports/Exported_by_PyQuesta/apb_coverage.ucdb