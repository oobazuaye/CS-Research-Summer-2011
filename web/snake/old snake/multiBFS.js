function multiBFS()
  { start = [currentPosition['x'], currentPosition['y']];
    //System.out.println("Breadth-first search\n");
    var cellsToVisit = [];
    visited = []
    visited.push(start)
    //start.visited = true;
    cellsToVisit.unshift( start );
    while (cellsToVisit != [])
    {
      current = cellsToVisit.pop();

      // not the destination, unshift neighbors if unmarked and not walls
      northNeighbor = [current[0] - gridSize, current[1]];
      southNeighbor = [current[0] + gridSize, current[1]];
      eastNeighbor = [current[0], current[1] + gridSize];
      westNeighbor = [current[0], current[1] - gridSize];
 
      if (isNom(current)) // have we reached the goal?
      {
        pathElement = current.parent;
        while (pathElement != start && pathElement != null)
        {
          visited.push(pathElement);
          pathElement = pathElement.parent;
        }
        nextInPath = null;
        startRow = currentPosition['x'];
        startCol = currentPosition['y'];
        northNeighbor1 = maze[(startRow-gridSize)][startCol];
        southNeighbor1 = maze[(startRow+gridSize)][startCol];
        eastNeighbor1 = maze[startRow][(startCol+gridSize)];
        westNeighbor1 = maze[startRow][(startCol-gridSize)];
        if (isVisited(northNeighbor1)|| isNom(northNeighbor1)) {nextInPath = northNeighbor1;}
        if (isVisited(southNeighbor1)|| isNom(southNeighbor1)) {nextInPath = southNeighbor1;}
        if (isVisited(eastNeighbor1)|| isNom(eastNeighbor1)) {nextInPath = eastNeighbor1;}
        if (isVisited(westNeighbor1)|| isNom(westNeighbor1)) {nextInPath = westNeighbor1;}
        visited = [];
        if (nextInPath == northNeighbor1) {return 'up';}
        if (nextInPath == southNeighbor1) {return 'down';}
        if (nextInPath == eastNeighbor1) {return 'right';}
        if (nextInPath == westNeighbor1) {return 'left';}
        return nextInPath;
      }
      if (isVisited(southNeighbor1) == false && isNom(southNeighbor1) == false)
      {
        visited.push(southNeighbor);
        southNeighbor.parent = current;
        cellsToVisit.unshift(southNeighbor);
      }

      if (isVisited(eastNeighbor1) == false && isNom(eastNeighbor1) == false)
      {
        visited.push(eastNeighbor);
        eastNeighbor.parent = current;
        cellsToVisit.unshift(eastNeighbor);
      }

      if (isVisited(westNeighbor1) == false && isNom(westNeighbor1) == false)
      {
        visited.push(westNeighbor);
        westNeighbor.parent = current;
        cellsToVisit.unshift(westNeighbor);
      }

      if (isVisited(northNeighbor1) == false && isNom(northNeighbor1) == false)
      {
        visited.push(northNeighbor);
        northNeighbor.parent = current;
        cellsToVisit.unshift(northNeighbor);
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

function isVisited(place){
    for(cell in visited){
    if (visited[cell][0] == place['x'] && visited[cell][1] == place['y']){
        return true;}}
    return false;}

function isNom(){
    for(nom in noms){
    if (noms[nom][0] == place['x'] && noms[nom][1] == place['y']){
        return true;}}
    return false;}
