## Python-based Verification Environment for APB Slave

This repository provides a fully Python-centric verification environment for an APB Slave design, leveraging Cocotb, PyUVM, PyVSC, constrainedrandom, cocotb-coverage and PyQuesta to combine the best of both worlds: Python's productivity and SystemVerilog's mature CRV and coverage engines.

---

## Table of Contents

1. [Introduction](#introduction)
2. [UVM Structure](#uvm-structure)
3. [Key Features](#key-features)
4. [RTL Overview](#rtl-overview)
5. [Directory Structure](#directory-structure)
6. [Installation & Setup](#installation--setup)
7. [Test Configuration](#test-configuration)
8. [Simulation Flow (Makefile)](#simulation-flow-makefile)
9. [Python Testbench Architecture](#python-testbench-architecture)
10. [Register Abstraction Layer (RAL)](#register-abstraction-layer-ral)
11. [Coverage Strategy](#coverage-strategy)
12. [Randomization Strategy](#randomization-strategy)
13. [Trade-offs: SV vs. Python Testbenches](#trade-offs-sv-vs-python-testbenches)
14. [Future Migration Possibilities](#future-migration-possibilities)
15. [Running the Tests](#running-the-tests)
16. [Contributing](#contributing)
17. [License](#license)
18. [Contact](#contact)

---

## Introduction

As Python gains momentum in functional verification, it still lacks some of SystemVerilog’s mature features for constrained random and coverage-driven methodologies. This project demonstrates a hybrid approach where a standard APB Slave in SystemVerilog is verified entirely from Python using:

* **Cocotb + PyUVM** for testbench structure and orchestration.
* **PyVSC**, **constrainedrandom** and **cocotb-coverage** for native Python constrained-random verification (CRV) and functional coverage.
* **PyQuesta** (SVConduit) to invoke SystemVerilog’s randomization (`sv_get`) and coverage (`sv_put`) engines via DPI.
* **Python RAL** for front-door register read/write operations.

---

## UVM Structure

![UVM Structure](Documentation/RAL-UVM_Structure_NoBG.png)
---

## Key Features

* **Hybrid CRV & Coverage** via multiple methods:

  * **PyVSC**: pure-Python randomization and coverage.
  * **constrainedrandom**
  * **cocotb-coverage**
  * **PyQuesta**: borrow SystemVerilog’s EDA solver and coverage via DPI.
* **PyUVM Factory & Sequences** for modular, reusable stimulus.
* **SVConduit DPI Shim** auto-built to connect Python and SystemVerilog.
* **ConfigDB-based Test Configuration** to toggle features at runtime.
* **README-driven Documentation** with examples and guidelines.

---
## RTL Overview

The RTL implements an APB slave device with standard AMBA APB interface signals, internal register file, and optional assertion checking (SVA). The RTL modules include:

- **APB_Slave.sv**: Implements core APB protocol handling (PREADY, PRDATA, PENABLE, etc.).
- **RegisterFile.sv**: Memory-mapped register bank for addressable data storage.
- **APB_Wrapper.sv**: Top module connecting slave, register file, and dummy DPI hooks.
- **APB_SVA.sv** and **SVA_bind.sv**: SystemVerilog Assertions verifying APB protocol compliance.

Assertions ensure correct timing and sequencing of APB transactions, strengthening functional correctness.

The RTL is kept lightweight and simple to allow a full Python-based verification flow to focus on CRV, coverage, and RAL interaction without unnecessary complexity.

![RTL Diagram](Documentation/APB_Wrapper.png)
---

## Directory Structure

```text
├── Coverage_Reports/            # Coverage outputs (cocotb, PyVSC, PyQuesta)
├── Documentation/               # Architecture and RTL diagrams
├── RAL/                         # Python Register Abstraction Layer
├── RTL/                         # APB Slave RTL and SVA
└── Testbench/                   # Python testbench sources
    ├── Agent.py
    ├── APB_seq_item_pkg.sv     # SVConduit-generated package
    ├── APB_seq_itemMod.py      # SVConduit-generated Python class
    ├── SequenceItem*.py        # Various sequence item definitions
    ├── SequenceLibrary.py      # PyUVM sequence definitions
    ├── Coverage.py             # PyVSC coverage collector
    ├── Driver.py               # UVM driver implementation
    ├── Monitor.py              # UVM monitor with dual coverage paths
    ├── Scoreboard.py           # RAL-based scoreboard
    ├── Tests.py                # @pyuvm.test definitions
    ├── Makefile                # Simulation orchestration
    └── setup.tcl               # Waveform & coverage setup
```

---

## Installation & Setup

1. **Prerequisites**

   * Python 3.6+ with `pip`
   * Mentor QuestaSim (for DPI build and SV coverage)
   * A system license for QuestaSim

2. **Clone & Create Virtual Environment**

   ```bash
   git clone https://github.com/amrelbatarny/Python-based_Verification_Environment_for_APB_Slave.git
   cd Python-based_Verification_Environment_for_APB_Slave
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python Packages**

   ```bash
   pip install cocotb pyuvm pyvsc pyquesta constrainedrandom
   ```

4. **Build the DPI Shim**
   Before running the testbench you must:

   ```bash
   export QUESTA_HOME=/path/to/QuestaSim
   cd venv/lib/python3.9/site-packages/pyquesta/makefiles
   make -f pyquesta.mk
   ```

   This produces `sv_conduit.so`. Ensure `QUESTA_HOME` is correctly set.

---

## Test Configuration

---

Configuration Parameters (via ConfigDB)

| Parameter                   | Type | Description                                                                                                                                                              | Default |
| --------------------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------- |
| `NUM_TRANSACTIONS`          | int  | Number of APB transactions each sequence should generate.                                                                                                                | 300     |
| `ENABLE_SV_RANDOMIZATION`   | bool | If True, all sequences bypass Python-side randomization and call `SVConduit.get()` to retrieve randomized items from SystemVerilog. Overrides other randomization flags. | False   |
| `ENABLE_VSC_RANDOMIZATION`  | bool | If True (and all other randomization flags False), sequences use PyVSC’s `randomize()` on `ApbSeqItemVSC`.                                                               | False   |
| `ENABLE_CR_RANDOMIZATION`   | bool | If True (and all other randomization flags False), sequences use constrainedrandom on `ApbSeqItemCR`.                                                                    | False   |
| `ENABLE_CCVG_RANDOMIZATION` | bool | If True (and all other randomization flags False), sequences use cocotb-coverage CRV on `ApbSeqItemCCVG`.                                                                | False   |
| `ENABLE_SV_COVERAGE`        | bool | If True, the monitor invokes `SVConduit.put()` to sample coverage in SystemVerilog (`sv_put`). The PyVSC coverage subscriber is not instantiated.                        | False   |
| `ENABLE_VSC_COVERAGE`       | bool | If True (and `ENABLE_SV_COVERAGE` False), the PyVSC-based coverage subscriber (`ApbCoverage`) is instantiated and receives transactions via the analysis port.           | True    |

**Notes:**

* Exactly one randomization mode flag (`ENABLE_SV_RANDOMIZATION`, `ENABLE_VSC_RANDOMIZATION`, `ENABLE_CR_RANDOMIZATION`, or `ENABLE_CCVG_RANDOMIZATION`) must be True.
* Coverage flags are independent: enable either SV or VSC coverage, but not both.
* To set these, in your test class:

```python
# Test Configuration (You can read the descriptions in the top for details)
ConfigDB().set(None, "*", "NUM_TRANSACTIONS", 5)
ConfigDB().set(None, "*", "ENABLE_SV_RANDOMIZATION", False)
ConfigDB().set(None, "*", "ENABLE_VSC_RANDOMIZATION", False)
ConfigDB().set(None, "*", "ENABLE_CR_RANDOMIZATION", True)
ConfigDB().set(None, "*", "ENABLE_CCVG_RANDOMIZATION", False)
ConfigDB().set(None, "*", "ENABLE_SV_COVERAGE", False)
ConfigDB().set(None, "*", "ENABLE_VSC_COVERAGE", False)
```

---

## Simulation Flow (Makefile)

The top-level `Makefile` automates compilation and execution of the RTL and Python testbench. After setting up, simply run:

```bash
make clean && make
```
---

## Python Testbench Architecture

* **BFM**: Clock & low-level APB signal driver (`BFM.py`).
* **Agent**: Instantiates Driver and Monitor, connects to sequencer (`Agent.py`).
* **Driver**: Converts UVM items to APB signals and performs RAL predict (`Driver.py`).
* **Monitor**: Samples bus, writes to:

  * PyVSC coverage via `self.cvg.sample(...)`
  * SV coverage via `SVConduit.put(item)` (if `ENABLE_SV_COVERAGE`)
* **Scoreboard**: Reads back RAL-model mirrored values, compares with DUT reads (`Scoreboard.py`).

---

## Register Abstraction Layer (RAL)

Located in `RAL/`, this layer defines:

* **Registers.py**: Field definitions and bit-widths.
* **RegisterBlock.py**: Collection of registers and address maps.
* **Adapter.py**: Translates register reads/writes into APB BFM calls.

`ApbRegSequence` uses RAL for front-door accesses via methods like `.write()` and `.read()`.

---

## Coverage Strategy

We support three active coverage backends; one is selected via ConfigDB flags:

1. **PyVSC Coverage** (`Coverage.py`):

   * Implements Python covergroups sampling `ApbSeqItemVSC` fields.
   * Invoked in Monitor when `ENABLE_VSC_COVERAGE` is True.
   * Export via `vsc.write_coverage_db()` to XML or UCDB.

2. **PyQuesta Coverage** (`sv_put` in `APB_seq_item.svh`):

   * Monitor calls `SVConduit.put(item)` to invoke SystemVerilog's `sv_put()`.
   * SV-side covergroup `APB_cg` samples fields, leveraging QuestaSim’s native UCIS engine.

> **Note:** Coverage flags are mutually exclusive: select either `ENABLE_SV_COVERAGE` or `ENABLE_VSC_COVERAGE`.

---
## Randomization Strategy
We support **four** randomization backends; only one may be active via ConfigDB flags:

1. **PyVSC** (`SequenceItemVSC.py`):

   * Uses `@vsc.randobj` and `@vsc.constraint` annotations on `ApbSeqItemVSC`.
   * Sequences call `.randomize()` or `with randomize_with(): dist { … }`.

2. **Constrainedrandom** (`SequenceItemCR.py`):

   * Uses the `constrainedrandom` library to declare random variables and constraints on `ApbSeqItemCR`.
   * Supports complex piecewise and post-randomization sampling (e.g. triangular distributions).

3. **cocotb-coverage CRV** (`SequenceItemCCVG.py`):

   * Defines random variables and constraints via the `cocotb-coverage` API on `ApbSeqItemCCVG`.
   * Sequences invoke this item when `ENABLE_CCVG_RANDOMIZATION` is set.

4. **PyQuesta (SVConduit)** (`APB_seq_item_pkg.sv` + `APB_seq_itemMod.py`):

   * Calls `SVConduit.get(APB_seq_item)` to invoke SystemVerilog’s `sv_get()`.
   * SV randomizes via `obj.randomize() with { … }` and serializes back to Python.

> **Note:** Exactly one of `ENABLE_VSC_RANDOMIZATION`, `ENABLE_CR_RANDOMIZATION`, `ENABLE_CCVG_RANDOMIZATION`, or `ENABLE_SV_RANDOMIZATION` must be `True`.
---
## SV vs. Python Testbenches

* **Python**: fast development, huge ecosystems (ML, data), dynamic typing, but slower sim (VPI/DPI), limited built-in assertions.
* **SV**: high performance, rich CRV/coverage/assertions, full waveform visibility, but verbose and steeper learning curve.
* **PyQuesta**: bridges by letting Python drive SV engines via DPI, requiring only minimal SV code.

---

## Future Migration Possibilities

* **Native Python support** in EDA kernels (removing VPI overhead).
* Growing Python CRV/coverage libraries (PyVSC, constrainedrandom, cocotb-coverage).
* AI/ML-driven testbench enhancements.
* Challenges include debug visibility and formal integration.

---

## Running the Tests

```bash
make clean && make
```

Upon completion, coverage reports appear in `Coverage_Reports/`:

* `Exported_by_cocotb-coverage/`
* `Exported_by_PyVSC/`
* `Exported_by_PyQuesta/`

---

## Contributing

Contributions, bug reports, and feature requests are welcome! Please open an issue or pull request on GitHub.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Contact

Click on the image below

<a href="https://beacons.ai/amrelbatarny" target="_blank">
  <img align="left" alt="Beacons" width="180px" src="https://www.colormango.com/development/boxshot/beacons-ai_154511.png" />
</a> 
<br>
