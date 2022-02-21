from tempfile import TemporaryFile
import picos as pic
from picos import RealVariable
from copy import deepcopy
from heapq import *
import heapq as hq
import numpy as np
import itertools
import math
counter = itertools.count() 

class BBTreeNode():
    def __init__(self, vars = [], constraints = [], objective='', prob=None):
        self.vars = vars
        self.constraints = constraints
        self.objective = objective
        self.prob = prob

    def __deepcopy__(self, memo):
        '''
        Deepcopies the picos problem
        This overrides the system's deepcopy method bc it doesn't work on classes by itself
        '''
        newprob = pic.Problem.clone(self.prob)
        return BBTreeNode(self.vars, newprob.constraints, self.objective, newprob)
    
    def buildProblem(self):
        '''
        Bulids the initial Picos problem
        '''
        prob=pic.Problem()
   
        prob.add_list_of_constraints(self.constraints)    
        
        prob.set_objective('max', self.objective)
        self.prob = prob
        return self.prob

    def is_integral(self):
        '''
        Checks if all variables (excluding the one we're maxing) are integers
        '''
        for v in self.vars[:-1]:
            if v.value == None or abs(round(v.value) - float(v.value)) > 1e-4 :
                return False
        return True

    def branch_floor(self, branch_var):
        '''
        Makes a child where xi <= floor(xi)
        '''
        n1 = deepcopy(self)
        n1.prob.add_constraint( branch_var <= math.floor(branch_var.value) ) # add in the new binary constraint

        return n1

    def branch_ceil(self, branch_var):
        '''
        Makes a child where xi >= ceiling(xi)
        '''
        n2 = deepcopy(self)
        n2.prob.add_constraint( branch_var >= math.ceil(branch_var.value) ) # add in the new binary constraint
        return n2


    def bbsolve(self):
        '''
        Use the branch and bound method to solve an integer program
        This function should return:
            return bestres, bestnode_vars

        where bestres = value of the maximized objective function
              bestnode_vars = the list of variables that create bestres
        '''

        # these lines build up the initial problem and adds it to a heap
        root = self
        res = root.buildProblem().solve(solver='cvxopt')
        heap = [(res, next(counter), root)]
        bestres = -1e20 # a small arbitrary initial best objective value
        bestnode_vars = root.vars # initialize bestnode_vars to the root vars

        while len(heap) > 0:
            _, _, node = hq.heappop(heap) # pop a node

            # solve problem
            try:
                new_res = node.prob.solve(solver="cvxopt")
                print(f"Objective value: {node.prob.value}")
            except:
                print("Infeasible, pruned")
                pass
            
            # check if objective value is less than bestres (prune)
            if new_res.value <= bestres:
                print("Not better than current best, pruned")
                pass
                
            elif node.is_integral(): # new best solution
                print(f"New best solution objective: {node.prob.value}")
                bestres = float(node.prob.value)
                bestnode_vars = [float(v.value) for v in node.vars]
                print(f"New best solution variable values: {bestnode_vars}")
            
            else: #branch
                for v in node.vars:
                    # get first non integer
                    if abs(float(v) - round(v)) > 1e-4:
                        # add floor
                        hq.heappush(heap, (float(bestres), next(counter), node.branch_floor(v)))

                        # add ceil
                        hq.heappush(heap, (float(bestres), next(counter), node.branch_ceil(v)))
                        break
                    
        return bestres, bestnode_vars
 

def problem1():
    print("Problem 1")
    fail_count = 0

    x = RealVariable("x")
    y = RealVariable("y")
    z = RealVariable("z")
    vars = [x, y, z]
    objective = z
    constraints = [z == x + y, -5*x + 4* y <= 0, 6*x+2*y <= 17, x >= 0, y >= 0]
    root = BBTreeNode(constraints = constraints, objective = objective, vars = vars)
    res, sol_vars = root.bbsolve()
    print(f"res: {res}, sol_vars: {sol_vars}")
    correct_vals = [2.0, 2.0, 4.0]

    check_index = 0

    while check_index < len(correct_vals):
        try:
            assert(abs(correct_vals[check_index] - float(sol_vars[check_index])) < 1e-4)
        except AssertionError:
            print("Test case 1 failed on variable at index " + str(check_index))
            fail_count = 1
        check_index += 1

    return fail_count

problem1()
