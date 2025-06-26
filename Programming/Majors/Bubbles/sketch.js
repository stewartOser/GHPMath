var numBubbles = 600;
var bubbles = [];

class Bubble {
  constructor() {
    // position and diameter
    this.d = 25 /* or something */;
    this.x = random(this.d, width - this.d);
    this.y = random(this.d, height - this.d);

    // velocity
    this.xv = getVelocity();
    this.yv = getVelocity();
    
    // color
    this.clr = [random(255), random(255), random(255), random(150, 200)];
  }

  draw() {
    fill(this.clr);
    circle(this.x, this.y, this.d);
  } 

  move() {
    this.x = this.x + this.xv;
    this.y = this.y + this.yv;

    if (((this.x + this.d / 2) >= width) || ((this.x - this.d / 2) <= 0)) {
      this.xv = -this.xv;
    }

    if (((this.y + this.d / 2) >= height) || (this.y - this.d / 2) <= 0) {
      this.yv = -this.yv;
    }
  }

}

function getVelocity() {
  var v = random(-2, 2.0001);

  while (v == 0) {
    v = random(-3, 4);
  }

  return v;
}

function setup() {
  createCanvas(windowWidth, windowHeight);

  for (var b = 0; b < numBubbles; b++) {
    bubbles.push(new Bubble());
  }
}

function draw() {
  background(0);

  bubbles.forEach(function(ball) {
    ball.draw();
    ball.move();
  });
}
