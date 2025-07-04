let cw = 600;
let ch = 600;

function setup() {
  createCanvas(cw, ch);

  noLoop();
  rectMode(CENTER);
  ellipseMode(CENTER);
}

function draw() {
  background(220);

  for (var x = 25; x < cw; x += 50) {
    for (var y = 25; y < ch; y += 50) {
      fill(random(255), random(255), random(255));
      rect(x, y, 50, 50);

      fill(random(255), random(255), random(255));
      var d = random(20, 40);

      var choice = random(100);
      if (choice < 51) {
        // draw an ellipse
        ellipse(x, y, d, d);
      } else {
        // draw a rectangle
        rect(x, y, d, d);
      }
    }
  }
}
