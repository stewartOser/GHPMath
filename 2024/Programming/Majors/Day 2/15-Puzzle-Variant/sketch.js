var board = [['1', '2', '3', '4'],
             ['5', '6', '7', '8'],
             ['9', '10', '11', '12'],
             ['13', '14', '15', '']];

// Let's make a color board instead
var colorboard = [['r', 'r', 'r', 'r'],
                  ['g', 'g', 'g', 'g'],
                  ['b', 'b', 'b', 'b'],
                  ['e', 'e', 'e', '']];

var scrambled = false;

function colorpick(row, col){
  if (colorboard[row][col] == 'r'){
    fill(100, 0, 0);
  } else if (colorboard[row][col] == 'g'){
    fill(50, 0, 0);
  } else if (colorboard[row][col] == 'b'){
    fill(150, 0, 0);
  } else if (colorboard[row][col] == 'e'){
    fill(200, 0, 0);
  } else {
    fill(101, 67, 33);
  }
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  textSize(40);
}

function draw() {
  background(50);
  strokeWeight(5);
  stroke(0);

  for (var i = 0; i < 4; i++) {
    // i == row, j == col
    for (var j = 0; j < 4; j++) {
      colorpick(i, j);
      strokeWeight(5);
      rect(100*j + 100, i*100 + 100, 100, 100, 5);
      stroke(255);
      strokeWeight(1);
      if ((i >= 2 && j >= 1) || i == 3) {
        noFill();
        text(board[i][j],100*j + 125,100*i + 165);
      } else {
        noFill();
        text(board[i][j],100*j + 140,100*i + 165);
      }
      fill(0);
      stroke(0);
    }
  }
  
  stroke(255);
  fill(0);
  rect(100, 550, 400, 100, 10);
  fill(255);
  noStroke();
  text('SCRAMBLE!', 185, 615);
}

function conditions(row, col) {
  if (col < 3 && board[row][col+1] == '') {
    board[row][col+1] = board[row][col];
    board[row][col] = '';
    a = colorboard[row][col+1];
    colorboard[row][col+1] = colorboard[row][col];
    colorboard[row][col] = a;
  }
  if (col > 0 && board[row][col-1] == '') {
    board[row][col-1] = board[row][col];
    board[row][col] = '';
    a = colorboard[row][col-1];
    colorboard[row][col-1] = colorboard[row][col];
    colorboard[row][col] = a;
  }
  if (row < 3 && board[row+1][col] == '') {
    board[row+1][col] = board[row][col];
    board[row][col] = '';
    a = colorboard[row+1][col];
    colorboard[row+1][col] = colorboard[row][col];
    colorboard[row][col] = a;
  }
  if (row > 0 && board[row-1][col] == '') {
    board[row-1][col] = board[row][col];
    board[row][col] = '';
    a = colorboard[row-1][col];
    colorboard[row-1][col] = colorboard[row][col];
    colorboard[row][col] = a;
  }
}

function scramble() {
  for (var i = 1; i <= 10000; i++){
    row = floor(random(4));
    col = floor(random(4));
    conditions(row, col);
  }
  scrambled = true;
}


function mousePressed(){
  if (mouseY > 550 && mouseY < 650) {
    scramble();
    return;
  }
  var row = floor((mouseY - 100) / 100);
  var col = floor((mouseX - 100) / 100);

  conditions(row, col);

  // console.log(row, col, board[row][col]);
}