'''
Created on Apr 5, 2012

@author: MichiPUG
'''


class Grid3D( object ):
    '''
    The Grid is the game space.
	It has rows and columns.
    '''

    def __init__( self,  rows = 9, columns = 9, layers = 1  ):
        '''
        Constructor
        '''
        self.rows = rows
        self.columns = columns
        self.layers = layers
        self.grid = {}

    def setCell(self, row = 1, column =1, layer = 1, value = 1 ):
        xRow = 1 + ( row % self.rows )
        xColumn = 1 + ( column % self.columns )
        xLayer = 1 + ( layer % self.layers )
        self.grid[ (xRow,xColumn,xLayer ) ] = value
        
    def getCell(self, row = 1, column =1, layer = 1 ):
        xRow = 1 + ( row % self.rows )
        xColumn = 1 + ( column % self.columns )
        xLayer = 1 + ( layer % self.layers )
        if self.grid.has_key( (xRow,xColumn,xLayer) ):
            value = self.grid[ (xRow,xColumn,xLayer ) ]
            return value
        else:
            return None
        
    def __eq__(self, otherGrid ):
        return True
        for row in range( self.rows ):
            for column in range( self.columns ):
                for layer in range( self.layers ):
                    if self.getCell( row, column, layer ) != otherGrid.getCell( row, column, layer ):
                        return False
                    
        return True
    
    
    def countLiveNeighbors(self, row, column, layer = 1 ):
        '''
        Eventually, we may want different versions.
        - Count only nearest neighbors (ignore diagnals).
        - Don't wrap over the edges.
        '''
        count = 0
        for r in ( row - 1, row, row + 1 ):
            for c in ( column - 1, column, column + 1 ):
                for lay in ( layer - 1, layer, layer + 1):
                    value = self.getCell( r, c, lay )
                    if r == row and c == column and lay == layer:
                        pass
                    elif value == None :
                        pass
                    elif value == 0 :
                        pass
                    else:
                        count += 1
        return count
                    
 
    def nextGeneration( self ):
        ''' 
        Create the next generation of the grid 
        by applying the rule to the cells in the current generation.
        '''
        nextGrid = Grid3D(  rows = self.rows, columns = self.columns, layers = self.layers  )
        for rowIndex in range( self.rows ):
            for columnIndex in range( self.columns ):
                for layerIndex in range(  self.layers ):
                    value = self.rule( rowIndex, columnIndex, layerIndex )
                    nextGrid.setCell( rowIndex, columnIndex, layerIndex, value )
                
        return nextGrid
   
    def nextGenerationViaSelectedRules( self, selectedRule, selectedNeighborCounter ):
        ''' 
        Enable multiple rules.
        Create the next generation of the grid 
        by applying the selected rule to the cells in the current generation.
        '''
        nextGrid = Grid3D(  rows = self.rows, columns = self.columns, layers = self.layers  )
        for rowIndex in range( self.rows ):
            for columnIndex in range( self.columns ):
                for layerIndex in range(  self.layers ):
                    value = selectedRule( rowIndex, columnIndex, layerIndex, selectedNeighborCounter )
                    nextGrid.setCell( rowIndex, columnIndex, layerIndex, value )
                
        return nextGrid
   
   
    def nextGenerationViaSelectedRuleSet( self, selectedRule, selectedNeighborCounter, seedRule, killRule ):
        ''' 
        Enable multiple rules.
        Create the next generation of the grid 
        by applying the selected rule to the cells in the current generation.
        '''
        nextGrid = Grid3D(  rows = self.rows, columns = self.columns, layers = self.layers  )
        for rowIndex in range( self.rows ):
            for columnIndex in range( self.columns ):
                for layerIndex in range(  self.layers ):
                    value = selectedRule( rowIndex, columnIndex, layerIndex, selectedNeighborCounter, seedRule, killRule )
                    nextGrid.setCell( rowIndex, columnIndex, layerIndex, value )
                
        return nextGrid
   
    def rule( self, row, column, layer  ):
        '''
        Modified Game of Life rule 
        -- We are distinguishing dead from empty to enable strength or age values
        This version of the rule distinguishes dead from empty; but is otherwise the same as the 2D rule.
        '''
        nLiveNeighbors = self.countLiveNeighbors( row, column, layer )

        value = self.getCell( row, column, layer )
        
        if value == None and nLiveNeighbors == 3 :
            return 1
        elif value == None:
            return None
        elif value > 0:
            if nLiveNeighbors == 2 or nLiveNeighbors == 3:
                return value + 1           # Live longer and prosper
            else:
                return 0                       # Too few or too many neighbors
        else:  # I am dead
            if nLiveNeighbors == 3:
                return 1                       # Curiously, exactly three neighbors make a seed
            else:
                return 0
    
   
    def rule2( self, row, column, layer, selectedNeighborCounter  ):
        '''
        This version parameterizes countLiveNeighbors() function.
        '''
        nLiveNeighbors = selectedNeighborCounter( row, column, layer )

        value = self.getCell( row, column, layer )
        
        if value == None and nLiveNeighbors == 3 :
            return 1
        elif value == None:
            return None
        elif value > 0:
            if nLiveNeighbors == 2 or nLiveNeighbors == 3:
                return value + 1           # Live longer and prosper
            else:
                return 0                       # Too few or too many neighbors
        else:  # I am dead
            if nLiveNeighbors == 3:
                return 1                       # Curiously, exactly three neighbors make a seed
            else:
                return 0
    
   
    def rule3( self, row, column, layer, selectedNeighborCounter, seedRule, killRule  ):
        '''
        This version parameterizes countLiveNeighbors() function.
        '''
        nLiveNeighbors = selectedNeighborCounter( row, column, layer )

        cellValue = self.getCell( row, column, layer )
        
        #  Note: Seed rule over-rides kill rule.         
        if seedRule( cellValue, nLiveNeighbors ):
            
            if cellValue == None:
                return 1                             # Seed
            else:
                return  cellValue + 1          # Live longer and prosper       
        
        
        elif killRule( cellValue, nLiveNeighbors ):
            if cellValue == None:
                return None                       # Stay empty
            else:
                return 0                             # Die
            
        else: 
            if cellValue == None:
                return None
            else: 
                return cellValue + 1          # Live longer and prosper 
       
    
    def printGrid( self, gridMessage = '' ):
        ''' 
        Print utility for debug
        '''
        for layerIndex in range(  1, self.layers + 1 ):
            for rowIndex in range( 1, self.rows + 1  ):                        # Use 1 .. rows rather than than 0 .. rows-1
                for columnIndex in range( 1, self.columns + 1 ):
                    cellValue = self.getCell( row = rowIndex, column = columnIndex, layer = layerIndex )
                    self.printCell( row = rowIndex, column = columnIndex, layer = layerIndex, value = cellValue, message = gridMessage )
                    
    def printCell(self,  row, column, layer, value, message = '' ):
        print( message+ ': Layer, Row, Column =' , layer, row, column, '==>', value )
        
    def printLiveCells(self, liveMessage = 'Live cells' ):
        ''' 
        Another Print utility for debug
        '''
        for layerIndex in range(  1, self.layers + 1 ):
            for rowIndex in range( 1, self.rows + 1  ):                        # Use 1 .. rows rather than than 0 .. rows-1
                for columnIndex in range( 1, self.columns + 1 ):
                    cellValue = self.getCell( row = rowIndex, column = columnIndex, layer = layerIndex )
                    if cellValue == None:
                        pass
                    elif cellValue == 0:
                        pass
                    else:
                        self.printCell( row = rowIndex, column = columnIndex, layer = layerIndex, value = cellValue, message = liveMessage )
        
                
    def isAllDead( self ):
        ''' 
        Test for no living cells. (Game Over)
        '''
        nEmpty = 0
        for layerIndex in range(  1, self.layers + 1 ):
            for rowIndex in range( 1, self.rows + 1  ):                        # Use 1 .. rows rather than than 0 .. rows-1
                for columnIndex in range( 1, self.columns + 1 ):
                    cellValue = self.getCell( row = rowIndex, column = columnIndex, layer = layerIndex )
                    if cellValue == None:
                        nEmpty += 1
                    elif cellValue > 0:
                        #self.printCell( message = 'Alive at', row = rowIndex, column = columnIndex, layer = layerIndex, value = cellValue )
                        return False
                    
        print( '. nEmpty = ', nEmpty )
        return True
    
    def seedAtRandom(self, percentage ):
        '''
        Generate a new grid with seed (value = 1) at random locations
        '''
        import random
        random.seed() 
        
        nextGrid = Grid3D(  rows = self.rows, columns = self.columns, layers = self.layers  )
        for rowIndex in range( 1, self.rows + 1  ):                        # Use 1 .. rows rather than than 0 .. rows-1
            for columnIndex in range( 1, self.columns + 1 ):
                for layerIndex in range(  1, self.layers + 1 ):
                    rand = random.randint(0,100)
                    if rand >= percentage:
                        nextGrid.setCell( row = rowIndex, column = columnIndex, layer = layerIndex, value = 1 )
                        #print('. Setting: ', rowIndex, columnIndex, layerIndex )
        
        return nextGrid
        
        
                

 
"""   
    def grid3DfromFile( self, file_name ):
        textFile = open( file_name )
        rows = [ line.rstrip( '\r\n' ) for line in textFile ]
        textFile.close( )
        
        width  = max( len( row ) for row in rows )
        grid = Grid3D( len( rows ), width )
    
        for ( y, row ) in enumerate( rows ):
            for ( x, cell ) in enumerate( row ):
                if cell == '*':
                    grid.rows[y][x] = 1
    
        return grid
"""    
