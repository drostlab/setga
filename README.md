# Minimal Subset Optimizer

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Overview

Minimal Subset Optimizer is a small Python library designed to extract a minimal subset from a given set, optimizing a given (set of) objective(s). Based on the [DEAP library](https://deap.readthedocs.io/en/master/).

## Features

- **Subset Extraction:** Automatically identifies and extracts a minimal subset from the input set optimizing given objective(s).
- **Multi-objective Optimization:** Optimizes the subset based on a provided objective or a set of objectives.
- **Highly Customizable:** Allows for customization of the crossover, mutation and selection functions (as long as they are contained in the DEAP library.


## Usage

```python
# Example Usage
from set_subset_optimizer import SubsetOptimizer

# Create an instance of the optimizer
optimizer = SubsetOptimizer()

# Define your input set and functions to optimize
input_set = {1, 2, 3, 4, 5}
objective_functions = [lambda subset: len(subset), lambda subset: sum(subset)]

# Optimize the subset
optimized_subset = optimizer.optimize_subset(input_set, objective_functions)

print("Optimized Subset:", optimized_subset)
