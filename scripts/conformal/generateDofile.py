#!/usr/bin/env python

from os import listdir
from os.path import isfile, join
import sys

# usage: gendo


def main():

    # get path to source files
    pathToDesign = sys.argv[1]
    print "path to design:", pathToDesign

    srcDir = pathToDesign + "/src"
    print "working directory:", srcDir

    print "looking for source RTL files in", srcDir

    # get RTL source files
    vlog = [
        join(srcDir, f) for f in listdir(srcDir) if (isfile(join(srcDir, f)) and f.endswith(".v"))
    ]

    vhdl = [
        join(srcDir, f) for f in listdir(srcDir) if (isfile(join(srcDir, f)) and f.endswith(".vhd"))
    ]

    # build file name
    dofile = join(pathToDesign, "dofile.do")
    print "creating", dofile

    # if the file exists, delete it
    if isfile(dofile):
        os.remove(dofile)

    # open the file and do the deed
    with open(dofile, "w+") as f:

        f.write("// generated by cmonster\n")

        # read libraries
        # TODO parameterize path to lattice libraries
        f.write(
            "read library -Both -Replace -sensitive -Verilog /auto/fsh/crg3710/research/lattice_libraries/sb_ice_syn.v -nooptimize\n"
        )

        # read golden design
        # for each VHDL source file
        if vhdl:
            f.write("read design ")
            for rtlFile in vhdl:
                f.write("%s " % rtlFile)

            # TODO see what these options do
            f.write(
                " -vhdl -Golden -continuousassignment Bidirectional -nokeep_unreach -norangeconstraint\n"
            )

        # for each Verilog source file
        if vlog:
            f.write("read design ")
            for rtlFile in vlog:
                f.write("%s " % rtlFile)

            # TODO see what these options do
            f.write(
                " -Verilog -Golden -continuousassignment Bidirectional -nokeep_unreach -norangeconstraint\n"
            )

        # read revised design
        global extracted
        print "looking for extracted netlist in", pathToDesign
        for ugh in listdir(pathToDesign):
            if ugh.endswith("_extracted.v"):
                extracted = join(pathToDesign, ugh)

        f.write(
            "read design %s -Verilog -Revised -sensitive -continuousassignment Bidirectional -nokeep_unreach -nosupply\n"
            % extracted
        )

        # add secret sauce
        f.write("set system mode lec\nadd compared points -all\ncompare")


if __name__ == "__main__":
    main()
