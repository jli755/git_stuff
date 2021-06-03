import subprocess
from textwrap import dedent
import json
from pathlib import Path
import shutil
import shlex


"""
Get latest output for each model
- run this script inside the question-classifier.git
"""

# name contains current date time
outdir = datetime.datetime.now().strftime("OUTPUT_%Y%m%d_%H-%M-%S") 
myoutdir = Path("..") / outdir
myoutdir.mkdir(parents=True, exist_ok=True)

# prune will delete branches removed from origin
subprocess.run(['git', 'fetch', '--all', '--prune'])
subprocess.run(['git', 'checkout', 'main'])
subprocess.run(['git', 'pull', '--ff-only', 'origin', 'main'])

# get a list of branch
branch = subprocess.run(['git', 'branch', '-r'], capture_output=True)
branch_list = branch.stdout.strip().split(b'\n')
branch_list = [x.decode().strip().replace('origin/','') for x in branch_list]
branch_list = [x for x in branch_list if not x.startswith("HEAD")]

# copy output directory from each branch
for br in branch_list:
    brdir = myoutdir / br
    brdir.mkdir(parents=True, exist_ok=True)

    print(f'*** checking out branch "{br}"')
    subprocess.run(['git', 'switch', br])
    subprocess.run(['git', 'pull', '--ff-only', 'origin', br])
    
    # will not copy if output dir is not exist
    try:
        shutil.copytree('output', brdir, dirs_exist_ok=True)
    except FileNotFoundError:
    	pass
