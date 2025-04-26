package APB_seq_item_pkg;
export "DPI-C" function sv_get;
export "DPI-C" function sv_put;
export "DPI-C" function sv_transport;


// *** APB_seq_item ***
    typedef byte unsigned APB_seq_item_buf_t[10];
    typedef bit[0:79] APB_seq_item_packed_t;

    class APB_seq_item;
       rand  int unsigned  addr;
       rand  int unsigned  data;
       rand  byte unsigned  strobe;
       rand  byte unsigned  type_sv;

        function new(APB_seq_item_buf_t buffer={0,0,0,0,0,0,0,0,0,0});
            APB_seq_item_packed_t packed_buf;
            packed_buf = 80'(buffer);
            addr = packed_buf[0:31];
            data = packed_buf[32:63];
            strobe = packed_buf[64:71];
            type_sv = packed_buf[72:79];
        endfunction

        function string serialize();
            string buffer;
            buffer = $sformatf("%08h%08h%02h%02h",addr,data,strobe,type_sv);
            return buffer;
        endfunction

        // User-defined: parse that 20-char string back into fields
        function void deserialize(string str);
            addr        = str.substr( 0,  7).atohex();
            data        = str.substr( 8, 15).atohex();
            strobe      = str.substr(16, 17).atohex();
            type_sv        = str.substr(18, 19).atohex();
        endfunction
    endclass

`include "APB_seq_item.svh"
endpackage