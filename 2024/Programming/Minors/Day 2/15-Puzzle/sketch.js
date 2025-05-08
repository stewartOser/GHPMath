var cat = [['1', '2', '3', '4'],
           ['5', '6', '7', '8'],
           ['9', '10', '11', '12'],
           ['13', '14', '15', '']];

//var cat stores our numbers

function setup() {
  createCanvas(600, 800);
  textSize(40);
}

function draw() {
  background(220);

  for (var row = 0; row < 4; row++) {
    for (var col = 0; col < 4; col++) {
      fill(255);
      rect(100*col + 100, 100*row + 100, 100, 100);
      fill(0);
      text(cat[row][col], 100*col + 130, 100*row + 165);
    }
  }

  
  fill(255);
  rect(100, 550, 400, 100);
  fill(0);
  text('SCRAMBLE!', 185, 615);

}

function conditions(row, col) {
  if (col < 3 && cat[row][col+1] == ''){
    cat[row][col+1] = cat[row][col];
    cat[row][col] = '';
  }

  if (col > 0 && cat[row][col-1] == ''){
    cat[row][col-1] = cat[row][col];
    cat[row][col] = '';
  }

  if (row < 3 && cat[row+1][col] == ''){
    cat[row+1][col] = cat[row][col];
    cat[row][col] = '';
  }

  if (row > 0 && cat[row-1][col] == ''){
    cat[row-1][col] = cat[row][col];
    cat[row][col] = '';
  }
}

function scramble() {
  for (var i = 1; i <= 10000; i++) {
    var row = floor(random(4));
    var col = floor(random(4));
    conditions(row, col);
  }
}

function mousePressed() {
  if (mouseY > 550 && mouseY < 650) {
    scramble();
    return;
  }

  var col = floor(mouseX/100) - 1;
  var row = floor(mouseY/100) - 1;

  conditions(row, col);

  console.log(cat[row][col]);
}