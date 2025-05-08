function setup() {
  createCanvas(800, 800);
  background(220);
  ellipseMode(RADIUS);

  fill(220);
  for (var i = 400; i >= 100; i -= 100) {
    circle(width/2, height/2, i);
  }

  line(0, height/2, width, height/2);
  line(width/2, 0, width/2, height);

  noLoop();
}

function mousePressed() {
  fill(255, 0, 0);
  circle(mouseX, mouseY, 5);

  var x = (mouseX - 400) / 200;
  var y = (400 - mouseY) / 200;
  // console.log(x,y);

  var sqX = x*x - y*y;
  var sqY = 2*x*y;
  
  var scrX = 200*sqX + 400;
  var scrY = 400 - 200*sqY;

  fill(0, 0, 255);
  circle(scrX, scrY, 5);
}
