import subprocess
from subprocess import PIPE
import shlex
import warnings
import os

def run_dasgoclient(query: str,
                    executable: str = '/cvmfs/cms.cern.ch/common/dasgoclient'
) -> list[str]:
    if not os.path.exists(executable):
        raise RuntimeError(f'{executable} not found')

    args = [
        executable,
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
