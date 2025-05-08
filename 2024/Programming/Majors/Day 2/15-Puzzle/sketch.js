var board = [['1', '2', '3', '4'],
             ['5', '6', '7', '8'],
             ['9', '10', '11', '12'],
             ['13', '14', '15', '']];

var scrambled = false;

function setup() {
  createCanvas(600, 800);
  textSize(40);
}

function draw() {
  background(220);
  strokeWeight(5);
  stroke(0);
  fill(255);

  for (var i = 0; i < 4; i++) {
    // i == row, j == col
    for (var j = 0; j < 4; j++) {
      strokeWeight(5);
      rect(100*j + 100, i*100 + 100, 100, 100, 5);
      stroke(0);
      strokeWeight(1);
      fill(0);
      if (board[i][j] == '11'){
        text(board[i][j],100*j + 130,100*i + 165);
      } else if (board[i][j].length > 1) {
        text(board[i][j],100*j + 127,100*i + 165);
      } else {
        text(board[i][j],100*j + 140,100*i + 165);
      }
      fill(255);
      stroke(0);
    }
  }
  
  stroke(0);
  fill(255);
  rect(100, 550, 400, 100, 10);
  fill(0);
  text('SCRAMBLE!', 185, 615);
}

function conditions(row, col) {
  if (col < 3 && board[row][col+1] == '') {
    board[row][col+1] = board[row][col];
    board[row][col] = '';
  }
  if (col > 0 && board[row][col-1] == '') {
    board[row][col-1] = board[row][col];
    board[row][col] = '';
  }
  if (row < 3 && board[row+1][col] == '') {
    board[row+1][col] = board[row][col];
    board[row][col] = '';
  }
  if (row > 0 && board[row-1][col] == '') {
    board[row-1][col] = board[row][col];
    board[row][col] = '';
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