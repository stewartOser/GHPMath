function setup() {
  createCanvas(600, 600);
  angleMode(DEGREES);
  noLoop();
}

function makeFlower(x, y, size) {
  var np = floor(random(2, 13));
  fill(random(255), random(255), random(255));
  for (var c = 0; c < np; c++) {
    var xOff = (size/2)*cos(360*c/np);
    var yOff = (size/2)*sin(360*c/np);
    circle(x + xOff, y + yOff, size);
  }

  fill(random(255), random(255), random(255));
  circle(x, y, size);
}

function draw() {
  background(220);

  for (var row = 0; row < 12; row++) {
    for (var col = 0; col < 12; col++) {
      makeFlower(25 + 50*col, 25 + 50*row, random(10, 25));
    }
  }

}
