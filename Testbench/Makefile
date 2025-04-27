###############################################################################
# Author : Makefile
# File   : Amr El Batarny
# Brief  : Build script for compiling sv_conduit DPI, SystemVerilog sources,
#          and running cocotb.
###############################################################################

# Force GUI mode and export variables
export COCOTB_RESOLVE_X = ZEROS
GUI = 1
WAVES = 1
SIM ?= questa
TOPLEVEL_LANG ?= verilog

# RTL Files 
VERILOG_SOURCES += APB_seq_item_pkg.sv
VERILOG_SOURCES += ../RTL/shared_pkg.sv ../RTL/APB_Wrapper.sv ../RTL/APB_Slave.sv ../RTL/RegisterFile.sv
VERILOG_SOURCES += dummy_dpi_initializer.sv
VERILOG_SOURCES += APB_SVA.sv SVA_bind.sv

# Top-level and module
TOPLEVEL = APB_Wrapper

# MODULE is the basename of the Python test file
MODULE = Tests

# Compilation arguments
VLOG_ARGS += -mfcu -cuname -timescale=1ns/1ps
VLOG_ARGS += +cover
# VLOG_ARGS += +define+DEBUG_SVCONDUIT

# Use setup.tcl for waveform configuration
VSIM_ARGS += -do setup.tcl
VSIM_ARGS += -dpioutoftheblue 1
VSIM_ARGS += -classdebug
VSIM_ARGS += -coverage
VSIM_ARGS += -cover

# Include Cocotb's Makefile AFTER variable exports
include $(shell cocotb-config --makefiles)/Makefile.sim

# Clean target
.PHONY: clean
clean::
	rm -rf __pycache__ results.xml modelsim.ini transcript vsim.wlf ../RAL/__pycache__

# PyUCIS-Viewer target
.PHONY: pyucis
pyucis::
	pyucis-viewer ../Coverage_Reports/Exported_by_PyVSC/apb_coverage.xml