import time


class State:

    def __init__(self, leftCannibals, leftMissionaries, rightCannibals, rightMissionaries, boatPosition):  # data for
        # all states
        self.leftCannibals = leftCannibals  # number of left cannibals
        self.leftMissionaries = leftMissionaries  # number of left missionaries
        self.rightCannibals = rightCannibals  # number of right cannibals
        self.rightMissionaries = rightMissionaries  # number of right missionaries
        self.boatPosition = boatPosition  # position of boat 'L' for left or 'R' for right
        self.parent = None  # current parent of state
        self.info = "{" + str(leftCannibals) + ", " + str(leftMissionaries) + ", " + str(rightCannibals) + ", " + str(
            rightMissionaries) + ", " + boatPosition + "}"  # string information for state to see
        self.g = 0  # depth of state
        self.h = 0  # heuristic cost of state
        self.f = 0  # total cost for state

    def __eq__(self, other):  # operator '==' for states
        return self.leftCannibals == other.leftCannibals and \
               self.leftMissionaries == other.leftMissionaries and \
               self.rightCannibals == other.rightCannibals and \
               self.rightMissionaries == other.rightMissionaries and \
               self.boatPosition == other.boatPosition  # check if all data are exact

    def heuristic(self):  # heuristic cost
        self.h = (self.leftCannibals + self.leftMissionaries) / M + self.g
        # heuristic -> people on left side / capacity + depth of current state

    def crossToRight(self, cN, mN):  # check if the boat can cross right
        if self.boatPosition == 'R':
            return False
        if cN + mN > M:
            return False
        if cN + mN < 1:
            return False
        if self.leftCannibals - cN < 0 or self.leftMissionaries - mN < 0:
            return False
        if self.rightCannibals + cN > self.rightMissionaries + mN != 0:
            return False
        if self.leftCannibals - cN > self.leftMissionaries - mN != 0:
            return False
        return True

    def crossToLeft(self, cN, mN):  # check if the boat can cross left
        if self.boatPosition == 'L':
            return False
        if cN + mN > M:
            return False
        if cN + mN < 1:
            return False
        if self.rightCannibals - cN < 0 or self.rightMissionaries - mN < 0:
            return False
        if self.leftCannibals + cN > self.leftMissionaries + mN != 0:
            return False
        if self.rightCannibals - cN > self.rightMissionaries - mN != 0:
            return False
        return True

    def setParent(self, parent):  # when we create the children for each state we set its parent
        self.parent = parent

    def getChildren(self):
        #  print("Next State ->" + " " + str(self.info))
        children = []  # list for states' children
        if self.boatPosition == 'L':
            for i in range(self.leftCannibals + 1):
                for j in range(self.leftMissionaries + 1):
                    if self.crossToRight(i, j):
                        child = State(self.leftCannibals - i, self.leftMissionaries - j, self.rightCannibals + i,
                                      self.rightMissionaries + j, 'R')  # we check all possible transfers for the boat
                        # after we create the child before we put it in the list, we set all remaining characteristics
                        child.setParent(self)
                        child.heuristic()
                        child.getDepth()
                        children.append(child)
        elif self.boatPosition == 'R':
            for i in range(self.rightCannibals + 1):
                for j in range(self.rightMissionaries + 1):
                    if self.crossToLeft(i, j):
                        child = State(self.leftCannibals + i, self.leftMissionaries + j, self.rightCannibals - i,
                                      self.rightMissionaries - j, 'L')  # we check all possible transfers for the boat
                        # after we create the child before we put it in the list, we set all remaining characteristics
                        child.setParent(self)
                        child.heuristic()
                        child.getDepth()
                        children.append(child)

        #  if len(children) > 0:  # print all possible children
        # print("     Children:     ")
        # for c in children:
        # print("  " + c.info)

        return children

    def getDepth(self):  # method to find state's depth g
        current_state = self
        g = 0
        while current_state.parent is not None:
            g += 1
            current_state = current_state.parent
        self.g = g
        return g

    def getTotalCost(self):  # method to find total cost f
        f = self.g + self.h
        self.f = f
        return f

    def isGoal(self):  # check if current state is goal
        return self == goal


def A_Star():  # A* algorithm
    current_state = start  # we begin from the very first state {N, N, 0, 0, 'L'}
    if current_state.isGoal():  # check if the current state is our goal
        return current_state
    frontier = list()  # open list
    closed = []  # closed set
    frontier.append(current_state)  # first we put current state(starting state) in the frontier
    while frontier:  # while len(frontier) > 0:
        cost = list()  # list with all states' costs
        for s in frontier:  # s is every state inside frontier
            cost.append(s.getTotalCost())  # we add the f cost of s state
        index = cost.index(min(cost))  # we use index to find the position of the minimum cost inside the list cost
        state = frontier.pop(index)  # we remove the state with the minimum cost
        if state.isGoal():  # check if state is our goal
            return state
        closed.append(state)  # we add state in the closed set
        children = state.getChildren()  # we find all possible children of state
        for child in children:  # for each child
            if (child in closed) and (state.g < child.g):  # if the child is already in the closed set and 'above'
                # the state then we put it 'under' the state, which is its new parent
                child.g = state.g
                child.parent = state
            elif (child in frontier) and (state.g < child.g):  # if the child is already in the frontier and 'above'
                # the state then we put it 'under' the state, which is its new parent
                child.g = state.g
                child.parent = state
            else:
                frontier.append(child)
                child.g = state.g


def print_solution(solution):
    transfers = 0
    path = list()
    path.append(solution)
    try:
        parent = solution.parent
    except AttributeError:
        print("NO VALID PATH FOUND")
    else:
        while parent:
            path.append(parent)
            parent = parent.parent
        print("Beginning state: " + start.info)
        transfers = transfers + 1
        for i in range(1, len(path)):
            state = path[len(path) - i - 1]
            if i == len(path) - 1:
                print("Objective state: " + goal.info)
            else:
                print("Current State: " + state.info)
                transfers = transfers + 1
        print("Total boat transfers: " + str(transfers))
        if solution is not None and transfers <= K:
            print("Boat transfers are less or equal to " + str(K))
            print("OBJECTIVE COMPLETE")
        elif solution is not None and transfers > K:
            print("Boat transfers are more than " + str(K))
            print("OBJECTIVE FAILED")
        else:
            print("NO VALID PATH FOUND")


Time_Start = time.time()
# Input
try:
    N = int(input("Give number of cannibals/missionaries: "))  # number of missionaries or cannibals, in total 2N
    M = int(input("Give maximum boat capacity: "))  # number of seats in the boat
    K = int(input("How many times you wish the boat moves?: "))  # number of seats in the boat
    if N == 0 or M < 2 or K == 0:
        print("Invalid input can't find path!")
except ValueError:
    print("\nInvalid input can't find path!")
else:
    start = State(N, N, 0, 0, 'L')
    goal = State(0, 0, N, N, 'R')
    result = A_Star()
    print_solution(result)
Time_End = time.time()
print("Real time duration: " + str(Time_End - Time_Start))
