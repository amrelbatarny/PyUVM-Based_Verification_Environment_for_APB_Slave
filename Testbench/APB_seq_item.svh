/***********************************************************************
 * Author : Amr El Batarny
 * File   : APB_seq_item.svh
 * Brief  : DPI implementations (sv_get, sv_put, sv_transport) and
 *          covergroup for APB_seq_item.
 **********************************************************************/

function string sv_get;
    APB_seq_item obj;
    string obj_str;
    // Create a new transaction object
    obj = new();

    // Randomize the object with constraints
    void'(obj.randomize() with {
        type_sv inside { 0, 1 }; // 0=READ, 1=WRITE per Python APBType
        if (type_sv) {
            data dist {
                32'h00000000 :/ 20,
                [32'h00000001:32'hFFFFFFFE] :/ 60,
                32'hFFFFFFFF :/ 20
            };
            strobe dist {[1:5]:/10, [6:10]:/20, [11:14]:/70, 15:/90};
        }
        else {
            data == 0;
            strobe == 0;
        }
        addr inside { [32'h00000000:32'h0000003C] };
        (addr % 4) == 0;
    });
    // Serialize the object and return the string
    obj_str = obj.serialize();
    return obj_str;
endfunction

covergroup APB_cg with function sample(APB_seq_item item);
    type_cp:  coverpoint item.type_sv  {
        bins write = {1};
        bins read  = {0};
    }
    addr_cp:   coverpoint item.addr   {
        bins aligned_addr[] = {0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60};
    }
    data_cp:  coverpoint item.data  {
        bins zero     = {32'h0};
        bins max      = {32'hFFFFFFFF};
        bins typical  = {[32'h1:32'hFFFFFFFE]};
    }
    write_x_data: cross type_cp, data_cp {
        ignore_bins read_nonzero = binsof(type_cp.read) && binsof(data_cp.typical); // Ensures read transactions have data=0 (as per the constraint)
    }
    write_x_addr: cross type_cp, addr_cp;
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
        $display("  addr    = 0x%8h", obj.addr);
        $display("  data    = 0x%8h", obj.data);
        $display("  strobe  = 0x%2h", obj.strobe);
        $display("  type_sv    = 0x%2h", obj.type_sv);
        $display("=============================================");
    `endif
    // ========================

    cov_inst.sample(obj);
endfunction

function string sv_transport(input string data_buf);
    // Optional implementation for transporting data.
    return "";
endfunction