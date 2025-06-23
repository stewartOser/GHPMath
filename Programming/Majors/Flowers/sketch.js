function setup() {
  createCanvas(600, 600);
  noLoop();
}

function makeFlower(x, y, size) {
  fill(random(255), random(255), random(255));
  circle(x, y + (size / 2), size);
  circle(x, y - (size / 2), size);
  circle(x + (size / 2), y, size);
  circle(x - (size / 2), y, size);

  fill(random(255), random(255), random(255));
  circle(x, y, size);
}

function draw() {
  background(220);

  for (var x = 25; x < 600; x += 50) {
    for (var y = 25; y < 600; y += 50) {
      makeFlower(x, y, random(10, 25));
    }
  }
}
