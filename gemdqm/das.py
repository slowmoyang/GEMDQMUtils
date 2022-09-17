import subprocess
from subprocess import PIPE
import shlex
import warnings

def run_dasgoclient(query: str) -> list[str]:
    args = [
        '/cvmfs/cms.cern.ch/common/dasgoclient',
        '-limit',
        '0',
        '-query',
        query
    ]
    print(f"running '{shlex.join(args)}'")
    output = subprocess.run(args, stdout=PIPE, stderr=PIPE, encoding='utf-8')
    if len(output.stderr) != 0:
        warnings.warn(output.stderr, RuntimeWarning)
    data = [line for line in output.stdout.split('\n') if len(line) > 0]
    return data
