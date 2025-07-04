let snake = [];
const SNAKE_LENGTH = 50;

class Body {

  constructor(prevSegment) {
    this.x = random(width);
    this.y = random(height);

    this.radius = 50;

    this.speed = 0.15;

    this.prevSegment = prevSegment;

    this.clr = [random(255), random(255), random(255)];
  }

  draw() {
    fill(this.clr);
    circle(this.x, this.y, this.radius);
  }

  move() {
    var shiftx;
    var shifty;

    if (this.prevSegment == null) {
      shiftx = mouseX - this.x;
      shifty = mouseY - this.y;
    }

    else {
      shiftx = this.prevSegment.x - this.x;
      shifty = this.prevSegment.y - this.y;
    }


    this.x += this.speed*shiftx;
    this.y += this.speed*shifty;
  }

}

function setup() {
  createCanvas(windowWidth, windowHeight);
  ellipseMode(RADIUS);

  snake.push(new Body(null));
  for (var folllow = 1; folllow < SNAKE_LENGTH; folllow++) {
    snake.push(new Body(snake[folllow-1]));
  }
}

function draw() {
  background(29, 29, 37);

  snake.forEach(function(body) {
    body.draw();
    if (mouseIsPressed) {
      body.move();
    }
  })
}