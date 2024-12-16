# PyUVM-Based Verification Environment for APB Slave Register File

## Overview

This repository contains a complete verification environment for an APB Slave Register File using the PyUVM library. The environment leverages Cocotb and PyUVM for high-level testbench development and includes constrained random verification and coverage using the `cocotb-coverage` library. The design under test (DUT) is described in SystemVerilog and simulates using QuestaSim.

### Features

- **PyUVM-based Components**: Implements UVM-like constructs in Python using PyUVM.
- **Constrained Random Verification**: Leverages the `cocotb-coverage` library for constrained random generation.
- **Coverage Support**: Ensures thorough testing through coverage metrics.
- **Custom APB RAL Model**: (Currently under development; APB RAL tests disabled).
- **Cocotb Integration**: Python-based testing for hardware design simulation.

---

## Directory Structure

```plaintext
├── RAL
│   ├── APB_reg.py
│   ├── APB_reg_adapter.py
│   ├── APB_reg_block.py
│   └── __pycache__
│
├── RTL
│   ├── APB_Slave.sv
│   ├── APB_Wrapper.sv
│   ├── RegisterFile.sv
│   └── shared_pkg.sv
│
└── Testbench
    ├── APB_agent.py
    ├── APB_bfm.py
    ├── APB_driver.py
    ├── APB_env.py
    ├── APB_monitor.py
    ├── APB_sequence.py
    ├── APB_seq_item.py
    ├── APB_test.py
    ├── common_imports.py
    ├── Makefile
    ├── run.sh
    └── setup.tcl
```

---

## Key Components

### Testbench Components

- **APB Sequence Item**: Implements constrained randomization using multiple inheritance from `uvm_sequence_item` and `crv.Randomized`.
- **APB Driver**: Drives stimuli into the DUT by coordinating with the APB BFM.
- **APB Monitor**: Observes and captures transactions on the APB bus.
- **APB Agent**: Wraps the driver, monitor, and sequencer for APB transactions.
- **APB Environment**: Top-level testbench environment integrating the agent and register model (RAL).

### Cocotb-Coverage Library

This library provides:

- Constrained randomization through `crv.Randomized`.
- User-defined constraints and distributions for complex randomization scenarios.
- A Pythonic alternative to SystemVerilog-style constrained random verification.

Example of Constrained Randomization:

```python
class frame_t(crv.Randomized):
    def __init__(self):
        crv.Randomized.__init__(self)
        self.src_port = 0
        self.des_port = 0
        self.add_rand("src_port", list(range(256)))
        self.add_rand("des_port", list(range(256)))

        self.add_constraint(lambda src_port: src_port in range(10))
        self.add_constraint(lambda des_port: des_port not in range(4, 255))
```

For more details on constrained random verification and coverage, refer to the [documentation](https://github.com/mciepluc/cocotb-coverage).

---

## Design Under Test

The DUT includes the following SystemVerilog modules:

- **APB Wrapper**: Top-level wrapper connecting the APB Slave and Register File.
- **APB Slave**: Handles APB protocol transactions.
- **Register File**: A configurable register file for data storage.

---

## Running the Testbench

### Prerequisites

- QuestaSim installed and added to the system PATH.
- Cocotb and PyUVM installed:
  ```bash
  pip install cocotb pyuvm cocotb-coverage
  ```

### Steps to Simulate

1. Clean previous builds and run the simulation using the following command:
   ```bash
   ./run.sh
   ```
   or for bash:
   ```bash
   bash run.sh
   ```
2. Analyze results using the generated waveforms and logs.

---

## Note on Current RAL Model

The Register Abstraction Layer (RAL) is under development. As such, the `APB_reg_test` test is currently disabled. The `@pyuvm.test` decorator is commented out for this test.

---

## Future Work

- Enable and validate RAL-based tests.
- Add more coverage metrics for detailed verification.
- Extend support for additional APB Slave configurations.

---
## Contribution

We welcome contributions to this educational project. Feel free to submit pull requests for improvements or additional features.
---
## Contact

Click on the image below

<a href="https://beacons.ai/amrelbatarny" target="_blank">
  <img align="left" alt="Beacons" width="180px" src="https://www.colormango.com/development/boxshot/beacons-ai_154511.png" />
</a> 
<br>
