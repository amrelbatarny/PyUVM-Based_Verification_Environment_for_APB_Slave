package APB_seq_item_pkg;
    export "DPI-C" function sv_get;
    export "DPI-C" function sv_put;
    export "DPI-C" function sv_transport;


// *** APB_seq_item ***
    typedef byte unsigned APB_seq_item_buf_t[20];
    typedef bit[0:159] APB_seq_item_packed_t;

    class APB_seq_item;
       rand  int unsigned  PRESETn;
       rand  int unsigned  PWDATA;
       rand  int unsigned  PENABLE;
       rand  int unsigned  PWRITE;
       rand  int unsigned  PADDR;

        function new(APB_seq_item_buf_t buffer={0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0});
            APB_seq_item_packed_t packed_buf;
            packed_buf = 160'(buffer);
            PRESETn = packed_buf[0:31];
            PWDATA = packed_buf[32:63];
            PENABLE = packed_buf[64:95];
            PWRITE = packed_buf[96:127];
            PADDR = packed_buf[128:159];
        endfunction

        function string serialize();
            string buffer;
            buffer = $sformatf("%08h%08h%08h%08h%08h",PRESETn,PWDATA,PENABLE,PWRITE,PADDR);
            return buffer;
        endfunction
    endclass

    function string sv_get;
    APB_seq_item obj;
    string obj_str;
    obj = new();
    
    void'(obj.randomize() with {
        // Constraints must use class member syntax
        PRESETn dist { 1 :/ 90, 0 :/ 10 };
        PENABLE dist { 1 :/ 90, 0 :/ 10 };
        PWDATA dist {
            32'h00000000 :/ 20,
            [32'h00000001:32'hFFFFFFFE] :/ 60,  // Fixed range syntax
            32'hFFFFFFFF :/ 20
        };
        
        // Conditional constraints
        if (PWRITE == 0) {
            PWDATA == 0;
        }
        
        // Address constraints
        PADDR inside { [32'h00000000:32'h0000003C] };
        (PADDR % 4) == 0;
    });
    
    obj_str = obj.serialize();
    return obj_str;
endfunction

function void sv_put(input string data_buf);
    // Optional implementation
endfunction

function string sv_transport(input string data_buf);
    // Optional implementation
    return "";
endfunction

// `include "APB_seq_item.svh"
endpackage
