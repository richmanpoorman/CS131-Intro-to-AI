import random

FAILED = -1
RUNNING = 0
SUCCESS = 1

# Blackboard
blackboard = {
    "battery"          : 100,
    "spotCleaning"     : False,
    "generalCleaning"  : False,
    "dustySpot"        : False,

    "homePath"         : "",
    "timer"            : -1,
    "timerRunning"     : False,
}

# Base class
class Node:
    def run(self):
        def __init__(self):
            pass
        return FAILED

class Task(Node):
    def __init__(self):
        super().__init__()

    def run(self):
        return FAILED

class Condition(Node):
    def __init__(self):
        super().__init__()
    
    def run(self):
        return FAILED

class Composite(Node):
    def __init__(self, children):
        super().__init__()
        self.children = children
        self.currEval = 0
    
    def run(self):
        return FAILED

class Decorator(Node):
    def __init__(self, child):
        super().__init__()
        self.child = child
    
    def run(self):
        return FAILED

# Composites
class Sequence(Composite):
    def __init__(self, children):
        super().__init__(children)
    
    def run(self):
        
        for i in range(self.currEval , len(self.children)):
            # print("Sequence", i)
            self.currEval = i
            child = self.children[i]
            val = child.run()
            # If it is running or a fail
            
            if val == RUNNING:
                return RUNNING

            if val == FAILED:
                self.currEval = 0
                return FAILED
        
        self.currEval = 0
        return SUCCESS

class Selector(Composite):
    def __init__(self, children):
        super().__init__(children)
    
    def run(self):
        
        for i in range(self.currEval , len(self.children)):
            # print("Selector", i)
            self.currEval = i
            child = self.children[i]
           
            val = child.run()
            # If it is a success or Running
            if val == RUNNING:
                return RUNNING
            
            if val == SUCCESS:
                self.currEval = 0
                return SUCCESS
        
        self.currEval = 0
        return FAILED

class Priority(Composite):
    def __init__(self, priority, children):
        super().__init__(children)
        self.priority = priority

    def run(self):
        for idx in self.priority:
            # print("priority", idx)
            
            # If it is the index that we know that there is a running on, return running
            
            val = self.children[idx - 1].run()
            if val == RUNNING:
                return RUNNING
            
            if val == SUCCESS:
                resetComposites(self.children[self.currEval])
                clearRunning()
                return SUCCESS
        
        resetComposites(self.children[self.currEval])
        clearRunning()
        return FAILED

# Decorator
class Timer(Decorator):
    def __init__(self, child, time):
        super().__init__(child)
        self.time = time
        
    def run(self):
        
        
        if blackboard["timerRunning"] and blackboard["timer"] < 0:
            blackboard["timerRunning"] = False
            return SUCCESS

        if not blackboard["timerRunning"]:
            blackboard["timer"] =  self.time
            blackboard["timerRunning"] = True
            
        
        print("Timer: ", blackboard["timer"])
        self.child.run()
        return RUNNING
        
class UntilFail(Decorator):
    def __init__(self, child):
        super().__init__(child)
    
    def run(self):
        print("Until Fail")
        if self.child.run() == FAILED:
            return SUCCESS
        return RUNNING

# Tasks
class FindHome(Task):
    def __init__(self):
        super().__init__()
    
    def run(self):
        path = input("Path Home: ")
        print("Got path: " + path)
        if (path == ""):
            return FAILED
        blackboard["homePath"] = path
        return SUCCESS

class GoHome(Task):
    def __init__(self):
        super().__init__()
    
    def run(self):
        print(blackboard["homePath"])
        return SUCCESS
    
class Dock(Task):
    def __init__(self):
        super().__init__()
    
    def run(self):
        print("Docked")
        blackboard["battery"] = 100
        return SUCCESS

class CleanSpot(Task):
    def __init__(self):
        super().__init__()

    def run(self):
        if blackboard["dustySpot"]:
            print("Cleaning Dust")
            return SUCCESS
        print("Clean Spot")
        return FAILED

class DoneSpot(Task):
    def __init__(self):
        super().__init__()

    def run(self):
        print("Spot Done")
        blackboard["dustySpot"]    = False
        blackboard["spotCleaning"] = False
        return SUCCESS

class CleanFloor(Task):
    def __init__(self):
        super().__init__()
    
    def run(self):
        print("Clean floor")
        if random.randint(0, 100) < 1:
            return FAILED
        return SUCCESS

class DoneGeneral(Task):
    def __init__(self):
        super().__init__()
    
    def run(self):
        print("Done General")
        blackboard["generalCleaning"] = False
        return SUCCESS

class DoNothing(Task):
    def __init__(self):
        super().__init__()

    def run(self):
        print("Do Nothing :(")
        return FAILED

# Conditionals
class BatteryCheck(Condition):
    def __init__(self):
        super().__init__()

    def run(self):
        blackboard["battery"] -= 1
        print("Battery: ", blackboard["battery"])
        
        if blackboard["battery"] < 30:
            return SUCCESS
        return FAILED

class SpotCleaning(Condition):
    def __init__(self):
        super().__init__()

    def run(self):
        blackboard["spotCleaning"] = toBoolString(input("Spot Cleaning? (True or False): "))
        if blackboard["spotCleaning"]:
            return SUCCESS
        return FAILED

class GeneralCleaning(Condition):
    def __init__(self):
        super().__init__()

    def run(self):
        blackboard["generalCleaning"] = toBoolString(input("General Cleaning? (True or False): "))
        if blackboard["generalCleaning"]:
            return SUCCESS
        return FAILED

class DustySpot(Condition):
    def __init__(self):
        super().__init__()

    def run(self):
        blackboard["dustySpot"] = toBoolString(input("Is it dusty? (True or False): "))
        if blackboard["dustySpot"]:
            return SUCCESS
        return FAILED


def toBoolString(inputVal):
    if inputVal == "true" or inputVal == "True":
        return True
    return False

# Tree
root = Priority([1, 2, 3], [
    Sequence([
        BatteryCheck(),
        FindHome(),
        GoHome(),
        Dock()
    ]),
    Selector([
        Sequence([
            SpotCleaning(),
            Timer(CleanSpot(), 20),
            DoneSpot()
        ]),
        Sequence([
            GeneralCleaning(),
            Sequence([
                Priority([1, 2], [
                    Sequence([
                        DustySpot(),
                        Timer(CleanSpot(), 35)
                    ]),
                    UntilFail(CleanFloor())
                ])
            ]),
            DoneGeneral()
        ])
    ]),
    DoNothing()
])


def clearRunning():
    # blackboard["runningStack"].clear()
    blackboard["timer"]            = -1
    blackboard["timerRunning"]     = False

def resetComposites(composite):
    if not isinstance(composite, Composite):
        return
    resetComposites(composite.children[composite.currEval])
    composite.currEval = 0


# Initial input
blackboard["battery"] = int(input("The starting battery power: "))
# Loop Checks
while True:
    if blackboard["timer"] >= 0:
        blackboard["timer"] -= 1
    # Go through the list, (it should be priority queues up until the end), then run that last function;
    # If a priority return success, then something else is running
    # If it is not running, then just delete everything
    # Assume list only gets deleted when it finds something else
    '''
    if blackboard["runningStack"]:
        print("STACK:")
        for x in blackboard["runningStack"]:
            print(x) 

        for i in range(0, len(blackboard["runningStack"])):
            x = blackboard["runningStack"][i]
            if isinstance(x[0], Priority): # If it is a priority
                if x[0].runUntil(x[1]) == SUCCESS: # If the priority finds something else, do that first
                    clearRunningStack()
                    break
            elif x.run() != RUNNING: # If the running function we were waiting for evaluates to something else
                clearRunningStack()
                break
        continue
    '''
    root.run()
    