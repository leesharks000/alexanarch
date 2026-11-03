import sys, numpy as np
sys.argv=['x','raw/OH','2.5','2.0']
import importlib.util
spec=importlib.util.spec_from_file_location('cf','cometframe_raw.py'); cf=importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
from oh_cluster import clusters
