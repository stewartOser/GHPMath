let numbers = [["1", "2", "3", "4"],
               ["5", "6", "7", "8"],
               ["9", "10", "11", "12"],
               ["13", "14", "15", ""]];
// "" NOT " "

function setup() {
  createCanvas(600, 800);
  textSize(32);

  // I'm adding this, dont worry about it
  textAlign(CENTER, CENTER);
  console.log("Stewart is Awesome!");
}

function draw() {
  background(225);

  fill(165, 42, 42);
  rect(75, 75, 450, 450);
  strokeWeight(3);
  
  stroke(0);
  rect(100, 100, 400, 400, 7);
  fill(255);
  for (var row = 0; row < 4; row++) {
    for (var col = 0; col < 4; col++) {
      stroke(0);
      fill(181, 101, 29);
      if (numbers[row][col] != "") {
        rect(100 + 100*col, 100 + 100*row, 100, 100, 7);
      }
      fill(0);
      text(numbers[row][col], 150 + 100*col, 150 + 100*row);
    }
  }

  // last number is smoothness
  stroke(0);
  fill(255);
  rect(100, 600, 400, 100, 25);
  fill(0);
  stroke(255);
  text("SCRAMBLE", 300, 650);
}

function mouseClicked() {
  if (mouseX > 100 && mouseX < 400 && mouseY > 600 && mouseY < 700) {
    scramble()
  }

  if (mouseX > 99 && mouseX < 501 && mouseY > 99 && mouseY < 501) {
    var col = floor(mouseX / 100) - 1;
    var row = floor(mouseY / 100) - 1;

    slide(row, col);
  }
}

function slide(row, col) {
  // check left
  if(col > 0 && numbers[row][col - 1] == "") {
    numbers[row][col - 1] = numbers[row][col];
    numbers[row][col] = "";
  }

  // check right
  if(col < 3 && numbers[row][col + 1] == "") {
    numbers[row][col + 1] = numbers[row][col];
    numbers[row][col] = "";
  }

  // check up
  if(row > 0 && numbers[row - 1][col] == "") {
    numbers[row - 1][col] = numbers[row][col];
    numbers[row][col] = "";
  }

  // check down
  if(row < 3 && numbers[row + 1][col] == "") {
    numbers[row + 1][col] = numbers[row][col];
    numbers[row][col] = "";
  }
}

function scramble() {
  for (var cnt = 1; cnt <= 10000; cnt++) {
    row = floor(random(4));
    // returns a random number between 0 and 4, 0 included, 4 not

    col = floor(random(4));
    slide(row, col);
  }
}