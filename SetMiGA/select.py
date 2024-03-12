from deap import base, creator, tools
import random
import numpy as np
import array
from SetMiGA import utils

class WrongType(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

# mutation: ["bit_flip","inversion"]
# crossover: ["uniform", "onepoint","twopoint","partialy_matched","ordered","uniform_partialy_matched"],
# selection: ["SPEA2","NGSA2"]
def run_minimizer(set_size,eval_ind, stats_by,stats_names,eval_func_kwargs={},mutation_rate = 0.001,crossover_rate = 0.02, 
                  pop_size = 150, num_gen = 8000, num_islands = 6, mutation = "bit_flip" , 
                  crossover =  "uniform_partialy_matched", selection = "SPEA2",frac_init_not_removed = 0.01,
                  create_individual_funct = None, create_individual_func_kwargs={}):
    """Run minimizer algorithm to optimize individual solutions.

    Parameters:
    - set_size: int, size of the set to be optimized
    - evaluate_individual: function, function to evaluate a single individual
    - eval_func_kwargs: dict, keyword arguments for evaluate_individual function
    - mutation_rate: float, mutation rate for the algorithm
    - crossover_rate: float, crossover rate for the algorithm
    - pop_size: int, population size of the one island of the GA
    - num_gen: int, maximum number of generations
    - num_islands: int, number of islands for the algorithm
    - mutation: str, type of mutation ["bit_flip","inversion"] (see DEAP documentation)
    - crossover: str, type of crossover ["uniform", "onepoint","twopoint","partialy_matched","ordered","uniform_partialy_matched"] (see DEAP documentation)
    - selection: str, type of selection ["SPEA2","NGSA2"] (see DEAP documentation)
    - frac_init_not_removed: float, fraction of initially not removed elements
    - create_individual_funct: function, function to create an individual
    - create_individual_func_kwargs: dict, keyword arguments for create_individual_funct

    Returns:
    - np.array(pop): numpy array, final population (array of binary arrays, 1 for every selected item in the set)
    - pareto_front: list, Pareto front solutions (just the solutions, that are pareto dominant)
    """
    for arg in [mutation_rate, crossover_rate, frac_init_not_removed]:
        if not isinstance(arg, float):
            raise TypeError(f"{arg} must be a float.")

    for arg in [set_size, pop_size, num_gen, num_islands]:
        if not isinstance(arg, int):
            raise TypeError(f"{arg} must be an integer.")

    def create_individual(set_size,frac_init_not_removed):
        a =  round(set_size*frac_init_not_removed)
        b = round(set_size*frac_init_not_removed*3)
        individual = array.array("b",random.choices([0,1], weights=(1, random.randint(a,b)), k=set_size))
        return creator.Individual(individual)
    
    def evaluate_individual(individual,**kwargs):
        fit = eval_ind(individual,**kwargs)
        individual = np.array(individual)
        num_not_removed = np.sum(individual)
        len_removed = set_size - num_not_removed
        return len_removed, *fit


    creator.create("Fitness", base.Fitness, weights=(-1,) * (len(stats_names) + 1))
    creator.create("Individual", array.array,typecode='b', fitness=creator.Fitness)

    toolbox = base.Toolbox()
    if create_individual_funct == None:
        toolbox.register("individual", create_individual, set_size = set_size, frac_init_not_removed = frac_init_not_removed)
    else:
        toolbox.register("individual", lambda ind: create_individual_funct(ind, **create_individual_func_kwargs))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", lambda ind: evaluate_individual(ind, **eval_func_kwargs))
    if mutation == "bit_flip":
        toolbox.register("mutate_low", tools.mutFlipBit, indpb=mutation_rate/2)
        toolbox.register("mutate_high", tools.mutFlipBit, indpb=mutation_rate)
    if mutation == "inversion":
        toolbox.register("mutate_low", tools.mutInversion)
        toolbox.register("mutate_high", tools.mutInversion)
    if mutation not in ["bit_flip","inversion"]:
        raise WrongType("Unknown type of mutation")

    if crossover == "uniform":
        toolbox.register("mate", tools.cxUniform,indpb=crossover_rate)
    if crossover == "onepoint":
        toolbox.register("mate", tools.cxOnePoint)
    if crossover == "twopoint":
        toolbox.register("mate", tools.cxTwoPoint)
    if crossover == "partialy_matched":
        toolbox.register("mate", tools.cxPartialyMatched)
    if crossover == "uniform_partialy_matched":
        toolbox.register("mate", tools.cxUniformPartialyMatched,indpb=crossover_rate)
    if crossover == "ordered":
        toolbox.register("mate", tools.cxOrdered)
    if crossover not in ["uniform", "onepoint","twopoint","partialy_matched","ordered","uniform_partialy_matched"]:
        raise WrongType("Unknown type of crossover")

    if selection == "SPEA2":
        toolbox.register("select", tools.selSPEA2)
    if selection == "NGSA2":
        toolbox.register("select", tools.selNGSA2)
    
    toolbox.register("migrate",tools.migRing,k=10,selection = toolbox.select)

    stats = tools.Statistics()

    for i,s in enumerate(["Num removed"] + stats_names):
        stats.register(s, lambda x, i=i, stats_by=stats_by: x[np.argmin([ind.fitness.values[stats_by] for ind in x])].fitness.values[i])
    
    mut_functs = [toolbox.mutate_high if i+1 < num_islands * 0.4 else toolbox.mutate_low for i in range(num_islands)]

    islands = [toolbox.population(n=pop_size) for _ in range(num_islands)]
    population, _ = utils.eaMuPlusLambda_stop_isl(islands,toolbox, mu=round(len(islands[0])), lambda_ = len(islands[0]),cxpb=0.45, mutpb=0.45, ngen=num_gen, mut_functs_isl=mut_functs,stats=stats, verbose=True)

    pop = [solution for island in population for solution in island]

    pareto_front = tools.sortNondominated(pop, k=pop_size*num_islands,first_front_only=True)
    return np.array(pop),pareto_front

