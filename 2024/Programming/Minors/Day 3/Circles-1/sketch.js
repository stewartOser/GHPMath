var grapes = [];

function Orb() {
  this.d = random(100, 400);
  this.x = random(0, width);
  this.y = random(0, height);
  
  this.clr = [random(100), random(255), 
              random(100)];
  
  this.draw = function() {
    fill(this.clr);
    square(this.x, this.y, this.d);
  };
}

function setup() {
  createCanvas(800, 800);
  background(220);
  rectMode(CENTER);
}

function draw() {
  var grape = new Orb();
  grape.draw();
}
