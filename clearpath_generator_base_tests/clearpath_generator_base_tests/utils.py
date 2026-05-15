# Software License Agreement (BSD)
#
# @author    Luis Camero <lcamero@clearpathrobotics.com>
# @copyright (c) 2026, Clearpath Robotics, Inc., All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of Clearpath Robotics nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Redistribution and use in source and binary forms, with or without
# modification, is not permitted without the express permission
# of Clearpath Robotics.
import argparse
import difflib
import filecmp
import os

from typing import List
from collections.abc import Callable

from ament_index_python.packages import get_package_share_directory


DEFAULT_SETUP_PATH = '/etc/clearpath'


class MissingSampleException(Exception):
    """Exception to capture missing sample directories."""

    def __init__(self, message, errors):
        """Initialize default exception and keep errors."""
        super().__init__(message)
        self.errors = errors


class MismatchSampleException(Exception):
    """Exception to capture mismatching sample files."""

    def __init__(self, message, errors):
        """Initialize default exception and keep errors."""
        super().__init__(message)
        self.errors = errors


def diff_dir_trees(
        dir_1: str,
        dir_2: str,
        shallow: bool = False,
        line_filter: Callable = None
        ) -> tuple[List]:
    """Compare the two directory trees and return a list of differences."""
    logs = []
    summary_logs = []
    # Compare Directories
    dirs_cmp = filecmp.dircmp(dir_1, dir_2)
    # Log Only in Installed Directory
    if len(dirs_cmp.left_only) > 0:
        error = (
            f'Files/directories: {dirs_cmp.left_only}, '
            f'only found in: {dir_1} '
            f'not in: {dir_2}'
        )
        logs.append(error)
        summary_logs.append(error)
    # Log Only in Generated Directory
    if len(dirs_cmp.right_only) > 0:
        error = (
            f'Files/directories: {dirs_cmp.right_only}, '
            f'only found in: {dir_2} '
            f'not in: {dir_1}'
        )
        logs.append(error)
        summary_logs.append(error)
    # Compare Files
    (_, mismatches, errors) = filecmp.cmpfiles(
        dir_1, dir_2, dirs_cmp.common_files, shallow=False)
    # Log File Mismatches
    for mismatch in mismatches:
        path_1 = os.path.join(dir_1, mismatch)
        path_2 = os.path.join(dir_2, mismatch)
        with open(path_1, 'r') as fp1:
            lines_1 = fp1.readlines()
        with open(path_2, 'r') as fp2:
            lines_2 = fp2.readlines()
        if line_filter:
            lines_1 = line_filter(lines_1, path_1)
            lines_2 = line_filter(lines_2, path_2)
        file_diff = difflib.unified_diff(
            a=lines_1,
            b=lines_2,
            fromfile=path_1,
            tofile=path_2,
        )
        str_file_diff = ''    ''.join(list(file_diff))
        if len(str_file_diff) > 0:
            logs.append(
                f'File mismatch: \n{str_file_diff}')
            summary_logs.append(
                f'File mismatch: {os.path.relpath(path_1)}')
    # Log File Errors
    if len(errors) > 0:
        logs.append(
            f'Errors: {errors} found when '
            f'comparing: {dir_1} '
            f'and: {dir_2}'
        )
    # Recurse
    if not shallow:
        for common_dir in dirs_cmp.common_dirs:
            sub_logs, sub_summary_logs = diff_dir_trees(
                dir_1=os.path.join(dir_1, common_dir),
                dir_2=os.path.join(dir_2, common_dir),
                shallow=shallow,
                line_filter=line_filter,
            )
            logs.extend(sub_logs)
            summary_logs.extend(sub_summary_logs)
    return logs, summary_logs


def ensure_sample_dir_exists(sample_dir: str) -> None:
    """Create the sample directory if it does not already exist."""
    os.makedirs(sample_dir, exist_ok=True)


def find_real_path_to_samples(path: str) -> str:
    """Find real path to sample YAML files."""
    for sample in os.listdir(path):
        real_installed_sample_dir = os.path.dirname(
            os.path.dirname(
                os.path.realpath(
                    os.path.join(path, sample, 'robot.yaml'))))
        break
    return real_installed_sample_dir


def get_test_samples():
    """Return all test samples from Clearpath Config package."""
    samples = []
    share_dir = get_package_share_directory('clearpath_config')
    sample_dir = os.path.join(share_dir, 'sample')
    for sample in os.listdir(sample_dir):
        # Filter for Test Samples
        if 'test' not in sample:
            continue
        samples.append(sample)
    return samples



def normalize_sample_paths(root_dir: str, target_path: str = DEFAULT_SETUP_PATH) -> None:
    """Replace all occurrences of sample directory paths with the target path.

    Walks each sample subdirectory in root_dir and replaces all occurrences
    of that sample's absolute path with target_path in every text file.
    The robot.yaml file is excluded as it is a source input, not generated output.
    """
    target_path = target_path.rstrip('/')
    for sample_name in os.listdir(root_dir):
        sample_dir = os.path.join(root_dir, sample_name)
        if not os.path.isdir(sample_dir):
            continue
        sample_dir_abs = os.path.abspath(sample_dir)
        # Replace with trailing slash first, then without
        replacements = [
            (sample_dir_abs + '/', target_path + '/'),
            (sample_dir_abs, target_path),
        ]
        for dirpath, _, filenames in os.walk(sample_dir):
            for filename in filenames:
                if filename == 'robot.yaml':
                    continue
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                except (UnicodeDecodeError, PermissionError):
                    continue
                original = content
                for old, new in replacements:
                    content = content.replace(old, new)
                if content != original:
                    with open(filepath, 'w') as f:
                        f.write(content)


def generate_samples_main(
        prog: str,
        description: str,
        generate_fn: Callable[[str], None],
        default_out: str = None) -> None:
    """Shared entry point for all generate_samples scripts.

    Handles argument parsing, invokes the generator function, and optionally
    normalizes paths in the generated output.

    :param prog: Program name for argparse.
    :param description: Description for argparse.
    :param generate_fn: Function that generates samples given a root directory.
    :param default_out: Default output directory. If None, current working directory is used.
    """
    parser = argparse.ArgumentParser(prog=prog, description=description)
    parser.add_argument(
        '--out',
        help='Output directory of generated files.',
        default=default_out if default_out else os.getcwd(),
        required=False)
    parser.add_argument(
        '--no-normalize',
        action='store_true',
        default=False,
        help='Skip post-generation path normalization. '
             'By default, absolute paths in generated files are replaced '
             f'with {DEFAULT_SETUP_PATH}.')
    args = parser.parse_args()

    root_dir = os.path.abspath(args.out)
    assert os.path.isdir(root_dir), f'Output directory "{root_dir}" does not exist.'

    generate_fn(root_dir)

    if not args.no_normalize:
        print('Normalizing paths in generated files...')
        normalize_sample_paths(root_dir)
        print('Done.')
