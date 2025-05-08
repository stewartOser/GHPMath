var bubbles = []; // Call this grapes
var bounced = false;
var black = 0;
var mult = 1;

function Bubble() { // Call this Orb
  this.d = 40;
  this.x = random(this.d, width-this.d);
  this.y = random(this.d, height-this.d);

  this.clr = [random(255), random(255), random(255), random(100,200)];

  // ()v signals velocity
  var speed = 0.1;
  this.xv = speed*random(-3, 3);
  this.yv = speed*random(-3, 3);

  this.draw = function() {
    fill(this.clr);
    circle(this.x, this.y, this.d);
  }

  this.move = function() {
    this.x += this.xv;
    this.y += this.yv;
    // Not what we wanted WOOHOO!!!

    var acceleration = -1;
    if (this.y <= this.d/2 || this.y >= height-this.d/2) {
      this.yv *= acceleration;
      bounced = true;
    }

    if (this.x <= this.d/2 || this.x >= width-this.d/2) {
      this.xv *= acceleration;
      bounced = true;
    }



  }
}

// Orbs --> new Orb()
// grapes --> grapes[0]

function setup() {
  createCanvas(windowWidth, windowHeight);
  stroke(255);

  for (var i = 0; i < 60; i++) {
    bubbles.push(new Bubble());
  }
}

function draw() {
  if (bounced) {
    black += mult;
    bounced = false;
  }
  background(black);

  if (black == 255){
    mult = -1;
  } else if (black == 0) {
    mult = 1;
  }
  stroke(255 - black);

  for (var i = 0; i < bubbles.length; i++) {
    bubbles[i].draw();
    bubbles[i].move();
  }

}
