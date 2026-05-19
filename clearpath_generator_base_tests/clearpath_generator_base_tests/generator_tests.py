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

"""Pytest Test Class and Utility Methods for Validating Generated Samples."""

import filecmp
import os

from typing import List

from ament_index_python.packages import get_package_share_directory

from clearpath_generator_base_tests.utils import (
    ensure_sample_dir_exists,
    diff_dir_trees,
    get_test_samples,
    MismatchSampleException,
    MissingSampleException,
)


class BaseGeneratorSampleTest:
    """
    Base test class for validating generated samples.

    Methods
    -------
    test_generate_samples()
        Generate samples. Throw exception if failed.
    test_number_of_samples()
        Validate the same number of samples are generated as installed.
    test_samples_match()
        Validate generated samples match existing files.

    """

    # Generator name
    GENERATOR_NAME = 'base'
    # Directory to generate samples
    NEW_SAMPLE_DIR = os.path.join(os.environ['HOME'], '.clearpath', 'samples')
    ensure_sample_dir_exists(NEW_SAMPLE_DIR)
    # Directory of installed samples
    SHARE_DIR = get_package_share_directory('clearpath_generator_base_tests')
    INSTALLED_SAMPLE_DIR = os.path.join(SHARE_DIR, 'samples')
    # Test samples
    TEST_SAMPLES = get_test_samples()

    def __init_subclass__(cls, **kwargs):
        """Initialize subclass with generator-specific sample directory."""
        super().__init_subclass__(**kwargs)
        cls.NEW_SAMPLE_DIR = os.path.join(
            BaseGeneratorSampleTest.NEW_SAMPLE_DIR, cls.GENERATOR_NAME
        )
        ensure_sample_dir_exists(cls.NEW_SAMPLE_DIR)

    def filter_lines(self, lines: List[str], filepath: str) -> List[str]:
        """Filter file lines to prevent comparing lines that are expected to be different."""
        return lines

    def test_number_of_samples_match(self):
        """Validate number of samples matches."""
        if self.TEST_SAMPLES == 0:
            return

        errors, _ = diff_dir_trees(
            dir_1=self.NEW_SAMPLE_DIR,
            dir_2=self.INSTALLED_SAMPLE_DIR,
            shallow=True)

        if len(errors) > 0:
            raise MissingSampleException(
                'The number of generated samples does not match installed samples:\n'
                f'\n{"\n".join(errors)}',
                errors
            )

    def test_samples_match(self):
        """Validate contents of generated sample directory match."""
        if self.TEST_SAMPLES == 0:
            return
        errors = []
        error_summary = []

        dirs_cmp = filecmp.dircmp(
            self.NEW_SAMPLE_DIR,
            self.INSTALLED_SAMPLE_DIR
        )

        for common_dir in dirs_cmp.common_dirs:
            sample_errors, sample_errors_summary = diff_dir_trees(
                dir_1=os.path.join(self.NEW_SAMPLE_DIR, common_dir),
                dir_2=os.path.join(self.INSTALLED_SAMPLE_DIR, common_dir),
                shallow=False,
                line_filter=self.filter_lines,
            )
            if len(sample_errors) > 0:
                errors.append(
                    f'Generator {self.GENERATOR_NAME} sample "{common_dir}"'
                    ' mismatch between installed and'
                    ' generated file(s)'.center(100, '-') +
                    f'\n{"\n\n".join(sample_errors)}'
                )
                error_summary.append(
                    f'Generator {self.GENERATOR_NAME} sample "{common_dir}"'
                    ' mismatch between installed and'
                    ' generated file(s):'.center(100, '-') +
                    f'\n{"\n\n".join(sample_errors_summary)}'
                )

        error_summary.insert(
            0,
            f'Error summary, {len(errors)} sample output mismatch'.center(100, '='))

        if len(errors) > 0:
            raise MismatchSampleException(
                f'{len(errors)} generated sample(s) did not match installed sample(s)\n'
                f'\n{"\n\n".join(errors + error_summary)}',
                errors
            )
