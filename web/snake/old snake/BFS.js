protected MazeCell multiBFS(MazeCell start, char destination)
  {
    //System.out.println("Breadth-first search\n");
    Queue cellsToVisit = new Queue();
    start.visited = true;
    cellsToVisit.enqueue( start );
    while (!cellsToVisit.isEmpty())
    {
      MazeCell current = (MazeCell)cellsToVisit.dequeue();

     

      // not the destination, enqueue neighbors if unmarked and not walls
      int currentRow = current.row;
      int currentCol = current.col;
      MazeCell northNeighbor = maze[(currentRow-1)][currentCol];
      MazeCell southNeighbor = maze[(currentRow+1)][currentCol];
      MazeCell  eastNeighbor = maze[currentRow][(currentCol+1)];
      MazeCell  westNeighbor = maze[currentRow][(currentCol-1)];
 
      if (current.getContents() == destination) // have we reached the goal?
      {
        MazeCell pathElement = current.parent;
        while (pathElement != start && pathElement != null)
        {
          pathElement.contents = 'o';
          pathElement = pathElement.parent;
        }
        MazeCell nextInPath = null;
        int startRow = start.getRow();
        int startCol = start.getCol();
        MazeCell northNeighbor1 = maze[(startRow-1)][startCol];
        MazeCell southNeighbor1 = maze[(startRow+1)][startCol];
        MazeCell  eastNeighbor1 = maze[startRow][(startCol+1)];
        MazeCell  westNeighbor1 = maze[startRow][(startCol-1)];
        if (northNeighbor1.getContents() == 'o' || northNeighbor1.getContents() == 'D') {nextInPath = northNeighbor1;}
        if (southNeighbor1.getContents() == 'o' || southNeighbor1.getContents() == 'D') {nextInPath = southNeighbor1;}
        if (eastNeighbor1.getContents() == 'o' || eastNeighbor1.getContents() == 'D') {nextInPath = eastNeighbor1;}
        if (westNeighbor1.getContents() == 'o' || westNeighbor1.getContents() == 'D') {nextInPath = westNeighbor1;}
        clearFlags();
        return nextInPath;
      }
      if (!southNeighbor.visited && southNeighbor.isOpen())
      {
        southNeighbor.visited = true;
        southNeighbor.parent = current;
        cellsToVisit.enqueue(southNeighbor);
      }

      if (!eastNeighbor.visited && eastNeighbor.isOpen())
      {
        eastNeighbor.visited = true;
        eastNeighbor.parent = current;
        cellsToVisit.enqueue(eastNeighbor);
      }

      if (!westNeighbor.visited && westNeighbor.isOpen())
      {
        westNeighbor.visited = true;
        westNeighbor.parent = current;
        cellsToVisit.enqueue(westNeighbor);
      }

      if (!northNeighbor.visited && northNeighbor.isOpen())
      {
        northNeighbor.visited = true;
        northNeighbor.parent = current;
        cellsToVisit.enqueue(northNeighbor);
      }


    } // end while cellsToVisit is not empty 

    System.out.println("\nMaze not solvable!");
    return null;
  }



  class MazeCell
  {

    private int row;                 // The row at which this cell is located
    private int col;                 // The col at which this cell is located
    private char contents;           // Each cell has contents (a char)
    private boolean visited;         // A cell can be marked as visited.
    private MazeCell parent;         // parent is where we came from!

    // Constructor of the MazeElement at row, col, with contents c
    //   "visited" is set to false, and "parent" is set to null
    private MazeCell(int row, int col, char c)
    {
      this.row = row;        // this is required to avoid name confusion!
      this.col = col;        // ditto
      this.contents = c;     
      this.visited = false;  // we haven't been here yet...
      this.parent = null;    // ... so we have no parent yet
    }



  private void clearFlags()
{
  for (int r = 0; r < maze.length; r++)
    for (int c = 0; c < maze[r].length; c++)
  {
    if (maze[r][c].contents == 'o') 
      maze[r][c].contents = ' ';
    if (maze[r][c].visited == true) 
      maze[r][c].visited = false;
  }
}
