function setup() {
  createCanvas(800, 800);
  ellipseMode(CENTER);
  angleMode(DEGREES);
  noLoop();
}

function draw() {
  background(0, 100, 0);
  //for (var r = 0; r < 10; r++) {
    //for (var c = 0; c < 10; c++) {
      //push();
      //translate(c*80 + 20, r*80 + 20);
      translate(width/2, height/2);
      drawFlower(0, 0, 200, floor(random(5, 8) * 2));
      //pop();

      //firstFlower(40+c*80, 40+r*80, 40, 4);
    //}
  //}
}

function firstFlower(x, y, size, npetals) {
  var ang = 360/npetals;

  fill(random(255), random(255), random(255));
  for (var p = 0; p <= npetals; p++) {
    circle(x+size/2*cos(ang*p), y+size/2*sin(ang*p),size);
  }

  fill(random(255), random(255), random(255));
  circle(x, y, size);
}

function drawFlower(x, y, size, npetals) {
  var ang = 360/npetals;
  
  fill(255, 255, 0)
  for (var p = 1; p <= npetals; p++) {
    push();
    translate(size/2*cos(ang*p), size/2*sin(ang*p));
    rotate(ang*p);
    ellipse(x, y, size, size/2);
    pop();
  }

  fill(150, 100, 0)
  circle(x, y, size)
}
