var inside = 0;
var total = 0;

function setup() {
  createCanvas(400, 400);
  ellipseMode(RADIUS);
  background(255);
  fill(0);
  stroke(255);
  // circle(0,400,width);
}

function draw() {
  // Pick random points
  var x = random(0, 1);
  var y = random(0, 1);
  total++;

  // How far is it?
  if ((x*x + y*y) <= 1) {
    inside++;
    fill(0, 0, 255);
    stroke(0, 0, 255);
  } else {
    fill(255, 0, 0);
    stroke(255, 0, 0);
  }

  noStroke();
  circle(400*x, 400 - 400*y, 1);
  //point(400*x, 400 - 400*y);

  if (total % 100 == 0) {
    console.log(4*inside/total);
  };
}
