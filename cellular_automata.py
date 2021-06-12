"""Simple code for a Wolfram elementary cellular automata in python"""

import os
import time
import numpy as np
from skimage.io import imsave

def define_rule_sets(set_size):

    """Find every possible rule for given set size"""

    rule_sets = []

    for n in range(1<<set_size):
        s = bin(n)[2:]
        s = '0'*(set_size-len(s))+s
        rule_sets.append((list(map(int, list(s)))))
        
    return rule_sets

def apply_rules(l, m, r, rules):

    """Apply selected rule to cell
    
    Apply rule to cell given its current state m and neighbours 
    states l and r.
       
    Args:
        l: left neighbour cell state.
        m: current cell state.
        r: right neighbour cell state.
        rules: array current rule.
    """

    if l == 1 and m == 1 and r == 1:
        return rules[0]
    if l == 1 and m == 1 and r == 0:
        return rules[1]
    if l == 1 and m == 0 and r == 1:
        return rules[2]
    if l == 1 and m == 0 and r == 0:
        return rules[3]
    if l == 0 and m == 1 and r == 1:
        return rules[4]
    if l == 0 and m == 1 and r == 0:
        return rules[5]
    if l == 0 and m == 0 and r == 1:
        return rules[6]
    if l == 0 and m == 0 and r == 0:
        return rules[7]

def update_ca(current, rules):
    
    """Get next ca state given current state
    
    Get the next generations state from the current cell map for a 
    specified rule.
       
    Args:
        current: array of current cell states.
        rules: array current rule.
    """

    next_generation = np.ndarray([current.size])
    
    i = 0
    while i < current.size:
        
        if i == 0:
            left = current[map_size-1]
        else:
            left = current[i-1]
        
        me = current[i]
        
        if i == map_size-1:
            right = current[0]
        else:
            right = current[i+1]
            
        next_generation[i] = apply_rules(left, me, right, rules)
    
        i+=1
    
    return next_generation

def run_ca(generations, map_size, rule_sets):

    """Run the CA
    
    Run CA for a number of generations for all possible
    rules, and save each rule image.
       
    Args:
        generations: int number of generations to iterate.
        map_size: int number of cells in each generation.
        rule_sets: list of rules to implement.
    """
    
    final_img = np.ndarray((map_size, generations)).astype(np.uint8)

    rule_n = 0

    for rs in rule_sets:

        cell_map = np.zeros([map_size])
        cell_map[int(map_size/2)] = 1

        for r in range(generations):

            final_img[:,r] = cell_map[:]
            final_img[final_img == 1] = 255
            
            #print(cell_map)
            #time.sleep(0.1)
            
            next_generation = update_ca(cell_map, rs)
            cell_map[:] = next_generation[:]

        imsave(os.path.join('outputs','{0}{1}'.format(rule_n,'_ca.png')), final_img.T)
        
        rule_n+=1

if __name__ == '__main__':

    generations = 100
    map_size = 100

    rule_sets = define_rule_sets(8)
    run_ca(generations, map_size, rule_sets)