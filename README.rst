.. image:: https://readthedocs.org/projects/setga/badge/?version=latest
    :target: https://setga.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Minimal Subset Optimizer
========================

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT
.. image:: https://img.shields.io/badge/lifecycle-experimental-orange.svg
    :target: https://lifecycle.r-lib.org/articles/stages.html#experimental
.. image:: https://api.visitorbadge.io/api/visitors?path=https://github.com/lavakin/TraP-GA&label=Visitors&countColor=%23263759&style=flat

Overview
--------

SetGA is a small Python library designed to extract a minimal subset from a given set, optimizing a given (set of) objective(s). Based on the DEAP library.

Features
--------

- **Subset Extraction:** Automatically identifies and extracts a minimal subset from the input set optimizing given objective(s).
- **Multi-objective Optimization:** Optimizes the subset based on a provided objective or a set of objectives.
- **Highly Customizable:** Allows for customization of the crossover, mutation, and selection functions (as long as they are contained in the DEAP library).

Installation
-------------------

.. code-block:: bash

  pip3 install setga

Arguments
_________________
``set_size`` - size of the the set to optimize\

``eval_ind`` - fitness function (can compute multiple fitnesses, value or a list of values expected as an output)\

``stats_by`` - number of the objective to base statistic on (0 if num of genes, 1 if first user defined etc..)\

**Optionally:**

``pop_size`` -  num of solution on every island\
    
``num_gen`` - maximal number of generations \
    
``num_islands`` -  number of islands\
    
``min_max`` -  defines if user defined objectives should be minimized or maximized. Tuple of -1 (minimization) and 1 (maximization). Should have the same lenght as the fitness output.\
    
``mutation`` - type of mutation\
    
``crossover`` - type of crossover\
    
``mutation_rate`` - probability of an index to be selected for mutation\
    
``crossover_rate`` - robability of an index to be selected for crossover\
    
``weights`` - weights for weighted bit-flip mutation or weighted uniform crossover\
    
``selection`` - type of selection\
    
``ref_points`` - custom reference points for NSGA3\
    
``verbose`` - if logbook should be printed\
    
``stop_after`` - number of generations without a change in the size of selected subset across all islands to stop after\
    
``create_individual_funct`` - custom function to create the solutions for first generation\
    
    

  
Usage
-----

This package is used by `gatai <https://github.com/lavakin/gatai>`_, you might want to have a look.

Getting optimized solutions and pareto front:

.. code-block:: python

    # Example Usage
    from setga import utils, select_subset

    pop,logbook,gens,logbook, best_sols = select.run_minimizer(num_of_elements_in_the_set, fitness_function, stats_by, stats_names_list, 
                      mutation_rate = 0.001, crossover_rate = 0.02, 
                      pop_size = 150, num_gen = num_generations, num_islands = 8, mutation = "bit_flip", 
                      crossover = "uniform",
                      selection = "SPEA2", frac_init_not_removed = 0.005)


Genetic operators
------------

One can choose from all mutations and crossover DEAP provides for binary EA, where a the uniform crossover and bit-flip mutation operators have been further optimized. It s also possible to provide own genetic operators by passing a function as the mutation or crossover operator. One can also provide a list of mutation of length of the number of islands, if different mutations should be used for different islands. We provide also weighted bit-flip mutation and weighted uniform crossover, where the probability of a index being mutated (crossed over) is proportional to its weight that is passed as the optional argument "weight".

Crossover operators: 
    
    ``"uniform", "onepoint","twopoint","partialy_matched","ordered","uniform_partialy_matched","weighted"``
    
Mutation operators:
    
    ``"bit-flip","inversion", "weighted"``

Selection
----------

One can choose from all multi-objective selection operators DEAP provides. For NSGA3, uniform ref. points are used by default, but other can be specified.

Selection operators: 
    
    ``"SPEA2","NSGA2","NSGA3"``

Contributing
------------

Contributions to this project are welcome. If you have any ideas for improvements, new features, or bug fixes, please submit a pull request. For major changes, please open an issue to discuss the proposed modifications.

License
-------

This project is licensed under the MIT License. Feel free to use and modify the code according to the terms of this license.
