# RAY Distributed ML Framework Validation

## Overview

This repository contains scripts and instructions for validating the RAY Distributed ML framework. The validation process ensures that the framework functions as expected in a distributed machine learning environment.

## Prerequisites

- Python 3.7 or higher
- The Current Release RAY framework installed (version 2.7.0)
- Additional dependencies listed in requirements.txt

## Validation Steps

1. **Setup Environment**: Set up the required environment variables. Please make sure you have updated right head node hostport Ip and port.
    self._address = "10.224.226.40"
    self._port = 8265

2. **Validation Script**: Run the validation script.
    ```bash
    python ray_tasks_bechmark_script.py
    ```

## Issues and Contributions

If you encounter any issues during the validation process or would like to contribute to the validation scripts, please open an issue or submit a pull request to EzUA Dev Team.