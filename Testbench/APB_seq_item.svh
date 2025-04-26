// APB_seq_item.svh
// -----------------------------------------------------------------------------
// This file contains the DPI function implementations for the APB_seq_item_pkg.
// These functions are exported via DPI-C in the package file and provide the
// functionality required by pyquesta for object exchange between SystemVerilog
// and Python.
// -----------------------------------------------------------------------------

function string sv_get;
    APB_seq_item obj;
    string obj_str;
    // Create a new transaction object
    obj = new();

    // Randomize the object with constraints
    void'(obj.randomize() with {
        PRESETn dist { 1 :/ 90, 0 :/ 10 };
        PENABLE dist { 1 :/ 90, 0 :/ 10 };
        PWDATA dist {
            32'h00000000 :/ 20,
            [32'h00000001:32'hFFFFFFFE] :/ 60,
            32'hFFFFFFFF :/ 20
        };
        if (PWRITE == 0) { PWDATA == 0; }
        PADDR inside { [32'h00000000:32'h0000003C] };
        (PADDR % 4) == 0;
        PSTRB dist {[1:5]:/10, [6:10]:/20, [11:14]:/70, 15:/90};
    });

    // Serialize the object and return the string
    obj_str = obj.serialize();
    return obj_str;
endfunction

covergroup APB_cg with function sample(APB_seq_item item);
    PRESETn_cp: coverpoint item.PRESETn {
        bins reset_active   = {1};
        bins reset_inactive = {0};
    }
    PENABLE_cp: coverpoint item.PENABLE {
        bins enabled   = {1};
        bins disabled  = {0};
    }
    PWRITE_cp:  coverpoint item.PWRITE  {
        bins write = {1};
        bins read  = {0};
    }
    PADDR_cp:   coverpoint item.PADDR   {
        bins aligned_addr[] = {0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60};
    }
    PWDATA_cp:  coverpoint item.PWDATA  {
        bins zero     = {32'h0};
        bins max      = {32'hFFFFFFFF};
        bins typical  = {[32'h1:32'hFFFFFFFE]};
    }
    WRITE_x_DATA: cross PWRITE_cp, PWDATA_cp {
        ignore_bins read_nonzero = binsof(PWRITE_cp.read) && binsof(PWDATA_cp.typical); // Ensures read transactions have PWDATA=0 (as per the constraint)
    }
    WRITE_x_ADDR: cross PWRITE_cp, PADDR_cp;
endgroup

// Global coverage instance
APB_cg cov_inst = new();

function void sv_put(input string data_buf);
    APB_seq_item obj;
    obj = new();
    obj.deserialize(data_buf);

    // ===== Debug Control =====
    `ifdef DEBUG_SVCONDUIT
        $display("=============================================");
        $display("[SV] Received: %s", data_buf);
        $display("[SV] Deserialized Item:");
        $display("  PRESETn = %0d", obj.PRESETn);
        $display("  PWDATA  = 0x%8h", obj.PWDATA);
        $display("  PENABLE = %0d", obj.PENABLE);
        $display("  PWRITE  = %0d", obj.PWRITE);
        $display("  PADDR   = 0x%8h", obj.PADDR);
        $display("=============================================");
    `endif
    // ========================

    cov_inst.sample(obj);
endfunction

function string sv_transport(input string data_buf);
    // Optional implementation for transporting data.
    return "";
endfunction