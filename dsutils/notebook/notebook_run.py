import yaml
import json
import argparse
from dsutils import notebook_utils

"""
Execute a parameterised template notebook.
"""

if __name__ == '__main__':
    """
    Example usage:

    source activate py36
    python ~/myrepos/dsutils/dsutils/notebook/notebook_run.py \
      --nb-path ~/myrepos/ju_notebooks/notebook_tips_tricks/nbrun_example/example-template-notebook.ipynb \
      --nb-suffix cli_test \
      --nb-kwargs "{'data_id': 2, 'analysis_type': c}"
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--nb-path', type=str, required=True)
    parser.add_argument('--out-path', type=str)
    parser.add_argument('--nb-suffix', dest='nb_suffix', type=str)
    parser.add_argument('--nb-kwargs', type=str)
    parser.add_argument('--nb-tstamp', type=bool)
    parser.add_argument('--hide-input', type=bool)
    parser.add_argument('--insert-pos', type=int)
    parser.add_argument('--kernel-name', type=str)
    parser.add_argument('--timeout', type=int)
    parser.add_argument('--execute-kwargs', type=json.loads)

    args = parser.parse_args()

    args.nb_kwargs = yaml.safe_load(args.nb_kwargs)

    notebook_utils.run_notebook(**vars(args))
