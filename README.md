# clearpath_generator_tests
Clearpath configuration system generator testing

## Overview

This repository contains test packages that version and validate the generated output of the
Clearpath generators (`clearpath_generator_common`, `clearpath_generator_robot`, and
`clearpath_generator_gz`). Each generator test package stores a set of reference samples and
compares them against freshly generated output to detect regressions.

## Packages

| Package | Description |
|---|---|
| `clearpath_generator_base_tests` | Base test class (`BaseGeneratorSampleTest`) and shared utilities used by all generator test packages. |
| `clearpath_generator_common_tests` | Tests for `clearpath_generator_common` (bash, description, discovery server, SRDF, etc.). |
| `clearpath_generator_robot_tests` | Tests for `clearpath_generator_robot` (robot launch and parameter files). |
| `clearpath_generator_gz_tests` | Tests for `clearpath_generator_gz` (Gazebo launch and parameter files). |

## How It Works

### Test Samples

Test samples originate from the `clearpath_config` package. The `get_test_samples()` utility
function in `clearpath_generator_base_tests` scans the `clearpath_config` sample directory for all
YAML files whose names contain `test` (e.g. `test_a200`, `test_w200`, `test_all_dual_sensors`).

Each generator test package has a `samples/` directory that is checked into version control.
This directory contains the expected (reference) output for every test sample. When a generator
changes its output, these reference samples must be regenerated and committed.

### Generating Samples

Each generator test package provides a `generate_samples` executable that regenerates the
reference samples. By default, generated files are written into the package's `samples/` directory.

```bash
# Common generator samples
ros2 run clearpath_generator_common_tests generate_samples

# Robot generator samples
ros2 run clearpath_generator_robot_tests generate_samples

# Gazebo generator samples
ros2 run clearpath_generator_gz_tests generate_samples
```

An optional `--out` argument can be used to specify an alternative output directory:

```bash
ros2 run clearpath_generator_common_tests generate_samples --out /path/to/output
```

After generating, review the changes and commit the updated `samples/` directory.

### Running Tests

Tests are run through `colcon test` using `ament_cmake_pytest`. Each generator test package
registers its `generator_tests.py` as a pytest test. The tests execute in order:

1. **`test_generate_samples`** — Runs the generator against all test samples, writing output to a
   temporary directory (`~/.clearpath/samples`). Raises an exception if generation fails.
2. **`test_number_of_samples_match`** — Compares the directory trees of the generated output and
   the installed reference samples to ensure no files or directories are missing or unexpected.
3. **`test_samples_match`** — Performs a file-by-file diff between the generated output and the
   installed reference samples, reporting any content mismatches.

To run all generator tests:

```bash
colcon test --packages-select \
  clearpath_generator_common_tests \
  clearpath_generator_robot_tests \
  clearpath_generator_gz_tests

colcon test-result --verbose
```

## Development Workflow

When making changes to `clearpath_common`, `clearpath_robot`, or `clearpath_simulator` that affect
generator output, a corresponding branch with the **same name** must be created in the
`clearpath_generator_tests` repository with regenerated samples.

1. **Create a branch** in the source repository (e.g. `clearpath_common`) and make your changes.
2. **Create a branch with the same name** in `clearpath_generator_tests`.
3. **Build** the workspace so the generator changes are installed.
4. **Regenerate samples** for each affected generator:
   ```bash
   ros2 run clearpath_generator_common_tests generate_samples
   ros2 run clearpath_generator_robot_tests generate_samples
   ros2 run clearpath_generator_gz_tests generate_samples
   ```
5. **Run the tests** to verify the regenerated samples are consistent:
   ```bash
   colcon test --packages-select \
     clearpath_generator_common_tests \
     clearpath_generator_robot_tests \
     clearpath_generator_gz_tests
   colcon test-result --verbose
   ```
6. **Review and commit** the updated `samples/` directories in `clearpath_generator_tests`.
7. **Push both branches.** The matching branch names allow CI and reviewers to pair the generator
   changes with their expected output.

