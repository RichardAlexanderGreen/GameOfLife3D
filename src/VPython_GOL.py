#!/usr/bin/python

# working toward visualizing Game of Life in Visual Python

from visual import *
from visual.controls import *

from Grid3D import Grid3D

#import sys


grey80 = ( 0.8, 0.8, 0.8 )

class GameOfLifeUserInterface( object ):

    def __init__( self, nRows = 5, nColumns = 5, nLayers = 5 ):

        self.grid = Grid3D( rows = nRows, columns = nColumns, layers = nLayers )
        self.cells = dict()
        
        # Initialize scene parameters
        self.initializeSceneParameters()
        # Draw the grid. Put spots at intersections.
        self.drawGrid( self.grid )

    def initializeSceneParameters( self ):
        scene.title = "Game of Life in 3D"
        ##scene.stereo = 'redcyan'
        scene.height = 600
        scene.width = 600
        #scene.range = ( 1, 1, 1 )
        #scene.center = ( 0, 2, 20 )
        
        scene.autocenter = True
        scene.userspin = True
        scene.userzoom = True

    def drawGrid( self, grid ):
        '''
        Draw the grid. Put spots at centers.
        '''
        #print( '*** Draw the Grid *** ') 
        spotSize = 0.05
        for layerIndex in range( 1, grid.layers + 1):
            for rowIndex in range( 1, grid.rows + 1):
                for columnIndex in range( 1, grid.columns + 1):
                    spot = box( width = spotSize, length = spotSize, height = spotSize,
                                       pos = (  rowIndex, columnIndex, layerIndex ),
                                       color = color.white
                                       )
    """
    def expose_cb( self, window, event ):
        self.draw_grid()


    def loop( self ):
        # gobject.timeout_add( 1000, self.next_grid )
        # gtk.main()
        self.drawLiveCells()
    """
    def next_grid( self ):
        self.grid = self.grid.nextGeneration()
        self.drawLiveCells( )
        return True

    def drawLiveCells( self ):
        '''
        Draw the live cells in the grid.
        '''
        #print( '*** Draw the Live Cells ***' )
        for layerIndex in range( 1, self.grid.layers + 1):
            for rowIndex in range( 1, self.grid.rows + 1):
                for columnIndex in range( 1, self.grid.columns + 1):
                    cellValue = self.grid.getCell( layer = layerIndex, row = rowIndex, column = columnIndex )
                    self.drawCell( layer = layerIndex, row = rowIndex, column = columnIndex, value = cellValue )
                    
    def drawCell( self, layer, row, column, value ):
        cellValue = value
        position = ( row, column, layer )
 
        if cellValue == None:
            pass
        
        elif cellValue == 0:
            oldCell = self.cells.get( position )
            oldCell.color = color.red
            oldCell.opacity = 0.4
            oldCell.radius = 0.2
            
        elif cellValue > 0:
            oldCell = self.cells.get( position )
            greenLevel = min( 1.0, 0.4 + (cellValue * 0.2) )
            if oldCell != None:
                oldCell.color = ( 0.0, greenLevel, 0.0 )
                oldCell.opacity = greenLevel
                oldCell.radius = 0.4
            else:
                showLiveCell = sphere( color = ( 0.0, greenLevel, 0.0  )
                                              , opacity = greenLevel
                                              , radius = 0.4
                                              , pos = position
                                              )
                self.cells[ position ] = showLiveCell
        else:
            print( '???',  layer, row, column , cellValue )

def runFlasher():
    print( '*** Starting with Flasher pattern ***' )

    gameSize = 11
    middle = 1 + gameSize // 2
    game = GameOfLifeUserInterface( nRows = gameSize, nColumns = gameSize, nLayers = gameSize )
    game.grid.setCell( row = middle, column = middle, layer = middle-1, value = 1 )
    game.grid.setCell( row = middle, column = middle, layer = middle, value = 1 )
    game.grid.setCell( row = middle, column = middle, layer = middle+1, value = 1 )

    # Show set up.
    game.drawLiveCells()

    # Iterate each time a key is pressed.
    print( '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' )
    print( 'Press any key to get next generation.' )
    print( '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' )

    while scene.kb.getkey():
        game.next_grid()
    


if __name__ == "__main__":
    """
    if len( sys.argv ) != 2:
        print "VPython_GOL.py [file-name]"
        exit( 0 )
    """
    print "***pass***"
    
    pass

runFlasher()
