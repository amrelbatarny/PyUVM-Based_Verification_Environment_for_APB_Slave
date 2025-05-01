###############################################################################
# Author : Makefile
# File   : Amr El Batarny
# Brief  : Build script for compiling sv_conduit DPI, SystemVerilog sources,
#          and running cocotb.
###############################################################################

# Resolve unknown bits (X/Z) as zeros in cocotb
# use ':=' and no spaces around '=' for Makefile export :contentReference[oaicite:1]{index=1}
export COCOTB_RESOLVE_X = ZEROS

# Path to QuestaSim’s UCIS library for coverage database generation
# Users should update this to their local QuestaSim installation
UCIS_LIB_PATH ?= /home/amrelbatarny/QuestaSim/questasim/linux_x86_64/libucis.so

# ensure UCIS_LIB_PATH is visible to all recipe commands :contentReference[oaicite:0]{index=0}
export UCIS_LIB_PATH      


# Force GUI mode and export variables
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