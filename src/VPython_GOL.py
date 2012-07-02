#!/usr/bin/python

# working toward visualizing Game of Life in Visual Python
from visual.controls import *

from Grid3D import Grid3D

import sys



class GameOfLifeUserInterface( object ):
    cell_size =  16
    cell_border = 2

    def __init__( self, file_name ):

        #self.grid = Grid3D.grid3DfromFile( file_name )
        self.grid = Grid3D( rows = 8, columns = 8, layers = 8 )
        self.grid.seedAtRandom( percentage = 50 )

        # TODO - INITIALIZE SCENE PARAMTERS
        # TODO - Draw the grid. Put spots at intersections.
        
    def expose_cb( self, window, event ):
        self.draw_grid()


    def loop( self ):
        # gobject.timeout_add( 1000, self.next_grid )
        # gtk.main()
        pass

    def next_grid( self ):
        self.grid = self.grid.nextGeneration()
        self.draw_grid()
        return True

    def draw_grid( self ):
        for x in xrange( self.grid.width ):
            for y in xrange( self.grid.height ):
                self.draw_cell( x, y, self.grid.rows[y][x] )

    def draw_cell( self, x, y, state ):
        if state:
            gc = self.gc_on
        else:
            gc = self.gc_off

        """ REPLACE WITH APPROPRIATE VPython
        self.drawing.window.draw_rectangle( gc, True 
                                                                 , x * ( self.cell_size + self.cell_border ) 
                                                                 , y * ( self.cell_size + self.cell_border )
                                                                 , self.cell_size
                                                                 , self.cell_size 
                                                                 )
        """

""" REMOVED FOR NOW
    def program_exit( self, widget, event ):
        gtk.main_quit()
        return False
"""

if __name__ == "__main__":
    if len( sys.argv ) != 2:
        print "VPython_GOL.py [file-name]"
        exit( 0 )

    game = GameOfLifeUserInterface( sys.argv[1] )
    game.loop()
    
 

