'''
Created on Apr 5, 2012

@author: admin
'''
import unittest

from Grid3D import Grid3D

class Grid3DTest(unittest.TestCase):

    def testCreateGrid(self):
        ''' Story: A grid may be 3 dimensional with rows, columns, and layers. '''
        grid = Grid3D( rows = 17, columns = 19, layers = 1 )
        self.assertEqual( 17, grid.rows )
        self.assertEqual( 19, grid.columns )
        self.assertEqual( 1, grid.layers )
        
    def testSetAndGet(self):
        '''
        The health of a cell is an integer.
        It may be set and inspected.
        '''
        grid = Grid3D( rows = 17, columns = 19, layers = 1 )
        grid.setCell( row = 17, column = 19, layer = 1, value = 3 )
        self.assertEquals( 3, grid.getCell( row = 17, column = 19, layer = 1 ) )
        
    def testGetEmpty(self):
        '''
        An empty cell has never been alive or dead.
        A zero valued cell was alive but has died.
        '''
        grid = Grid3D( rows = 17, columns = 19, layers = 1 )
        grid.setCell( row = 17, column = 19, layer = 1, value = 3 )
        self.assertEquals( 3, grid.getCell( row = 17, column = 19, layer = 1 ) ) 
        # If the cell is empty (as opposed to dead) we get the code value None.
        self.assertEquals( None, grid.getCell( row = 1, column = 1, layer = 1 ) )
        
    def testIndicesWrapAround(self):
        '''
        Our grid is "toroid" -- Indices will wrap around.
        '''
        grid = Grid3D( rows = 17, columns = 19, layers = 1 )
        # Test the indices's upper edges
        grid.setCell( row = 18, column = 20, layer = 2, value = 3 )
        self.assertEquals( 3, grid.getCell( row = 18, column = 20, layer = 2 ) ) 
        self.assertEquals( 3, grid.getCell( row = 1, column = 1, layer = 1 ) )
        # Test the indices's lower edges
        grid.setCell( row = 0, column = 0, layer = 0, value = 5 )
        self.assertEquals( 5, grid.getCell( row = 0, column = 0, layer = 0 ) ) 
        self.assertEquals( 5, grid.getCell( row =17, column =19, layer = 1 ) )

        # If the cell is empty (as opposed to dead) we get the code value None.
        grid = Grid3D( rows = 17, columns = 19, layers = 1 )
        self.assertEquals( None, grid.getCell( row = 0, column = 0, layer = 0 ) )
        self.assertEquals( None, grid.getCell( row = 18, column = 20, layer = 2 ) )
       
    
    def testCountNeighbors(self):
        '''
        The adjacent neighbors include all cells with a row, column, or layer index plus or minus one the cell in question.
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        # One neighbor
        grid.setCell( row = 1, column=1, layer=1, value= 7 )
        count = grid.countLiveNeighbors( row = 2, column = 2, layer = 2 )
        self.assertEquals( 1, count )
        # Two neighbors
        grid.setCell( row = 3, column=3, layer=3, value= 7 )
        count = grid.countLiveNeighbors( row = 2, column = 2, layer = 2 )
        self.assertEquals( 2, count )
        # Three neighbors
        grid.setCell( row = 1, column=3, layer=3, value= 7 )
        count = grid.countLiveNeighbors( row = 2, column = 2, layer = 2 )
        self.assertEquals( 3, count )
        # Four neighbors
        grid.setCell( row = 1, column=2, layer=3, value= 7 )
        count = grid.countLiveNeighbors( row = 2, column = 2, layer = 2 )
        self.assertEquals( 4, count )
        
        #  All Twenty-Six neighbors
        for r in ( 1, 2, 3 ):
            for c in ( 1, 2, 3 ):
                for lay in ( 1, 2, 3 ):
                    grid.setCell( r, c, lay, 11 )        
        count = grid.countLiveNeighbors( row = 2, column = 2, layer = 2 )
        self.assertEquals( 26, count )
    
    def testRule(self):
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        nextGrid = grid.nextGeneration()
        self.assertEquals( grid, nextGrid )
        
    def testDieWithZeroNeighbors(self):
        '''
        Live cell dies when there are no neighbors
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 2, value = 2220 )
        nextGrid = grid.nextGeneration()
        self.assertEquals( 0, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
        
    def testPassWithZeroNeighbors(self):
        '''
        Empty cell stays empty when there are no neighbors
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        nextGrid = grid.nextGeneration()
        self.assertEquals( None, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
                
    def testDieWithOneNeighbor(self):
        '''
        Live cell dies when there is only one neighbor
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 2, value = 2220 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        
        nextGrid = grid.nextGeneration()
        self.assertEquals( 0, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
        
    def testPassWithOneNeighbor(self):
        '''
        Empty cell stays empty when there is only one neighbor
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 22 )
        
        nextGrid = grid.nextGeneration()
        self.assertEquals( None, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
        
    def testTwoNeighbors(self):
        '''
        A live cell lives on when there are two neighbors  
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 2, value = 2220 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        grid.setCell( row = 2, column = 2, layer = 3, value = 223 )
        
        nextGrid = grid.nextGeneration()
        self.assertEquals( 2221, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
      
    def testThreeNeighbors(self):
        '''
        A live cell lives on when there are three neighbors  
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 2, value = 2220 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        grid.setCell( row = 2, column = 2, layer = 3, value = 223 )
        grid.setCell( row = 1, column = 2, layer = 3, value = 123 )
        
        nextGrid = grid.nextGeneration()
        self.assertEquals( 2221, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
      
    def testThreeNeighborsSeed(self):
        '''
        A empty gets a seed when there are three neighbors  
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        grid.setCell( row = 2, column = 2, layer = 3, value = 223 )
        grid.setCell( row = 1, column = 2, layer = 3, value = 123 )
        
        nextGrid = grid.nextGeneration()
        self.assertEquals( 1, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
      
    def testThreeNeighborsRevive(self):
        '''
        A dead gets a seed when there are three neighbors  
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 2, value = 0 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        grid.setCell( row = 2, column = 2, layer = 3, value = 223 )
        grid.setCell( row = 1, column = 2, layer = 3, value = 123 )
        
        nextGrid = grid.nextGeneration()
        self.assertEquals( 1, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
    
    def testDieWithFourNeighbors(self):
        '''
        Live cell with four neighbors dies. (Crowded out)
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 2, value = 2220 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        grid.setCell( row = 2, column = 2, layer = 3, value = 223 )
        grid.setCell( row = 1, column = 2, layer = 3, value = 123 )
        grid.setCell( row = 1, column = 2, layer = 1, value = 121 )
        
        nextGrid = grid.nextGeneration()
        self.assertEquals( 0, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
        
    def testPassWithFourNeighbors(self):
        '''
        Empty cell with four neighbors stays empty. 
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        grid.setCell( row = 2, column = 2, layer = 3, value = 223 )
        grid.setCell( row = 1, column = 2, layer = 3, value = 123 )
        grid.setCell( row = 1, column = 2, layer = 1, value = 121 )
        
        nextGrid = grid.nextGeneration()
        self.assertEquals( None, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
        
    def testRandom(self):
        '''
        Randomly populate a grid
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        nextGrid = grid.seedAtRandom( percentage = 50 )
        self.assertFalse( nextGrid.isAllDead(), 'Should be about 50 % populated' )
        
    def testFlasher(self):
        '''
        See if the rule generates the "flasher" pattern
        ''' 
        grid = Grid3D( rows = 5, columns = 5, layers = 5 )
        grid.setCell( row = 3, column = 2, layer = 3, value = 3230 )
        grid.setCell( row = 3, column = 3, layer = 3, value = 3330 )
        grid.setCell( row = 3, column = 4, layer = 3, value = 3430 )
      
        secondGrid = grid.nextGeneration()
        # Following follows the 2D pattern
        self.assertEquals(       1, secondGrid.getCell( row = 2, column = 3, layer = 3 ) )
        self.assertEquals( 3331, secondGrid.getCell( row = 3, column = 3, layer = 3 ) )
        self.assertEquals(       1, secondGrid.getCell( row = 4, column = 3, layer = 3 ) )
        
        #  As in 2D these cells die
        self.assertEquals(       0, secondGrid.getCell( row = 3, column = 2, layer = 3 ) )
        self.assertEquals(       0, secondGrid.getCell( row = 3, column = 4, layer = 3 ) )
             
        # But we will also get seeds in the third dimension
        self.assertEquals(       1, secondGrid.getCell( row = 3, column = 3, layer = 2 ) )
        self.assertEquals(       1, secondGrid.getCell( row = 3, column = 3, layer = 4 ) )
        # Including the diagonals
        self.assertEquals(       1, secondGrid.getCell( row = 2, column = 3, layer = 2 ) )
        self.assertEquals(       1, secondGrid.getCell( row = 4, column = 3, layer = 2 ) )
        self.assertEquals(       1, secondGrid.getCell( row = 2, column = 3, layer = 4 ) )
        self.assertEquals(       1, secondGrid.getCell( row = 4, column = 3, layer = 4 ) )
        
        thirdGrid = secondGrid.nextGeneration()
        # Frankly, things are a little complicated at this point; and I cannot predict the outcome.
        thirdGrid.printLiveCells( liveMessage = 'Third Grid Live Cell' )
        
    def testNexGenerationViaSelectedRule(self):
        '''
        Enable different rules to be selected.
        '''
        '''
        A dead gets a seed when there are three neighbors  
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 2, value = 0 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        grid.setCell( row = 2, column = 2, layer = 3, value = 223 )
        grid.setCell( row = 1, column = 2, layer = 3, value = 123 )
        
        nextGrid = grid.nextGenerationViaSelectedRules( grid.rule2, grid.countLiveNeighbors )
        self.assertEquals( 1, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )

        
    def testNexGenerationWithFourRules(self):
        '''
        Enable different rules to be defined.
        '''
        
        def thisSeedRule( cellValue, nNeighbors ):
            if nNeighbors == 3:   
                return True                 # Curiously, exactly 3 neighbors makes a seed
            else:
                return False
            
        def thisKillRule( cellValue, nNeighbors ):
            if nNeighbors > 3 or nNeighbors < 2:
                return True
            else:
                return False
        '''
        Live cell dies when there are no neighbors
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 2, value = 2220 )
        nextGrid = grid.nextGenerationViaSelectedRuleSet( grid.rule3, grid.countLiveNeighbors, thisSeedRule, thisKillRule)
        self.assertEquals( 0, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
        '''
        Empty cell stays empty when there are no neighbors
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        nextGrid = grid.nextGenerationViaSelectedRuleSet( grid.rule3, grid.countLiveNeighbors, thisSeedRule, thisKillRule)
        self.assertEquals( None, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
                
        '''
        Live cell dies when there is only one neighbor
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 2, value = 2220 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        
        nextGrid = grid.nextGenerationViaSelectedRuleSet( grid.rule3, grid.countLiveNeighbors, thisSeedRule, thisKillRule)
        self.assertEquals( 0, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
        
        '''
        Empty cell stays empty when there is only one neighbor
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 22 )
        
        nextGrid = grid.nextGenerationViaSelectedRuleSet( grid.rule3, grid.countLiveNeighbors, thisSeedRule, thisKillRule)
        self.assertEquals( None, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
        
        '''
        A live cell lives on when there are two neighbors  
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 2, value = 2220 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        grid.setCell( row = 2, column = 2, layer = 3, value = 223 )
        
        nextGrid = grid.nextGenerationViaSelectedRuleSet( grid.rule3, grid.countLiveNeighbors, thisSeedRule, thisKillRule)
        self.assertEquals( 2221, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
      
        '''
        A live cell lives on when there are three neighbors  
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 2, value = 2220 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        grid.setCell( row = 2, column = 2, layer = 3, value = 223 )
        grid.setCell( row = 1, column = 2, layer = 3, value = 123 )
        
        nextGrid = grid.nextGenerationViaSelectedRuleSet( grid.rule3, grid.countLiveNeighbors, thisSeedRule, thisKillRule)
        self.assertEquals( 2221, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
      
        '''
        A empty gets a seed when there are three neighbors  
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        grid.setCell( row = 2, column = 2, layer = 3, value = 223 )
        grid.setCell( row = 1, column = 2, layer = 3, value = 123 )
        
        nextGrid = grid.nextGenerationViaSelectedRuleSet( grid.rule3, grid.countLiveNeighbors, thisSeedRule, thisKillRule)
        self.assertEquals( 1, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
      
        '''
        A dead gets a seed when there are three neighbors  
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 2, value = 0 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        grid.setCell( row = 2, column = 2, layer = 3, value = 223 )
        grid.setCell( row = 1, column = 2, layer = 3, value = 123 )
        
        nextGrid = grid.nextGenerationViaSelectedRuleSet( grid.rule3, grid.countLiveNeighbors, thisSeedRule, thisKillRule)
        self.assertEquals( 1, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
    
        '''
        Live cell with four neighbors dies. (Crowded out)
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 2, value = 2220 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        grid.setCell( row = 2, column = 2, layer = 3, value = 223 )
        grid.setCell( row = 1, column = 2, layer = 3, value = 123 )
        grid.setCell( row = 1, column = 2, layer = 1, value = 121 )
        
        nextGrid = grid.nextGenerationViaSelectedRuleSet( grid.rule3, grid.countLiveNeighbors, thisSeedRule, thisKillRule)
        self.assertEquals( 0, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )
        
        '''
        Empty cell with four neighbors stays empty. 
        '''
        grid = Grid3D( rows = 3, columns = 3, layers = 3 )
        grid.setCell( row = 2, column = 2, layer = 1, value = 221 )
        grid.setCell( row = 2, column = 2, layer = 3, value = 223 )
        grid.setCell( row = 1, column = 2, layer = 3, value = 123 )
        grid.setCell( row = 1, column = 2, layer = 1, value = 121 )
        
        nextGrid = grid.nextGenerationViaSelectedRuleSet( grid.rule3, grid.countLiveNeighbors, thisSeedRule, thisKillRule)
        self.assertEquals( None, nextGrid.getCell( row = 2, column = 2, layer = 2 ) )

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
