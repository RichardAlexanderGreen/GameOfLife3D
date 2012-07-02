'''
Created on Apr 5, 2012

@author: MichiPUG
'''

from itertools import repeat

def grid2DfromFile( file_name ):
    input = open( file_name )
    rows = [ line.rstrip( '\r\n' ) for line in input ]
    input.close( )
    
    width  = max( len( row ) for row in rows )
    grid = Grid2D( len( rows ), width )

    for ( y, row ) in enumerate( rows ):
        for ( x, cell ) in enumerate( row ):
            if cell == '*':
                grid.rows[y][x] = 1

    return grid

class Grid2D( object ):
    '''
    The Grid is the game space.
	It has rows and columns.
    '''

    def __init__( self,  height, width  ):
        '''
        Constructor
        '''
        self.width = width
        self.height = height
        self.rows = [ list( repeat( 0,width ) ) for dummy in range( height ) ]
        
    def __str__( self ):
        """
        Show the grid as text
        """
        output = []
        for row in self.rows:
            line = ''.join( '*' if cell else '-' for cell in row  )
            output.append( line  )
            
        return '\n'.join( output  )+'\n'
    
    def __str1__( self ):
        """
        Another way to do it with somewhat more readable code
        """
        output = ''
        for rowIndex in range( self.height ):
            for columnIndex in range( self.width ):
                output += str( self.rows[rowIndex][columnIndex]  )
            output += '\n'
        return output.replace( '0', '-' ).replace( '1','*' )
    
    def nextGeneration( self ):
        """ 
        Create the next generation of the grid 
        by applying the rule to the cells in the current generation.
        """
        nextGrid = Grid2D( height = self.height, width = self.width  )
        for rowIndex in range( self.height ):
            for columnIndex in range( self.width ):
                nextGrid.rows[rowIndex][columnIndex] = self.rule( row = rowIndex, column = columnIndex )
                
        return nextGrid
   
    def rule( self, row, column  ):
        """
        Rule with edge effects -- The space is not a toroid
        """
        nLiveNeighbors = 0
        for r in range( max( 0,row-1 ), min( self.height, row+2 )  ):              # NOT a toroid
            for c in range( max( 0, column-1  ), min( self.width, column+2 )  ):
                nLiveNeighbors += self.rows[r][c]

        nLiveNeighbors -= self.rows[row][column]    # Remove this cell from neighbors    

        amAlive = self.rows[row][column]
        if amAlive:
            if nLiveNeighbors == 2 or nLiveNeighbors == 3:
                return 1
            else:
                return 0
        else:
            if nLiveNeighbors == 3:
                return 1
            else:
                return 0
    
    def __eq__( self, other  ):
        return ( str( self )== str( other ) )
        

    def rule2( self, row, column  ):
       """
       Rule without edge effects -- The space is a toroid
       """
       nLiveNeighbors = 0
       for r in range( row-1, row+2  ):              
           for c in range( column-1, column-2  ):
               nLiveNeighbors += self.rows[ r % self.height ][ c % self.width ]  # Toroid indices wrap around

       nLiveNeighbors -= self.rows[row][column]    # Remove this cell from neighbors    

       amAlive = self.rows[row][column]
       if amAlive:
           if nLiveNeighbors == 2 or nLiveNeighbors == 3:
               return 1
           else:
               return 0
       else:
           if nLiveNeighbors == 3:
               return 1
           else:
               return 0

