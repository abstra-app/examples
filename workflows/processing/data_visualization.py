import utils, shutil, sys
import pandas as pd
import abstra.forms as af
import abstra.common as ac

utils.check_user()

graph = ac.get_persistent_dir() / "latest.png"

if not graph.exists():
    af.display("No data yet.", end_program=True)
    sys.exit(0)

response = (
    af.Page()
    .display("The GRAPH")
    .display_image(graph, full_width=True)
    .run(end_program=True)
)
sys.exit(0)
