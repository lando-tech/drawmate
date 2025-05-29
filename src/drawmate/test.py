import sys
from pathfinder import PathFinder

pf = PathFinder()
root_dir = pf.get_project_dir()
sys.path.insert(0, f"{root_dir}/drawmate_engine/build")
import drawmate_engine
