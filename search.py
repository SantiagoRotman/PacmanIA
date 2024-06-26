# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]


# Funcion de busqueda que toma el problema, los estados ya visitados (generalmente ninguno) y la heuristica usada para ordenar los estados
# devuelve las acciones realizadas para llegar a la meta del problema
def search(problem, fringe, heuristic):
    initial_state = problem.getStartState()
    initial_actions = []
    initial_candidate = (initial_state, initial_actions, 0)

    # Usamos isinstance() para diferenciar entre algoritmos que usen priorityQueue (Que necesita que le pasemos la prioridad)
    # y otras estructuras que no lo necesitan
    if isinstance(fringe, util.PriorityQueue):
        fringe.push(initial_candidate, heuristic(initial_state, problem))
    else:
        fringe.push(initial_candidate)
    closed_set = set()

    while not fringe.isEmpty():
        candidate = fringe.pop()
        state, actions, cost = candidate

        if problem.isGoalState(state):
            return actions
        
        if state not in closed_set:
            closed_set.add(state)
            candidate_successors = problem.getSuccessors(state)
            candidate_successors = filter(lambda x: x[0] not in closed_set, candidate_successors) # Filtro los estados ya explorados
            candidate_successors = map(lambda x: (x[0], actions + [x[1]], cost + x[2]), candidate_successors) # Le agrego a todos estados la nueva accion y el nuevo costo total
            for candidate in candidate_successors:
                if isinstance(fringe, util.PriorityQueue):
                    fringe.push(candidate, candidate[2] + heuristic(candidate[0], problem))
                else:
                    fringe.push(candidate)

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """

    #print ("Start:", problem.getStartState())
    #print ("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #print ("Start's successors:", problem.getSuccessors(problem.getStartState()))

    return search(problem, util.Stack(), nullHeuristic)
    

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    return search(problem, util.Queue(), nullHeuristic)

def uniformCostSearch(problem):
    return search(problem, util.PriorityQueue(), nullHeuristic)

    "Search the node of least total cost first."

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    return search(problem, util.PriorityQueue(), heuristic)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
