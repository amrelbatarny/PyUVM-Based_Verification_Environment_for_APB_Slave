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
  property p_apb_transfer;
    @(posedge PCLK) disable iff(!PRESETn)
      setup_phase_s |=> ##1 access_phase_s;
  endproperty : p_apb_transfer
  ASSERT_APB_TRANSFER: assert property (p_apb_transfer)
    else $error("[ASSERT_APB_TRANSFER] APB transfer timing violation: ACCESS not seen 1 cycle after SETUP");
  COVER_APB_TRANSFER: cover property (p_apb_transfer);

  property p_pready_idle;
    @(posedge PCLK) disable iff(!PRESETn)
      (!PSELx || !PENABLE) |-> !PREADY;
  endproperty : p_pready_idle
  ASSERT_PREADY_IDLE: assert property (p_pready_idle)
    else $error("[ASSERT_PREADY_IDLE] PREADY asserted outside ACCESS phase");
  COVER_PREADY_IDLE: cover property (p_pready_idle);

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

  //----------------------------------------------------------------------
  // 4. Register-File Interface Assertions
  //----------------------------------------------------------------------
  property p_write_enable;
    @(posedge PCLK) disable iff(!PRESETn)
      access_phase_s && PWRITE |-> (write_en && !read_en);
  endproperty : p_write_enable
  ASSERT_WRITE_ENABLE: assert property (p_write_enable)
    else $error("[ASSERT_WRITE_ENABLE] write_en/read_en mismatch on write transfer");
  COVER_WRITE_ENABLE: cover property (p_write_enable);

  property p_read_enable;
    @(posedge PCLK) disable iff(!PRESETn)
      access_phase_s && !PWRITE |-> (read_en && !write_en);
  endproperty : p_read_enable
  ASSERT_READ_ENABLE: assert property (p_read_enable)
    else $error("[ASSERT_READ_ENABLE] write_en/read_en mismatch on read transfer");
  COVER_READ_ENABLE: cover property (p_read_enable);

  property p_byte_strobe;
    @(posedge PCLK) disable iff(!PRESETn)
      access_phase_s |-> (byte_strobe == PSTRB);
  endproperty : p_byte_strobe
  ASSERT_BYTE_STROBE: assert property (p_byte_strobe)
    else $error("[ASSERT_BYTE_STROBE] byte_strobe mismatch during ACCESS phase");
  COVER_BYTE_STROBE: cover property (p_byte_strobe);

  property p_wdata;
    @(posedge PCLK) disable iff(!PRESETn)
      access_phase_s |-> (wdata == PWDATA);
  endproperty : p_wdata
  ASSERT_WDATA: assert property (p_wdata)
    else $error("[ASSERT_WDATA] wdata mismatch during ACCESS phase");
  COVER_WDATA: cover property (p_wdata);

endmodule : APB_SVA