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

  //----------------------------------------------------------------------
  // APB Phase Sequences
  //----------------------------------------------------------------------
  sequence setup_phase_s;
    PSELx    &&
    !PENABLE &&
    !PREADY;
  endsequence : setup_phase_s

  sequence access_phase_s;
    PSELx   &&
    PENABLE &&
    PREADY;
  endsequence : access_phase_s

  //----------------------------------------------------------------------
  // 1. Protocol Handshake Properties
  //----------------------------------------------------------------------
  property p_pready_access;
    @(posedge PCLK) disable iff(!PRESETn)
      access_phase_s |-> PREADY;
  endproperty : p_pready_access
  ASSERT_PREADY_ACCESS: assert property (p_pready_access)
    else $error("[ASSERT_PREADY_ACCESS] PREADY not asserted during ACCESS phase");
  COVER_PREADY_ACCESS: cover property (p_pready_access);

  //----------------------------------------------------------------------
  // 2. Signal Stability Properties
  //----------------------------------------------------------------------
  property p_addr_stable;
    @(posedge PCLK) disable iff(!PRESETn)
      setup_phase_s |=> ##1 $stable(PADDR);
  endproperty : p_addr_stable
  ASSERT_ADDR_STABLE: assert property (p_addr_stable)
    else $error("[ASSERT_ADDR_STABLE] PADDR changed during ACCESS phase");
  COVER_ADDR_STABLE: cover property (p_addr_stable);

  property p_ctrl_data_stable;
    @(posedge PCLK) disable iff(!PRESETn)
      setup_phase_s |=> ##1 ($stable(PWRITE) && $stable(PSTRB) && $stable(PWDATA));
  endproperty : p_ctrl_data_stable
  ASSERT_CTRL_DATA_STABLE: assert property (p_ctrl_data_stable)
    else $error("[ASSERT_CTRL_DATA_STABLE] Control or write data signals changed during ACCESS phase");
  COVER_CTRL_DATA_STABLE: cover property (p_ctrl_data_stable);

  //----------------------------------------------------------------------
  // 3. Single-Cycle Access Timing
  //----------------------------------------------------------------------
  property p_single_cycle_ready;
    @(posedge PCLK) disable iff(!PRESETn)
      access_phase_s |=> ##1 (!PREADY);
  endproperty : p_single_cycle_ready
  ASSERT_SINGLE_CYCLE_READY: assert property (p_single_cycle_ready)
    else $error("[ASSERT_SINGLE_CYCLE_READY] PREADY remained asserted beyond one cycle");
  COVER_SINGLE_CYCLE_READY: cover property (p_single_cycle_ready);

endmodule : APB_SVA