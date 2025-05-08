function Ball() {
  this.d = random(20, 400);
  this.x = random(0, width);
  this.y = random(0, height);
  
  this.col = [random(255), random(255), 
              random(255)];
  
  this.draw = function() {
    fill(this.col);
    circle(this.x, this.y, this.d);
  }
}

function setup() {
  createCanvas(800, 800);
  background(220);
  frameRate(60);
  rectMode(CENTER);
}

function draw() {
  // dennis == Ball object
  var dennis = new Ball();
  dennis.draw();
}
