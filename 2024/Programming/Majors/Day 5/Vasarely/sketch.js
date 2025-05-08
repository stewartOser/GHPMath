function setup() {
  createCanvas(600, 600);
  background(220);
  noLoop();
  rectMode(CENTER);
  noStroke();
}

function draw() {
  for (var i = 25; i < 600; i += 25) {
    for (var j = 25; j < 600; j += 25) {
      fill(random(255), random(255), random(255));
      square(i,j,25);
      fill(random(255),random(255),random(255));

      var shape = floor(random(0, 3));
      if (shape <= 1) {
        var dim = random(15, 23)
        circle(i,j,dim, dim)
      } else {
        square(i, j, random(15, 20));
      }
    }
  }
}
