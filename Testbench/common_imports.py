# common_imports.py

# General imports
import cocotb
import pyuvm
import logging
import sys
import os
import vsc

# Add the RAL directory to sys.path
directory_path = "../RAL"
sys.path.append(directory_path)

# pyuvm imports
from pyuvm import *
from pyuvm.s24_uvm_reg_includes import *

# cocotb imports
from cocotb.clock import Clock
from cocotb.triggers import *

# CRV imports
from cocotb_coverage.crv import *
from cocotb_coverage.coverage import *
import random

# pytest and cocotb-test imports
import pytest
from cocotb_test import run