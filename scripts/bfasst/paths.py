import pathlib

# root_path = pathlib.Path(__file__).parent.parent.parent
ROOT_PATH = pathlib.Path(__file__).resolve().parent.parent.parent

EXAMPLES_PATH = ROOT_PATH / "examples"
EXPERIMENTS_PATH = ROOT_PATH / "experiments"
RESOURCES_PATH = ROOT_PATH / "resources"
SCRIPTS_PATH = ROOT_PATH / "scripts"
ERROR_FLOW_PATH = ROOT_PATH / "error_flows"

I2C_RESOURCES = RESOURCES_PATH / "iCEcube2"
YOSYS_RESOURCES = RESOURCES_PATH / "yosys"
ONESPIN_RESOURCES = RESOURCES_PATH / "onespin"