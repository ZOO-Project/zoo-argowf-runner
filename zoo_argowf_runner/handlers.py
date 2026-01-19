"""Execution Handler for Argo Workflows.

Re-exports ExecutionHandler from zoo-runner-common.
"""

# Add zoo-runner-common to path
# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../zoo-runner-common')))
from zoo_runner_common.handlers import ExecutionHandler

__all__ = ['ExecutionHandler']
