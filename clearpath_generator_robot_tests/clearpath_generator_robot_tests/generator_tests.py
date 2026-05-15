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

import os

from ament_index_python.packages import get_package_share_directory

from clearpath_generator_base_tests.generator_tests import (
    BaseGeneratorSampleTest
)
from clearpath_generator_base_tests.utils import (
    find_real_path_to_samples,
    normalize_sample_paths,
)
from clearpath_generator_robot_tests.sample_generator import (
    generate_test_samples
)


class TestGeneratorRobotSamples(BaseGeneratorSampleTest):
    """
    Robot generator class for validating generated samples.

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
    GENERATOR_NAME = 'robot'
    # Directory of installed samples
    SHARE_DIR = get_package_share_directory('clearpath_generator_robot_tests')
    INSTALLED_SAMPLE_DIR = find_real_path_to_samples(os.path.join(SHARE_DIR, 'samples'))

    def test_generate_samples(self) -> None:
        """Validate robot sample generation."""
        generate_test_samples(self.NEW_SAMPLE_DIR)
        normalize_sample_paths(self.NEW_SAMPLE_DIR)
        return

    def test_number_of_samples_match(self) -> None:
        """Validate number of generated samples match installed."""
        super().test_number_of_samples_match()
        return

    def test_samples_match(self) -> None:
        """Validate contents of generated sample directory match."""
        super().test_samples_match()
        return
