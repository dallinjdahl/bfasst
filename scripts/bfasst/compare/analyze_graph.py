from re import X
import bfasst
import bfasst.paths
import subprocess
import shutil
from subprocess import Popen
from pathlib import Path
from bfasst.config import VIVADO_BIN_PATH

'''A function to launch the graphs for designs that have already been tested. Mainly meant
for checking designs that came back unequivalent to see what was wrong with them.'''
def analyze_graphs(path, module):
    impl_v = path / Path(module + "_impl.v")
    impl_tb = path / Path(module + "_impl_tb.v")
    reversed_v = path / Path(module + "_reversed.v")
    reversed_tb = path / Path(module + "_reversed_tb.v")
    impl_vcd = path / Path(module + "_impl.vcd")
    reversed_vcd = path / Path(module + "_reversed.vcd")
    impl_tcl = path / Path(module + "_impl.tcl")
    reversed_tcl = path / Path(module + "_reversed.tcl")
    impl_fst = path / Path(module + "_impl.vcd.fst")
    reversed_fst = path / Path(module + "_reversed.vcd.fst")
    diff = path / Path("diff.txt")
    run_vivado = bfasst.paths.ROOT_PATH / Path("scripts/bfasst/compare_waveforms/run_vivado.py")
    base_path = bfasst.paths.ROOT_PATH / Path("scripts/bfasst/compare_waveforms")

    if(diff.exists()):
        with diff.open() as file:
            for line in file:
                print(line)

    gtkwave = Path(".gtkwaverc")
    if(gtkwave.exists()):
        gtkwave.unlink()
    with gtkwave.open("x") as wavefile:
        wavefile.write("do_initial_zoom_fit 1\n")

        #Optional: Functionality to detect a system's monitor size is added so that
        # gtkwave can launch in full-screen mode.
        choice = input("Do you want to launch in full-screen mode? 1 for yes, 0 for no.")
        if(choice != "0"): 
            (x,y) = find_resolution()
            x = str(x)
            y = str(y)
            wavefile.write("initial_window_x " + x + "\n")
            wavefile.write("initial_window_y " + y + "\n")
        
        choice = input("Compare with Vivado? 1 for yes, 0 for no.")
        vivado = False
        if(choice != "0"):
            vivado=True

    if(vivado):
        commands = [
            ["gtkwave", "-T", str(impl_tcl), "-o", str(impl_vcd)],
            ["gtkwave", "-T", str(reversed_tcl), "-o", str(reversed_vcd)],
            ["python", str(run_vivado), str(impl_v), 
            str(impl_tb), module + "_impl_tb", str(reversed_v), str(reversed_tb), module + "_reversed_tb", str(VIVADO_BIN_PATH),
            str(base_path)]
        ]
    else:
        commands = [
            ["gtkwave", "-T", str(impl_tcl), "-o", str(impl_vcd)],
            ["gtkwave", "-T", str(reversed_tcl), "-o", str(reversed_vcd)]
        ]

    procs = [Popen(i) for i in commands]
    for p in procs:
        p.wait()

    gtkwave.unlink()
    impl_fst.unlink()
    reversed_fst.unlink()



'''A function primarily meant to check the user's monitor resolution so gtkwave can launch in full-screen mode.'''
def find_resolution():
    output = subprocess.check_output("xrandr")
    output = output.decode()
    temp = Path("temp.txt")
    with temp.open("x") as file:
        file.write(output)
    
    foundDisplay = False
    isPrimary = False

    with temp.open("r") as file:
        for line in file:
            if "primary" in line:
                isPrimary = True
            if isPrimary:
                #The user-resolution is indicated by the * character in a line.
                if "*" in line:
                    if foundDisplay == False:
                        line = line.strip()
                        #The user-resolution is always in the format ____x____, so the width is before the x and the
                        # height is after the x. 
                        x = line[0:line.index("x")]
                        y = line[line.index("x")+1:line.index(" ")]
                        foundDisplay = True
                        temp.unlink()
                        return(x, y)
    #If, for whatever reason, the screen resolution can't be found, it defaults to the absolute lowest screen resolution.
    if(foundDisplay == False):
        temp.unlink()
        return(320, 200)
    
    temp.unlink()
                    

