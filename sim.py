#!/usr/bin/python
'''
sim.py

This program provides a visual simulation of how A* and ACO behave when
they have imperfect information in a dynamic environment---think "fog 
of war" in RTS games, or the network topology in Internet routing.

'''

##########################
#        SETTINGS        #
##########################

# TODO: Set these via command line invocation?
ALGORITHM_ANT = 0
ALGORITHM_ASTAR = 1
ALGORITHM_DLITE = 0

ASTAR_REUSE_PATH = 0
ASTAR_TIMESLICE = 5    # Consider this depth-limited A*.
                        # To disable, set to 0

ANT_ELITIST = 1
ANT_USE_GLOBAL = 0
ANT_DIFFUSE_PHEROMONES = 0


EVAPORATION_FACTOR = 0.5
PHEROMONE_DROP_AMOUNT = 5

AGENT_VIEW_RADIUS = 3

UPDATE_PERIOD = 1280
NUM_AGENTS = 1

MAP_SIZE = 12
UPDATE_SPEED = 60



ALPHA = 0.8
BETA = 0.2

FIRST_CHANCE = 20
SECOND_CHANCE = 40

DRAW_PHEROMONES = 1

ANT_FORWARD_WEIGHT = 10
ANT_BACKWARD_WEIGHT = 1
ANT_SIDEWAYS_WEIGHT = 5

##########################

import wx
import wx.lib.plot
import random
from random import randint
import sys

class Sim(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(380, 380))

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('0')
        self.board = Board(self)
        self.board.SetFocus()
        self.board.start()

        self.Centre()
        self.Show(True)
       

class Board(wx.Panel):
    BoardWidth = MAP_SIZE
    BoardHeight = MAP_SIZE
    Speed = UPDATE_SPEED
    ID_TIMER = 1

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.FULL_REPAINT_ON_RESIZE)

        self.timer = wx.Timer(self, Board.ID_TIMER)
        #self.curX = 0
        #self.curY = 0
        self.map = Map() # Map object, for updating, etc.
        self.board = self.map.map
        
        self.numTicks = 0
        self.agents = [Agent() for x in range(NUM_AGENTS)]
        self.currentSolution = []  # for ACO to store best current solution

        self.isStarted = False
        self.isPaused = False

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_TIMER, self.OnTimer, id=Board.ID_TIMER)
        
        self.SetBackgroundColour('#CCCCCC')

    #def shapeAt(self, x, y):
        #return self.board[(y * Board.BoardWidth) + x]

    #def setShapeAt(self, x, y, shape):
        #self.board[(y * Board.BoardWidth) + x] = shape
        
    def getStatus(self):
        a = "TICKS: %d; " % self.numTicks
        b = "TRIPS: %d; " % sum([x.trips for x in self.agents])
        c = "NODES EXPANDED: %d" % sum([x.nodesExpanded for x in self.agents])
        return a+b+c

    def squareWidth(self):
        return self.GetClientSize().GetWidth() / float(Board.BoardWidth)

    def squareHeight(self):
        return self.GetClientSize().GetHeight() / float(Board.BoardHeight)

    def start(self):
        if self.isPaused:
            return

        self.isStarted = True

        self.timer.Start(Board.Speed)

    def pause(self):
        if not self.isStarted:
            return
        
        self.isPaused = not self.isPaused
        statusbar = self.GetParent().statusbar
        
        if self.isPaused:
            self.timer.Stop()
            statusbar.SetStatusText('paused')
        else:
            self.timer.Start(Board.Speed)
            statusbar.SetStatusText(self.getStatus())
            self.Refresh()
        self.Refresh()

    def OnPaint(self, event):
        '''
        We want to paint:
        
        1) The current real map
        2) The current known map <-- overlayed on real map ?
        3) Current agent positions
        4) Current path (for a single agent in A*? Overall for ACO.)
        5) Pheromone levels (for ACO)---draw as # in upper right corner
           of square? Need to look up how to do that.
        '''

        dc = wx.PaintDC(self)        

        size = self.GetClientSize()
        boardTop = size.GetHeight() - Board.BoardHeight * self.squareHeight()
        
        # Build the "display board"---combines real+known map
        displayBoard = [ [0 for y in range(self.map.size)] for x in range(self.map.size) ]
        trueMap = self.map.getMap()
        knownMap = self.map.getKnownMap()
        
        # Combine real+known maps
        for x, col in enumerate(displayBoard):
            for y, cell in enumerate(col):
                if trueMap[x][y] == Map.EMPTY and knownMap[x][y] == Map.EMPTY:
                    displayBoard[x][y] = Map.EMPTY
                elif trueMap[x][y] == Map.EMPTY and knownMap[x][y] == Map.FILLED:
                    displayBoard[x][y] = Map.FILLED_NOW_EMPTY
                elif trueMap[x][y] == Map.FILLED and knownMap[x][y] == Map.EMPTY:
                    displayBoard[x][y] = Map.EMPTY_NOW_FILLED
                elif trueMap[x][y] == Map.FILLED and knownMap[x][y] == Map.FILLED:
                    displayBoard[x][y] = Map.FILLED
        
        # Draw display board
        for i in range(Board.BoardWidth):
            for j in range(Board.BoardHeight):
                shape = displayBoard[i][j]
                
                if shape != Map.EMPTY:
                    self.drawSquare(dc,
                        0 + i * self.squareWidth(),
                        boardTop + j * self.squareHeight(), shape)
                
        
        # Draw current path
        # For A*, draw for just the first agent? (since we'll typically run with only one)
        # For ACO, draw the global solution.
        if ALGORITHM_ASTAR:
            # TODO: Do we want to track the *entire* path as well?
            # Could do "steps taken" + path - overlap
            path = self.agents[0].stepsTaken + list(reversed(self.agents[0].path))
        if ALGORITHM_ANT:
            path = self.map.globalSolution
        if len(path)>1:
            #print "PATH: ",
            #print path
            self.drawPathLine(dc, path)
            #for pos1, pos2 in [(path[i], path[i+1]) for i in range(0, len(path)-1, 2)]:
                # TODO: draw square in path.
                # Highlighy square in a different color?
                # *Draw line between square centers.
            #    self.drawPathLine(dc, pos1, pos2)
                
        
        # Draw agents
        # Ideally this would have some amount of alpha so the points
        # would get darker the more agents are in one square
        for agent in self.agents:
            x,y = agent.pos
            self.drawAgent(dc,
                0 + (x+0.5) * self.squareWidth(),
                boardTop + (y+0.5) * self.squareHeight())
        
        # Draw pheromones
        if ALGORITHM_ANT and DRAW_PHEROMONES:
            for x,col in enumerate(self.map.pheromones):
                for y,val in enumerate(col):
                    if round(val,3) > 0:
                        # TODO: Draw phermones in [x][y]
                        self.drawPheromone(dc, x, y, round(val,3))
        
    
    def OnKeyDown(self, event):
        if not self.isStarted:
            event.Skip()
            return

        keycode = event.GetKeyCode()

        if keycode == ord('P') or keycode == ord('p'):
            self.pause()
            return
        # If paused and you press SPACE, single step
        #if self.isPaused and keycode == wx.WXK_SPACE:
        #    self.oneStep()
        #    return
        if self.isPaused:
            return
        else:
            event.Skip()


    def OnTimer(self, event):
        if event.GetId() == Board.ID_TIMER:
            # Increment our tick count
            self.numTicks += 1
            # Update all our agents
            for agent in self.agents:
                agent.update(self.map)
            if ALGORITHM_ANT:
                self.map.attenuatePheromones()
            # We update the map, if needed
            if (self.numTicks % UPDATE_PERIOD) == 0:
                self.map.update()
            
            # Update status bar
            statusbar = self.GetParent().statusbar
            statusbar.SetStatusText(self.getStatus())
            self.Refresh()
        else:
            event.Skip()


    def drawPathLine(self, dc, path): #pos1, pos2):
        size = self.GetClientSize()
        boardTop = size.GetHeight() - Board.BoardHeight * self.squareHeight()
        pen = wx.Pen("#999999", min(self.squareHeight(), self.squareWidth())*0.1)
        dc.SetPen(pen)
        
        # Turn points into coords on display
        def toCoords( pos ):
            x = (pos[0]+0.5)*self.squareWidth()
            y = (pos[1]+0.5)*self.squareHeight()
            return (x,y)
            
        path = map(toCoords, path)
        
        line = wx.lib.plot.PolyLine( path, colour="#999999" )
        line.draw(dc, min(self.squareHeight(), self.squareWidth())*0.1)  #printerScale ?
        
        
        #x1 = (pos1[0]+0.5) * self.squareWidth()
        #y1 = (pos1[1]+0.5) * self.squareHeight()
        
        #x2 = (pos2[0]+0.5) * self.squareWidth()
        #y2 = (pos2[1]+0.5) * self.squareHeight()
        
        #dc.DrawLine(x1, y1,  # FROM
        #            x2, y2)                            # TO

    def drawPheromone(self, dc, x, y, val):
        size = self.GetClientSize()
        boardTop = size.GetHeight() - Board.BoardHeight * self.squareHeight()
        dc.SetMapMode(wx.MM_TEXT)
        f = wx.Font(4, wx.FONTFAMILY_MODERN, wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_NORMAL)
        dc.SetFont(f)
        val_str = "%.2f" % round(val,2)
        dc.DrawText(val_str, 0 + (x+0.75) * self.squareWidth(),
                boardTop + (y+0.25) * self.squareHeight())
    
    def drawAgent(self, dc, x, y):
        pen = wx.Pen("#000000")
        pen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(pen)
        dc.SetBrush(wx.Brush("#000000"))
        # Fill at most 1/2 of square
        radius = min( self.squareWidth(), self.squareHeight() )*0.5
        dc.DrawCircle(int(x), int(y), int(radius))

    def drawSquare(self, dc, x, y, shape):
        colors = ['#000000', '#CC6666', '#66CC66', '#6666CC',
                  '#CCCC66', '#CC66CC', '#66CCCC', '#DAAA00']
        
        #colors = ['#000000', '#DAAA00', '#66CCCC', '#CCCC66']
        
        light = ['#000000', '#F89FAB', '#79FC79', '#7979FC', 
                 '#FCFC79', '#FC79FC', '#79FCFC', '#FCC600']
        
        #light = ['#000000', '#FCC600', '#79FCFC', '#FCFC79']

        dark = ['#000000', '#803C3B', '#3B803B', '#3B3B80', 
                 '#80803B', '#803B80', '#3B8080', '#806200']

        #dark = ['#000000', '#806200', '#3B8080', '#80803B']

        pen = wx.Pen(light[shape])
        pen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(pen)

        dc.DrawLine(x, y + int(self.squareHeight()) - 1, x, y)
        dc.DrawLine(x, y, x + int(self.squareWidth()) - 1, y)

        darkpen = wx.Pen(dark[shape])
        darkpen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(darkpen)

        dc.DrawLine(x + 1, y + int(self.squareHeight()) - 1,
            x + int(self.squareWidth()) - 1, y + int(self.squareHeight()) - 1)
        dc.DrawLine(x + int(self.squareWidth()) - 1, 
        y + int(self.squareHeight()) - 1, x + int(self.squareWidth()) - 1, y + 1)

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(colors[shape]))
        dc.DrawRectangle(x + 1, y + 1, self.squareWidth() - 2, 
        self.squareHeight() - 2)


class Agent(object):
    def __init__(self):
        self.pos = (0,0)
        self.start = (0,0)
        self.path = []  # Stores A* path after computation,
                        # or ACO steps as it progresses
        self.returning = False
        self.goal = (MAP_SIZE-1, MAP_SIZE-1)
        self.pathTries = 0
        # Stats
        self.trips = 0
        self.nodesExpanded = 0
        
        # For storing the solution on the way back
        self.pathBack = []
        self.needsPath = True
        
        # For A* to store steps taken along paths so far (so we can
        # draw the entire path)
        self.stepsTaken = []

    def status(self):
        return self.returning

    #def x(self, index):
    #    return self.coords[0]

    #def y(self, index):
    #    return self.coords[1]

    #def setX(self, x):
    #    self.coords[0] = x

    #def setY(self, y):
    #    self.coords[1] = y
        
    def update(self, gameMap):
        self.move(gameMap)
        
    # AI
    def getSuccessors(self, pos):
        return [ (pos[0]+1, pos[1]), (pos[0], pos[1]+1), (pos[0]-1, pos[1]), (pos[0], pos[1]-1) ]
    
    def manhattanDistance(self, position, other=(-1,-1)):
        if other == (-1,-1):
            if self.returning:
                goalPosition = self.start
            else:
                goalPosition = self.goal
        else:
            goalPosition = other
        return abs(goalPosition[0] - position[0]) + abs(goalPosition[1] - position[1])
    
    def antHeuristic(self, successor, current, previous, map):
        '''
        Returns ant heuristic. Inverse of normal (we want higher weights being closer).
        We get the inverse by subtracting from the maximum heuristic.
        
        This applies the following weights (ant is facing > )
          5
        1 > 10
          5
          
        So we almost never go backwards (unless we have to), and we highly favor
        going in a straight line.
        '''
        # If we haven't moved
        if previous is None:
            #print "FAIL"
            return 5
        #print previous,
        #print " ",
        #print current,
        #print " ",
        #print successor
        # get the direction that the last move went
        if (previous[0]==current[0]-1 and successor[0]==current[0]+1):
            #print "FORWARD"
            return ANT_FORWARD_WEIGHT
        if (previous[1]==current[1]-1 and successor[1]==current[1]+1):
            #print "FORWARD"
            return ANT_FORWARD_WEIGHT
        if (previous[0]==current[0]+1 and successor[0]==current[0]-1):
            #print "FORWARD"
            return ANT_FORWARD_WEIGHT
        if (previous[1]==current[1]+1 and successor[1]==current[1]-1):
            #print "FORWARD"
            return ANT_FORWARD_WEIGHT
        if successor == previous:
            return ANT_BACKWARD_WEIGHT
        else:
            return ANT_SIDEWAYS_WEIGHT
        
    def getASTARPath(self, gameMap):
        '''
        Performs A* pathfinding.
        '''
        if self.returning:
            goal = self.start
        else:
            goal = self.goal
            
        # For Incremental A*
        depth = 0
        
        # Do the actual A* using knownMap
        start = self.pos
        closedSet = []
        openSet = [start]
        came_from = {}
        g_score = {}
        h_score = {}
        f_score = {}
        g_score[start] = 0
        h_score[start] = self.manhattanDistance(start, goal)
        f_score[start] = h_score[start]
        
        def getSuccessors(pos):
            # expand successors
            successors = [ (pos[0]+1, pos[1]), 
                           (pos[0], pos[1]+1), 
                           (pos[0]-1, pos[1]), 
                           (pos[0], pos[1]-1) ]
            # Filter out successors that are out of bounds
            successors = filter( lambda x: x[0]>=0 and x[1]>=0, successors )
            #print len(gameMap.getKnownMap())
            successors = filter( lambda x: x[0]<len(gameMap.getKnownMap()) and x[1]<len(gameMap.getKnownMap()), successors )
            # Filter out bad successors
            #print successors
            successors = filter(lambda x: gameMap.knownValidMove(x), successors)
            
            # We've expanded a node. Keep count.
            self.nodesExpanded += 1
            #print successors
            return successors
        
        def getFScore(pos):
            return f_score[pos]
            
        def reconstruct_path(came_from, current_node, start_node):
            p = [current_node]
            while current_node != start_node:
                p.append( came_from[current_node] )
                current_node = came_from[current_node]
            return p
        
        while len(openSet) > 0:
            #print "START"
            openSet.sort(key=getFScore)
            openSet.reverse() # sort openlist by f_score
            x = openSet.pop()
            if x == goal:
                return reconstruct_path(came_from, goal, start)
            # If we've hit our depth slice, we build the
            # path to where we currently are.
            if ASTAR_TIMESLICE and depth >= ASTAR_TIMESLICE:
                slice_path = reconstruct_path(came_from, x, self.pos)
                slice_path.pop()
                #slice_path.pop()
                print slice_path
                return slice_path
            
            depth += 1
            
            closedSet.append(x)
            for y in getSuccessors(x):
                #print "HAS SUCCESSORS"
                if y in closedSet:
                    #print "CLOSED"
                    continue
                tentative_g_score = g_score[x] + self.manhattanDistance(x,y)
                
                if y not in openSet:
                    #print "ADD TO OPENSET"
                    openSet.append(y)
                    tentative_is_better = True
                elif tentative_g_score < g_score[y]:
                    tentative_is_better = True
                else:
                    tentative_is_better = False
                
                if tentative_is_better == True:
                    came_from[y] = x
                    g_score[y] = tentative_g_score
                    h_score[y] = self.manhattanDistance(y, goal)
                    f_score[y] = g_score[y] + h_score[y]
        return -1
    
    
    def findASTARPath(self, gameMap):
        # store path in self.path
        ret = self.getASTARPath(gameMap)
        if ret == -1:
            # failure
            print "FAIL"
            return -1
        else:
            print "PATH RETURNED: ",
            print ret
            gameMap.globalSolution = ret
            self.path = ret
        self.needsPath = False
        return 0
        
    def move(self, gameMap):
        '''
        Moves the agent on the map.
        Can fail if obstacle is in the way.
        '''
        if ALGORITHM_ASTAR:
            # Check if path has been invalidated
            # For timesliced, just look at next step---forces
            # exploration
            #invalid = False
            #if ASTAR_TIMESLICE and len(self.path):
            #    print "TIMESLICE CHECK"
            #    if not gameMap.knownValidMove(self.path[-1]):
            #        print "PATH BAD"
            #        invalid = True
                
            # For normal, check entire thing/
            invalid = False
            if not ASTAR_TIMESLICE and len(self.path):
                print "NONTIMESLICE CHECK"
                for step in self.path:
                    if not gameMap.knownValidMove(step):
                        invalid = True
                        break
            if invalid:
                self.path = [] # invalidate the path
            
            newPos = self.moveASTAR(gameMap)
            
        elif ALGORITHM_ANT:
            oldPos = self.pos
            newPos = self.moveAnt(gameMap)
            if oldPos != newPos and self.returning:
                gameMap.addPheromone(oldPos)
        
        else:
            print "ERROR: Need to select an algorithm."
            sys.exit(-1)
        
        gameMap.updateKnownMap(newPos)
        self.pos = newPos
        
        if self.pos == self.goal and not self.returning:
            self.returning = True
            
            
            if ALGORITHM_ASTAR:
                self.stepsTaken = [] # Clear the prior steps
            
            if ALGORITHM_ANT:
                # Setup the storage for the path on the way back.
                self.pathBack = []
                # Straighten the path
                self.path = self.eliminateLoops(self.path)
                # Set the global solution
                gameMap.updateGlobalSolution(list(reversed(self.path)))
            
        if self.returning and self.pos == self.start:
            # Successfully made a round-trip
            self.trips += 1
            self.returning = False
            
            if ALGORITHM_ASTAR:
                self.stepsTaken = [] # clear the prior steps
            
            # If an ant returns, we should update the global solution
            #if ALGORITHM_ANT:
            #    gameMap.updateGlobalSolution(self.pathBack)
            
        
    def moveAnt(self, gameMap):
        '''
        Moves the agent based on Ant Algorithm.
        '''
        
        # If we're returning, follow the path that's been built as we went
        # When we reach the start, self.pathBack will contain the path
        if self.returning:
            if len(self.path)>0:
                #print "RETURNING"
                step = self.path.pop() # pop off a step at a time
            
                if not gameMap.validMove(step):
                    self.path = []
                    return self.pos
                else:
                    self.pathBack.append(step)
                    if step == self.goal: # We need to pop once more
                        step = self.path.pop()
                        self.pathBack.append(step)
                return step
            #else:
                # Our path back is lo longer valid.
                
                    
        
        # expand successors
        successors = self.getSuccessors(self.pos)
        previousStep = None
        if len(self.path) > 1:
            previousStep = self.path[-2]
            #print "PREVIOUS: ",
            #print previousStep
            #print self.path
        elif self.returning:
            self.path.append(self.goal)
        else:
            self.path.append(self.start)
        
        # Filter out successors that are out of bounds
        successors = filter( lambda x: x[0]>=0 and x[1]>=0, successors )
        successors = filter( lambda x: x[0]<len(gameMap.getKnownMap()) and x[1]<len(gameMap.getKnownMap()), successors )
        
        # Filter out bad successors
        successors = filter(gameMap.validMove, successors)
        if len(successors) == 0:
            return self.pos
        
        # calculate weight of successors
        # combines direction (favor forward) and pheromone
        probs = []
        for successor in successors:
            # TODO: Make this work
            #print "TESTING SUCCESSOR DIRECTION"
            #print "n ",
            #print successor,
            #print " c ",
            #print self.pos,
            #print " p ",
            #print previousStep
            if self.returning: # Ignore pheromones if our path back broke
                p = self.antHeuristic(successor, self.pos, previousStep, gameMap)*BETA
            else:
                p = gameMap.getPheromone(successor)*ALPHA + self.antHeuristic(successor, self.pos, previousStep, gameMap)*BETA
            probs.append( p )
        # probabilities are then each out of the total
        #print probs
        total = sum(probs)
        if total != 0:
            probs = [ prob / total for prob in probs ]
        else:
            probs = [ 0 for prob in probs ]
        
        # do probabilistic random walk
        totals = []
        running_total = 0
        for w in probs:
            running_total += w
            totals.append(running_total)
        rnd = random.random() * running_total
        newPos = self.pos
        for i, total in enumerate(totals):
            if rnd < total:
                newPos = successors[i]
                break
        
        #print newPos
        self.path.append(newPos)
        return newPos
        
    def moveASTAR(self, gameMap):
        '''
        Moves the agent based on their A* path.
        If no path exists (due to obstacle breaking it).
        Agents will trash for a while if they can't get a path.
        '''
        # DEPRECATED SETTING
        MAX_TRIES = 1
        
        if self.path != None and len(self.path) > 0 and gameMap.validMove(self.path[-1]):
            print "POPPING MOVE"
            self.pathTries = 0
            newPos = self.path.pop()
            self.stepsTaken.append(newPos)
            return newPos
            
        # If we've hit our timeslice, clear so we re-find
        #if ASTAR_TIMESLICE and len(self.stepsTaken) >= ASTAR_TIMESLICE:
        #    self.path = []
        #    self.globalSolution = []
        
        if len(self.path) > 0 and not gameMap.validMove(self.path[-1]):
            # If the path is bad, we need to reset the global solution
            print "BAD NEXT STEP"
            gameMap.globalSolution = []
            self.path = []
        
        if len(gameMap.globalSolution) > 0 and ASTAR_REUSE_PATH:
            if self.returning:
                self.path = list(reversed(gameMap.globalSolution))
                print "RETURNING: ",
                print self.path
            else:
                self.path = gameMap.globalSolution
                print "GOING: ",
                print self.path
            return self.moveASTAR(gameMap) # recurse
            #newPos = self.path.pop()
            #self.stepsTaken.append(newPos)
            #return newPos
            
        if self.pathTries < MAX_TRIES:
            print "TRYING TO FIND"
            self.pathTries += 1
            ret = self.findASTARPath(gameMap)
            if ret == -1:
                print "FAIL"
                self.pathTries = 0
                gameMap.resetKnownMap()  # If we fail to find, 
                                         # we should assume the map changed
                return self.pos
            return self.moveASTAR(gameMap)
            
        else:
            self.pathTries = 0
            return self.pos
    
    
    #def moveDLITE(self, gameMap):
        
        #if not len(s_last):
            #initialize_dstar()
            #compute_shortest_path_dlite()
        
        #s_start = min([c(s_start+s_prime)+g(s_prime) for s_prime in successors(s_start)])
        ## move to s_start
        
        
        ## Scan graph for changed edge costs
        ## if any edge costs changed
        #if edge_changed:
            #k_m = k_m + h(s_last, s_start)
            #s_last = s_start
            ## for all directed edge (u,v) with changed edge costs
            #for u,v in changed_edges:
                #c_old = c(u,v)
                ## Update the edge cost c(u,v)
                #if (c_old > c(u,v)):
                    
        
        
        
    #def 
    
    def eliminateLoops(self, path):
        '''
        Goes through path and eliminates loops.
        Each ant tracks its steps. In AntSim, it eliminates loops.
        To do that, we "straighten" the path by:
        For each step, if we return to that step later in the path, cut that length out
        
        Roughly O(length^2)
        '''
        #workingPath = []
        #print "eliminateLoops"
        loops = True
        while loops:
            loop_this_round = False
            for i, step1 in enumerate(path):
                for j, step2 in enumerate(path[i+1:]):
                    if step1 == step2:  # We've found a loop
                        path = path[0:i] + path[i+j+1:]
                        loop_this_round = True
                        break
                # If we've changed the path, we want to start again
                if loop_this_round:
                    break
            if loop_this_round == False:
                loops = False
        # We should now have a path with no loops
        return path

def manhattanDistance(position, other):
    
    #if other == (-1,-1):
        #if self.returning:
            #goalPosition = self.start
        #else:
            #goalPosition = self.goal
    #else:
        #goalPosition = other
    return abs(other[0] - position[0]) + abs(other[1] - position[1])

def getTrueASTARPath(trueMap):
    '''
    Performs A* pathfinding.
    '''
    start=(0,0)
    goal=(MAP_SIZE-1, MAP_SIZE-1)
    
    # Do the actual A* using the true map
    closedSet = []
    openSet = [start]
    came_from = {}
    g_score = {}
    h_score = {}
    f_score = {}
    g_score[start] = 0
    h_score[start] = manhattanDistance(start, goal)
    f_score[start] = h_score[start]
    
    def validMove(pos):
        if trueMap[pos[0]][pos[1]] == Map.FILLED:
            return False
        else:
            return True
    
    def getSuccessors(pos):
        # expand successors
        successors = [ (pos[0]+1, pos[1]), 
                       (pos[0], pos[1]+1), 
                       (pos[0]-1, pos[1]), 
                       (pos[0], pos[1]-1) ]
        # Filter out successors that are out of bounds
        successors = filter( lambda x: x[0]>=0 and x[1]>=0, successors )
        #print len(gameMap.getKnownMap())
        successors = filter( lambda x: x[0]<len(trueMap) and x[1]<len(trueMap), successors )
        # Filter out bad successors
        #print successors
        successors = filter(validMove, successors)
        
        # We've expanded a node. Keep count.
        #agent.nodesExpanded += 1
        #print successors
        return successors
    
    def getFScore(pos):
        return f_score[pos]
        
    def reconstruct_path(came_from, current_node, start_node):
        p = [current_node]
        while current_node != start_node:
            p.append( came_from[current_node] )
            current_node = came_from[current_node]
        return p
    
    while len(openSet) > 0:
        #print "START"
        openSet.sort(key=getFScore)
        openSet.reverse() # sort openlist by f_score
        x = openSet.pop()
        if x == goal:
            return reconstruct_path(came_from, goal, start)
        
        closedSet.append(x)
        for y in getSuccessors(x):
            #print "HAS SUCCESSORS"
            if y in closedSet:
                #print "CLOSED"
                continue
            tentative_g_score = g_score[x] + manhattanDistance(x,y)
            
            if y not in openSet:
                #print "ADD TO OPENSET"
                openSet.append(y)
                tentative_is_better = True
            elif tentative_g_score < g_score[y]:
                tentative_is_better = True
            else:
                tentative_is_better = False
            
            if tentative_is_better == True:
                came_from[y] = x
                g_score[y] = tentative_g_score
                h_score[y] = manhattanDistance(y, goal)
                f_score[y] = g_score[y] + h_score[y]
    return -1
    
class Map(object):
    '''
    Map is a time-variant random K by K grid.
    
    Each call to Map.update() switches to the next layout.
    
    The following is the meaning of each cell
    
    NOTE: We always access Map[x][y]
    This isn't actually representative of how Python handles arrays,
    but think of it as column, then cell. Less likely to make mistakes
    this way.
    
    '''
    
    EMPTY = 0
    FILLED = 1
    EMPTY_NOW_FILLED = 2  # When the knownMap has it empty,
                          # but the real map is filled
    FILLED_NOW_EMPTY = 3  # When the knownMap has it filled,
                          # but the real map is empty
    
    # So drawing the map uses those constants, along with agent pos,
    # pheromone levels, and current paths
    
    def __init__(self, size=MAP_SIZE):
        self.size = size
        self.currentState = 0
        self.map = [[0 for y in range(size)] for x in range(size)]
        self.globalSolution = []
        self.update()  # Sets the self.map
        # should be LENxLEN of 0s
        self.pheromones = [[0 for y in range(size)] for x in range(size)] 
        self.knownMap = [[Map.EMPTY for y in range(size)] for x in range(size)]
        
    def update(self):
        '''
        Updates the map to a new random state
        '''
        self.map = self.randomMap()
        self.updateGlobalSolution([]) # Clear the global solution
    
    def updateGlobalSolution(self, path):
        if len(self.globalSolution) == 0 or len(path) < len(self.globalSolution):
            self.globalSolution = path
    
    def getMap(self):
        return self.map
        
    def getKnownMap(self):
        '''
        Return map as it was last known.
        '''
        return self.knownMap
    
    def updateKnownMap(self, agentPos):
        '''
        Update known map.
        Does this in a square around the agent
        '''
        # Radius around agentPos gets synced with real map
        # NOTE: range is array index safe (lower to upper-1) already
        for x in range(max(agentPos[0]-AGENT_VIEW_RADIUS, 0), min(agentPos[0]+AGENT_VIEW_RADIUS, self.size)):
            for y in range(max(agentPos[1]-AGENT_VIEW_RADIUS, 0), min(agentPos[1]+AGENT_VIEW_RADIUS, self.size)):
                self.knownMap[x][y] = self.getMap()[x][y]
    
    def resetKnownMap(self):
        self.knownMap = [[Map.EMPTY for y in range(MAP_SIZE)] for x in range(MAP_SIZE)]
    
    def attenuateSpace(self, space):
        '''
        Very simple multiplicative evaporation.
        '''
        return space * EVAPORATION_FACTOR
    
    def attenuatePheromones(self):
        '''
        Evaporates (attenuates) pheromone levels.
        '''
        for x, col in enumerate(self.pheromones):
            for y, cell in enumerate(col):
                self.pheromones[x][y] = self.attenuateSpace(cell)
        if ANT_ELITIST:
            for x,y in self.globalSolution:
                self.addPheromone((x,y))
    
    def getPheromone(self, position):
        return self.pheromones[position[0]][position[1]]
        
    def addPheromone(self, position):
        self.pheromones[position[0]][position[1]] += PHEROMONE_DROP_AMOUNT
    
    def validMove(self, position):
        if self.map[position[0]][position[1]] == Map.FILLED:
            return False
        else:
            return True
    
    def knownValidMove(self, position):
        if self.knownMap[position[0]][position[1]] == Map.FILLED:
            return False
        else:
            return True
    
    def randomMap(self):
        '''
        This fills in a new map randomly (semi-randomly---there's some 
        structure to the fill).
        
        Until there exists a path on the full map using A*, we repeat:
            1) For each space (not start/goal), X% chance of filling.
            2) For each space, if it is next to a filled space, Y%
                chance of filling.
        
        That gives us a slightly clustered map (feels a little more
        realistic---could also group by 80/20, etc.) that still has at
        least one valid path through it (don't want to trap agents at
        start or goal---trapping elsewhere is okay).
        
        Uses basically the same A* as the agents to test (except it
        operates on just the map, not the Map object)
        '''
        
        validMap = False
        
        while not validMap:
            
            # Make an empty SIZE x SIZE map
            newMap = [ [ 0 for y in range(0,self.size) ] for x in range(0,self.size) ]
            
            for x, col in enumerate(newMap):
                for y, cell in enumerate(col):
                    # If start or goal, don't fill!
                    if (x,y) == (0,0) or (x,y) == (MAP_SIZE-1,MAP_SIZE-1):
                        continue
                    if (randint(0,100) < FIRST_CHANCE):
                        newMap[x][y] = Map.FILLED
            
            for x, col in enumerate(newMap):
                for y, cell in enumerate(col):
                    # If start or goal, don't fill!
                    if (x,y) == (0,0) or (x,y) == (MAP_SIZE-1,MAP_SIZE-1):
                        continue
                    # If already filled, skip out.
                    if newMap[x][y] == Map.FILLED:
                        break
                    # Check if any neighboring cells are filled
                    neighborFilled = False
                    for x2 in range(max(x-1, 0), min(x+1, self.size-1)):
                        for y2 in range(max(y-1,  0), min(y+1, self.size-1)):
                            if newMap[x2][y2] == Map.FILLED:
                                neighborFilled = True
                                break
                        if neighborFilled:
                            break
                    # If a neighbor was filled, we use the Second Chance %
                    i = randint(0,100)
                    if neighborFilled and i < SECOND_CHANCE:
                        newMap[x][y] = Map.FILLED
                    elif i < FIRST_CHANCE:
                        newMap[x][y] = Map.FILLED
            # Test the map!
            ret = getTrueASTARPath(newMap)
            if ret != -1:
                validMap = True
        return newMap
    
def main():
    # Parse any commandline args
    # Be able to set any settings via commandline?
    
    app = wx.App()
    Sim(None, -1, 'Imperfect Path')
    app.MainLoop()

if __name__ == "__main__":
    main()
