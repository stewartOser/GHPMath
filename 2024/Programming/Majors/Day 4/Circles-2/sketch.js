var balls = [];

function Ball() {
  this.d = random(20, 50);
  this.x = random(this.d/2,width-this.d/2);
  this.y = random(this.d/2,height-this.d/2);
  this.clr = [random(255),random(255),random(255),random(100,200)];
  this.xvel = random(-3,3)*10/this.d;
  this.yvel = random(-3,3)*10/this.d;
  this.draw = function() {
    fill(this.clr[0],this.clr[1],this.clr[2],this.clr[3]);
    circle(this.x,this.y,this.d);
  }
  this.move = function() {
    this.x = this.x + this.xvel;
    if(this.x < this.d/2 || this.x > width-this.d/2){
      this.xvel = -1*this.xvel;
    } 
    this.y = this.y + this.yvel;
    if(this.y < this.d/2 || this.y > height-this.d/2){
      this.yvel = -1*this.yvel;
    } 
  }
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  for (var i = 0; i <= 60; i++) {
    balls.push(new Ball());
  }
}

function draw() {
  background(220);
  for (b in balls) {
    balls[b].draw();
    balls[b].move();
  }
}
