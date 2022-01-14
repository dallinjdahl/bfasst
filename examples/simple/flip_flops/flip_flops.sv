/*************************************************************************************************************
*
*  Copyright 2021 BYU Configurable Computing Lab
*
*  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
*  associated documentation files (the "Software"), to deal in the Software without restriction, including 
*  without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
*  copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the 
*  following conditions:
*
*  The above copyright notice and this permission notice shall be included in all copies or substantial 
*  portions of the Software.
*
*  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
*  LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO 
*  EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
*  IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR 
*  THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*
**************************************************************************************************************/

/*************************************************************************************************************
*
*  Module Description: Some flip flops that display a binary number of the LEDs and can add or clear that
*                      number using the buttons
*
**************************************************************************************************************/

`default_nettype none
module flip_flops(
    input wire logic clk,
    input wire logic clear,
    input wire logic plus,
    output logic [3:0] Q,
    output logic [3:0] input_ff
    );
    
    
    assign input_ff = (~clear & ~plus)? Q:
                 (~clear & plus)? Q+4'b0001:
                 (clear & ~plus)? 4'b0000:
                 (clear & plus)? Q:
                 Q;
    
    FDCE my_ff0 (.Q(Q[0]), .C(clk), .CE(1'b1), .CLR(1'b0), .D(input_ff[0]));
    FDCE my_ff1 (.Q(Q[1]), .C(clk), .CE(1'b1), .CLR(1'b0), .D(input_ff[1]));
    FDCE my_ff2 (.Q(Q[2]), .C(clk), .CE(1'b1), .CLR(1'b0), .D(input_ff[2]));
    FDCE my_ff3 (.Q(Q[3]), .C(clk), .CE(1'b1), .CLR(1'b0), .D(input_ff[3]));
    
    
endmodule
