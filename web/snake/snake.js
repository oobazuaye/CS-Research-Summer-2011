function checkSupported() {
  canvas = document.getElementById('canvas');
  if (canvas.getContext){
    ctx = canvas.getContext('2d');
    this.gridSize = 10;
    start();
  } else {
    alert("We're sorry, but your browser does not support the canvas tag. Please use any web browser other than Internet Explorer.");
  }
}

function start(){
  this.currentPosition = {'x':50, 'y':50};
  autoSnake = false;
  snakeBody = [];
  visited = Array();
  path = Array();
  snakeLength = 3;
  noms = [];
  ctx.clearRect(0,0, canvas.width, canvas.height);
  updateScore();
  makeFoodItem();
  drawSnake();
  direction = 'right';
  oldDirection = null;
  play();
}

function restart(){
  pause();
  //ctx.fillStyle = "rgb(254, 0, 254)"; ctx.fillText('POOOOOP', 100, currentPosition['y']);
  start();
}

function pause(){
  clearInterval(interval);
  clearInterval(foods);
  clearInterval(rot);
  allowPressKeys = false;
}

function play(){
  interval = setInterval(moveSnake,100);
  foods = setInterval(makeFoodItem,2000);
  rot = setInterval(removeFoodItem,3000);
  allowPressKeys = true;
}

function drawSnake() {
  if (snakeBody.some(hasEatenItself) == true) {
    gameOver();
    return false;
  }
  snakeBody.unshift([currentPosition['x'], currentPosition['y']]);
  ctx.fillStyle = "rgb(200,0,0)";
  ctx.fillRect(currentPosition['x'], currentPosition['y'], gridSize, gridSize);
  if (snakeBody.length > snakeLength) {
    var itemToRemove = snakeBody.pop();
    ctx.clearRect(itemToRemove[0], itemToRemove[1], gridSize, gridSize);
  }
  nomCheck = hasFoundNom();
  if (nomCheck[0] == true) {
    makeFoodItem();
    snakeLength += 1;
    updateScore();
    noms.splice(nomCheck[1], 1);
  }
  
}

function leftPosition(){
 return currentPosition['x'] - gridSize;  
}

function rightPosition(){
  return currentPosition['x'] + gridSize;
}

function upPosition(){
  return currentPosition['y'] - gridSize;  
}

function downPosition(){
  return currentPosition['y'] + gridSize;
}

function whichWayToGo(axisType){  
  if (axisType=='x') {
    a = (currentPosition['x'] > canvas.width / 2) ? moveLeft() : moveRight();
  } else {
    a = (currentPosition['y'] > canvas.height / 2) ? moveUp() : moveDown();
  }
}

function moveUp(){
  if (upPosition() >= 0) {
    executeMove('up', 'y', upPosition());
  } else {
    whichWayToGo('x');
  }
}

function moveDown(){
  if (downPosition() < canvas.height) {
    executeMove('down', 'y', downPosition());    
  } else {
    whichWayToGo('x');
  }
}

function moveLeft(){
  if (leftPosition() >= 0) {
    executeMove('left', 'x', leftPosition());
  } else {
    whichWayToGo('y');
  }
}

function moveRight(){
  if (rightPosition() < canvas.width) {
    executeMove('right', 'x', rightPosition());
  } else {
    whichWayToGo('y');
  }
}

function executeMove(dirValue, axisType, axisValue) {
  direction = dirValue;
  currentPosition[axisType] = axisValue;
  drawSnake();
}

function reverse(){
  last = snakeBody.pop();
  secondToLast = snakeBody.pop();
  snakeBody.reverse()
  currentPosition['x'] = last[0];
  currentPosition['y'] = last[1];
  snakeBody.unshift(secondToLast);
  snakeBody.unshift(last);
  if (secondToLast[0] == last[0] && last[1] - gridSize == secondToLast[1])
  {direction = 'down';}
  else if (secondToLast[0] == last[0] && last[1] + gridSize == secondToLast[1])
  {direction = 'up';}
  else if (secondToLast[1] == last[1] && last[0] - gridSize == secondToLast[0])
  {direction = 'right';}
  else
  {direction = 'left';}
}

function makeFoodItem(){
  suggestedPoint = [Math.floor(Math.random()*(canvas.width/gridSize))*gridSize, Math.floor(Math.random()*(canvas.height/gridSize))*gridSize];
  if (isBody(suggestedPoint) || isNom(suggestedPoint)) {
    makeFoodItem();
  } else {
    ctx.fillStyle = "rgb(10,100,0)";
    ctx.fillRect(suggestedPoint[0], suggestedPoint[1], gridSize, gridSize);
    noms.push(suggestedPoint)
  }
}

function removeFoodItem(){
    if (noms.length > 1)
    {var itemToRemove = noms.shift();
    ctx.clearRect(itemToRemove[0], itemToRemove[1], gridSize, gridSize);
    }}

function hasPoint(element, index, array) {
  return (element[0] == suggestedPoint[0] && element[1] == suggestedPoint[1]);
}

function isBody(point){
    for (part in snakeBody){
        if (snakeBody[part][0] == point[0] && snakeBody[part][1] == point[1])
            {return true;}}
    return false;}

function hasEatenItself(element, index, array) {
  return (element[0] == currentPosition['x'] && element[1] == currentPosition['y']);  
}

function hasFoundNom(){
    for(nom in noms){
    if (noms[nom][0] == currentPosition['x'] && noms[nom][1] == currentPosition['y']){
        return [true, nom];}}
    return [false, 0];}

function isVisited(point){
    for(cell in visited){
    if (visited[cell][0] == point[0] && visited[cell][1] == point[1]){
        return true;}}
    return false;}


function isPath(point){
    for(cell in path){
    if (path[cell][0] == point[0] && path[cell][1] == point[1]){
        return true;}}
    return false;}

function isNom(point){
    for(nom in noms){
    if (noms[nom][0] == point[0] && noms[nom][1] == point[1]){
        return true;}}
    return false;}

function isBorder(point){
    if (point[0] < 0 || point[0] >= canvas.width)
        {return true;}
    if (point[1] < 0 || point[1] >= canvas.height)
        {return true;}
    return false;
}

function isOpen(point){
    if ((isBorder(point) == false && isBody(point) == false) || (isNom(point) == true)) 
    {return true;} return false;
}

function multiBFS()
  { start = [currentPosition['x'], currentPosition['y'], null];
    //System.out.println("Breadth-first search\n");
    var cellsToVisit = [];
    //if (isBorder(start)) {ctx.fillStyle = "rgb(300,200,100)"; ctx.fillRect(start[0], start[1], gridSize, gridSize); return 'POOP';}
    visited = Array();
    path = Array();
    visited.push(start);
    startRow = start[0];
    startCol = start[1];
    northNeighbor1 = [startRow, startCol - gridSize, start];
    southNeighbor1 = [startRow, startCol + gridSize, start];
    eastNeighbor1 = [startRow + gridSize, startCol, start];
    westNeighbor1 = [startRow - gridSize, startCol, start];
    //start.visited = true;
    cellsToVisit.unshift(start);
    while (cellsToVisit.length > 0)
    {
      current = cellsToVisit.pop();
      //ctx.font = '40pt Calibri'
      //ctx.fillText(current[1], 10, currentPosition['y'] * cellsToVisit.length);
      // not the destination, unshift neighbors if unmarked and not walls
      northNeighbor = [current[0], current[1] - gridSize, current];
      southNeighbor = [current[0], current[1] + gridSize, current];
      eastNeighbor = [current[0] + gridSize, current[1], current];
      westNeighbor = [current[0] - gridSize, current[1], current];
 
      if (isNom(current) == true) // have we reached the goal?
      {
        //ctx.fillText('SUCCESS!!', 10, currentPosition['y']);
        //ctx.fillStyle = "rgb(100,120,200)"; ctx.fillRect(current[0], current[1], gridSize, gridSize); 
        pathElement = current[2];
        while (pathElement != start || pathElement[2] != null)
        {
          path.push(pathElement);
          //ctx.fillStyle = "rgb(254,200,100)"; ctx.fillRect(pathElement[0], pathElement[1], gridSize, gridSize); 
          pathElement = pathElement[2];
        }
        // nextInPath = null;
        
        if (isPath(northNeighbor1) == true || isNom(northNeighbor1) == true) {return 'up';}
        if (isPath(southNeighbor1) == true || isNom(southNeighbor1) == true) {return 'down';}
        if (isPath(eastNeighbor1) == true || isNom(eastNeighbor1) == true) {return 'right';}
        if (isPath(westNeighbor1) == true || isNom(westNeighbor1) == true) {return 'left';}
        return null;
        /*
        if (isPath(northNeighbor1) == true || isNom(northNeighbor1) == true) {nextInPath = northNeighbor1;}
        if (isPath(southNeighbor1) == true || isNom(southNeighbor1) == true) {nextInPath = southNeighbor1;}
        if (isPath(eastNeighbor1) == true || isNom(eastNeighbor1) == true) {nextInPath = eastNeighbor1;}
        if (isPath(westNeighbor1) == true || isNom(westNeighbor1) == true) {nextInPath = westNeighbor1;}
        
        if (nextInPath == northNeighbor1) {return 'up';}
        if (nextInPath == southNeighbor1) {return 'down';}
        if (nextInPath == eastNeighbor1) {return 'right';}
        if (nextInPath == westNeighbor1) {return 'left';}
        return nextInPath; */
      }
      if (isVisited(southNeighbor) == false && isOpen(southNeighbor))
      {
        visited.push(southNeighbor);
        southNeighbor[2] = current;
        cellsToVisit.unshift(southNeighbor);
      }

      if (isVisited(eastNeighbor) == false && isOpen(eastNeighbor))
      {
        visited.push(eastNeighbor);
        eastNeighbor[2] = current;
        cellsToVisit.unshift(eastNeighbor);
      }

      if (isVisited(westNeighbor) == false && isOpen(westNeighbor))
      {
        visited.push(westNeighbor);
        westNeighbor[2] = current;
        cellsToVisit.unshift(westNeighbor);
      }

      if (isVisited(northNeighbor) == false && isOpen(northNeighbor))
      {
        visited.push(northNeighbor);
        northNeighbor[2] = current;
        cellsToVisit.unshift(northNeighbor);
      }


    } // end while cellsToVisit is not empty 

    //ctx.fillStyle = "rgb(254, 0, 254)"; ctx.fillText('POOOOOP', 100, currentPosition['y']);
    return null;
  }
  
function gameOver(){
  autoSnake = false;
  var score = (snakeLength - 3)*10;
  pause();
  alert("Game Over. Your score was "+ score);
  ctx.clearRect(0,0, canvas.width, canvas.height);
  document.getElementById('play_menu').style.display='none';
  document.getElementById('restart_menu').style.display='block';
}

function updateScore(){
  var score = (snakeLength - 3)*10
  document.getElementById('score').innerText = score;
}

function auto(){
    // ctx.fillStyle = "rgb(100,120,200)"; ctx.fillRect(currentPosition['x'], 0, gridSize, gridSize); 
    autoSnake = true;
    go = multiBFS();
    //ctx.fillText(go, 10, currentPosition['y']);
        if (go == 'up'){
          if (direction != "down"){oldDirection = go;
           moveUp();} else{oldDirection = 'down'; moveDown();}}
        else if (go == 'down'){
          if (direction != "up"){oldDirection = go;
          moveDown();} else{oldDirection = 'up'; moveUp();}}
        else if (go == 'left'){
          if (direction != "right"){oldDirection = go;
          moveLeft();}else{oldDirection = 'right'; moveRight();}}
        else if (go == 'right'){
            if (direction != "left"){oldDirection = go;
            moveRight();}else{oldDirection = 'left'; moveLeft();}}
        else{
            reverse();
            go = multiBFS();
            if (go == null){
            reverse();
            go = multiBFS();
            if (go == null){autoSnake = false; direction = oldDirection; moveSnake();}}}
}

document.onkeydown = function(event) {
  if (!allowPressKeys){
    return null;
  }
  var keyCode; 
  if(event == null)
  {
    keyCode = window.event.keyCode; 
  }
  else 
  {
    keyCode = event.keyCode; 
  }
 
  switch(keyCode)
  {
    case 83:
    reverse();
      break;
      
    case 65:
      auto();
      break;
      
    case 37:
      autoSnake = false;
      if (direction != "right"){
        moveLeft();
      }
      break;
     
    case 38:
      autoSnake = false;
      if (direction != "down"){
        moveUp();
      }
      break; 
      
    case 39:
      autoSnake = false;
      if (direction != "left"){
        moveRight();
      }
      break; 
    
    case 40:
      autoSnake = false;
      if (direction != "up"){
        moveDown();
      }
      break; 
      
    default:
      break; 
  } 
}

function moveSnake(){
  if (autoSnake == true){auto(); }
  if (autoSnake == false){
  switch(direction){
    case 'up':
      moveUp();
      break;

    case 'down':
      moveDown();
      break;
      
    case 'left':
      moveLeft();
      break;

    case 'right':
      moveRight();
      break;
  }

}}
