if {$argc != 5} {
    puts "Usage: run_backend.tcl <project name> <build directory> <device> <top module> <iCEcube2 directory>"
    exit
}

set proj_name [lindex $argv 0]
set proj_dir [lindex $argv 1]
set device [lindex $argv 2]
set top_module [lindex $argv 3]
set iCEcube2_dir [lindex $argv 4]

#set device iCE40HX8K-CT256
#set top_module ALU
#set proj_dir /home/elicahill/lscc/iCEcube2.2017.08/sbt_backend/Projects/test/
append output_dir $proj_name "_Implmnt"
append edif_file $proj_name ".edf"
append sbt_root $iCEcube2_dir "sbt_backend/"
append sbt_tcl $sbt_root "/tcl/sbt_backend_synpl.tcl"
source $sbt_tcl 
run_sbt_backend_auto $device $top_module $proj_dir $output_dir "" $edif_file     
