#!/bin/bash

# Clean previous simulation files
echo "Cleaning previous simulation files..."
rm -rf __pycache__ modelsim.ini transcript vsim.wlf sim_build

# Run make to build the simulation
echo "Running Makefile..."
make