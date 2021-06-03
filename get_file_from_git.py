import subprocess
from textwrap import dedent
import json
from pathlib import Path
import shutil
import shlex

"""
Get all metrics.json from all commit of each branch 
- run this script inside the question-classifier.git
"""

myoutdir = Path("../OUTPUT_metrics")
myoutdir.mkdir(parents=True, exist_ok=True)

subprocess.run(['git', 'fetch', '--all', '--prune'])
subprocess.run(['git', 'checkout', 'main'])
subprocess.run(['git', 'pull', '--ff-only', 'origin', 'main'])

# get a list of branch
branch = subprocess.run(['git', 'branch', '-r'], capture_output=True)
branch_list = branch.stdout.strip().split(b'\n')
branch_list = [x.decode().strip().replace('origin/','') for x in branch_list]
branch_list = [x for x in branch_list if not x.startswith("HEAD")]


for br in branch_list:
    brdir = myoutdir / br
    brdir.mkdir(parents=True, exist_ok=True)

    subprocess.run(['git', 'fetch', '--all'])  # --all for other remotes? 
    print(f'*** checking out branch "{br}"')
    subprocess.run(['git', 'switch', br])
    print("getting list of commits")
    result = subprocess.run(['git', 'rev-list', 'main'], capture_output=True)
    L = result.stdout

    L = L.split()
    L.reverse()
    L = [x.decode() for x in L]   # convert to str

    print("Iterating over commits")
    for x in L:
        print(f"**** {x}")
        subprocess.run(['git', 'checkout', x])
        metric_files = list(Path('output').glob('**/metrics.json'))
        
        # unix timestamp
        timedatething = subprocess.check_output(shlex.split("git show -s --format=%ct"))
        timedatething = timedatething.decode().strip()

        for met in metric_files:
            # flat out the filename
            outfile = str(met).replace('/', '_')
            outfile = outfile.replace('output_', '')
            outfile = f"{timedatething}__{outfile}"
            shutil.copyfile(met, brdir / outfile)
       
