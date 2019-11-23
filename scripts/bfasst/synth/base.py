import abc

class SynthesisTool(abc.ABC):
    # Save directory in which to run the tool
    def __init__(self, cwd):
        self.cwd = cwd

    # This method should run synthesis.  It should return 
    # (netlist, status), where:
    #   - netlist is the path to the produced netlist file
    #   - status is a Status object from bfasst.status
    @abc.abstractmethod
    def create_netlist(self, design, build_dir):
        pass