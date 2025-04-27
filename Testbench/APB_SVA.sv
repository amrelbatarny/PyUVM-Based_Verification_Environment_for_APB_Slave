module APB_SVA #(
	 parameter DATA_WIDTH = 32,
	 parameter ADDR_WIDTH = 32,
	 parameter NBYTES  = DATA_WIDTH/8
	)(
	// Global Signals
	input wire									PCLK,
	input wire									PRESETn,

	// APB Signals
	input wire									PSELx,
	input wire [ADDR_WIDTH-1:0]	PADDR,
	input wire									PWRITE,
	input wire [NBYTES-1:0]			PSTRB,
	input wire [DATA_WIDTH-1:0]	PWDATA,
	input wire									PENABLE,
	input wire [DATA_WIDTH-1:0]	PRDATA,
	input wire									PREADY
	);

// Define the SETUP phase: PSELx asserted while PENABLE and PREADY are deasserted
sequence setup_phase_s;
  PSELx        &&
  !PENABLE     &&
  !PREADY;
endsequence

// Define the ACCESS phase: PSELx, PENABLE, and PREADY all asserted
sequence access_phase_s;
  PSELx     &&
  PENABLE   &&
  PREADY;
endsequence

//////////////////////////////////////////////////////////////////////////////
// 1. Protocol Handshake Properties
//////////////////////////////////////////////////////////////////////////////

// 1.1 Every SETUP must be followed exactly one cycle later by an ACCESS
property p_apb_transfer;
  @(posedge PCLK) disable iff(!PRESETn)
    setup_phase_s |=> ##1 access_phase_s;
endproperty
assert property (p_apb_transfer)
  else $error("APB transfer protocol violated: ACCESS not seen one cycle after SETUP");

// 1.2 PREADY must only be asserted during ACCESS, and deasserted otherwise
property p_pready_idle;
  @(posedge PCLK) disable iff(!PRESETn)
    (!PSELx || !PENABLE) |-> !PREADY;
endproperty
assert property (p_pready_idle)
  else $error("PREADY asserted outside ACCESS phase");

property p_pready_access;
  @(posedge PCLK) disable iff(!PRESETn)
    access_phase_s |-> PREADY;
endproperty
assert property (p_pready_access)
  else $error("PREADY not asserted during ACCESS phase");

//////////////////////////////////////////////////////////////////////////////
// 2. Signal Stability Properties
//////////////////////////////////////////////////////////////////////////////

// 2.1 Address stability: PADDR must remain stable during ACCESS
property p_addr_stable;
  @(posedge PCLK) disable iff(!PRESETn)
    setup_phase_s |=> ##1 $stable(PADDR);
endproperty
assert property (p_addr_stable)
  else $error("PADDR changed during ACCESS phase");

// 2.2 Control and data signals must remain stable during ACCESS
property p_ctrl_data_stable;
  @(posedge PCLK) disable iff(!PRESETn)
    setup_phase_s |=> ##1
      ($stable(PWRITE) && $stable(PSTRB) && $stable(PWDATA));
endproperty
assert property (p_ctrl_data_stable)
  else $error("Control or write data signals changed during ACCESS");

//////////////////////////////////////////////////////////////////////////////
// 3. Single-Cycle Access Timing
//////////////////////////////////////////////////////////////////////////////

// 3.1 ACCESS must complete in a single cycle: PREADY deasserts immediately after ACCESS
property p_single_cycle_ready;
  @(posedge PCLK) disable iff(!PRESETn)
    access_phase_s |=> ##1 (!PREADY);
endproperty
assert property (p_single_cycle_ready)
  else $error("PREADY remained asserted beyond one cycle ACCESS");

endmodule : APB_SVA