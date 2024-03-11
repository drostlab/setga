import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np 
from deap import tools
import os
import concurrent.futures
import random


class SolutionException(Exception):
    def __init__(self, message):
        super().__init__(message)
        
# same as in the DEAP library except for enabeling different mutations for different a
def varOr(population, toolbox, lambda_, cxpb, mutpb,mutate_funct):
    assert (cxpb + mutpb) <= 1.0, (
        "The sum of the crossover and mutation probabilities must be smaller "
        "or equal to 1.0.")

    offspring = []
    for _ in range(lambda_):
        op_choice = random.random()
        if op_choice < cxpb:            # Apply crossover
            ind1, ind2 = [toolbox.clone(i) for i in random.sample(population, 2)]
            ind1, ind2 = toolbox.mate(ind1, ind2)
            del ind1.fitness.values
            offspring.append(ind1)
        elif op_choice < cxpb + mutpb:  # Apply mutation
            ind = toolbox.clone(random.choice(population))
            ind, = mutate_funct(ind)
            del ind.fitness.values
            offspring.append(ind)
        else:                           # Apply reproduction
            offspring.append(random.choice(population))

    return offspring


def eaMuPlusLambda_stop_isl(islands, toolbox, mu, lambda_, cxpb, mutpb, ngen,mut_functs_isl: list, stats = None, stop_after = 100, verbose=__debug__):
    
    def isl_evaluate(invalid_ind):
        return list(toolbox.map(toolbox.evaluate, invalid_ind))
    
    def isl_select(island):
        return toolbox.select(island, mu)
    
    def isl_evolve(island,i):
        return varOr(island, toolbox, lambda_, cxpb, mutpb,mut_functs_isl[i])
    
    def comp_fitness_inv(island):
        inv_ind = [ind for ind in island if not ind.fitness.valid]
        fitnesses = isl_evaluate(inv_ind)
        for ind, fit in zip(inv_ind, fitnesses):
                ind.fitness.values = fit

    
    def island_evolve(island,i):
        offsprings  = isl_evolve(island,i)
        comp_fitness_inv(island)
        comp_fitness_inv(offsprings)
        return isl_select(offsprings + island)
    
    def migrate(islands,gen):
        if min([min(islands[i], key=lambda ind: ind.fitness.values[1]).fitness.values[1] for i in range(len(islands))]) > 0:
            if gen%5 == 0:
                toolbox.migrate(islands)
        else:
            if gen%10 == 0:
                toolbox.migrate(islands)

    def should_stop(islands,prev_max_len,max_len_counter,stop_after):
        max_len = min([min(islands[i], key=lambda ind: ind.fitness.values[1]).fitness.values[0] for i in range(len(islands))])
        if prev_max_len == max_len:
            max_len_counter += 1
        else:
            prev_max_len = max_len
            max_len_counter = 1
        if max_len_counter > stop_after:
            return True,prev_max_len,max_len_counter
        return False,prev_max_len,max_len_counter
    
    def log_results(islands,gen):
        for i in range(len(islands)):
            record = stats.compile(islands[i]) if stats is not None else {}
            logbook.record(gen=gen, island = i+1, **record)
            if verbose:
                print(logbook.stream)
        if verbose:        
            print("\n")


    executor = concurrent.futures.ThreadPoolExecutor()

    logbook = tools.Logbook()
    logbook.header = ['gen'] + ['island'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    fitnesses = list(executor.map(comp_fitness_inv, islands))

    record = stats.compile(islands[0]) if stats is not None else {}
    logbook.record(gen=0, islands = 0, **record)
    if verbose:
        print(logbook.stream)

    prev_max_len = 0
    max_len_counter = 1
    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Vary the population
        islands = list(executor.map(island_evolve, islands,range(len(islands))))

        # Update the statistics with the new population

        log_results(islands,gen)
        stop,prev_max_len,max_len_counter = should_stop(islands,prev_max_len,max_len_counter,stop_after)   
        if stop:
            break
        migrate(islands,gen)    

    return islands, logbook


def get_sol_from_indices(indices,ind_len):
    ones = np.ones(ind_len)
    ones[indices] = 0
    return ones

def get_removed_from_solution(solution,names):
    return np.array(names[np.where(solution == 0)[0]])

def plot_pareto(pareto,par,folder,upper_bound = None,lower_bound = None):
    plt.scatter(pareto[:,0],pareto[:,1],s = 1.5,color='blue', marker='o', label='Solution')
    plt.scatter(par[:,0],par[:,1],s = 5,color='red', marker='o', label='Front')
    #plt.gca().invert_yaxis()
    #plt.gca().invert_xaxis()

    plt.xlabel('Number of extracted genes')  # X-axis label
    plt.ylabel('p-value')  # Y-axis label

    plt.title('Solution extraction')  # Title

    plt.legend()  # Show legend

    plt.grid(True, linestyle='--', alpha=0.7)  # Add gridlines

    plt.xticks(fontsize=12)  # Customize tick labels
    plt.yticks(fontsize=12)
    selected = pareto[np.logical_and(pareto[:,1] < 0.5,pareto[:,1] >= 0.1)][:,0]
    if len(selected) == 0:
        raise SolutionException("No solution found")
    
    if upper_bound is not None:
        plt.axhline(y=upper_bound, color='red', linestyle='--', linewidth=2)
    if lower_bound is not None:
        plt.axhline(y=lower_bound, color='red', linestyle='--', linewidth=2)
    # Add the Rectangle patch to the current plot¨
    # Save or display the plot
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    # Save the plot as an image
    return plt
    
    #plt.show()

def get_results_from_pareto(solutions,pareto,folder,names):
    pareto_filtered = pareto[np.logical_and(pareto[:,1] < 0.5,pareto[:,1] > 0.1)]
    pareto_filtered = pareto
    solutions = solutions[np.logical_and(pareto[:,1] < 0.5,pareto[:,1] > 0.1)]
    solutions = solutions
    if len(pareto_filtered) == 0:
        raise SolutionException("No solution found")
    min_v = min(pareto_filtered[:,0])
    sel_sols  = solutions[pareto_filtered[:,0] < min_v + min_v *0.2]
    
    genes = get_removed_from_solution(get_sol_from_indices(np.where(len(sel_sols) - sel_sols.sum(axis=0) >= len(sel_sols*0.8))[0],sel_sols.shape[1]),names)
    np.savetxt(os.path.join(folder,"extracted_genes.txt"),genes, fmt="%s")


def get_results(solutions,fitness,folder,names,upper_bound = 0.4, lower_bound = 0, min_freq = 0.65):
    fitness_filtered = fitness[np.logical_and(fitness[:,1] < upper_bound,fitness[:,1] >= lower_bound)]
    #pareto_filtered = pareto
    solutions = solutions[np.logical_and(fitness[:,1] < upper_bound,fitness[:,1] >= lower_bound)]
    sel_sols = solutions
    if len(fitness_filtered) == 0:
        raise SolutionException("No solution found")
    
    sel_sols = np.unique(sel_sols,axis = 0)
    genes = get_removed_from_solution(get_sol_from_indices(np.where(sel_sols.sum(axis=0) <= len(sel_sols)*(1- min_freq))[0],sel_sols.shape[1]),names)
    return genes
