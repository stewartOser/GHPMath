let sigma, rho, beta, dx, dy, dz, dt, x, y, z;
let rot = 0;

let points = new Array();
let floaters = new Array();

class Floater {
  constructor() {
   this.x = random(-10, 10);
   this.y = random(-10, 10);
   this.z = random(-10, 10);
   
   this.clr = [random(150, 255), random(100, 200), random(50)]
  }
  
  draw() {
   stroke(this.clr);
   strokeWeight(5);
   point(this.x, this.y, this.z);
   strokeWeight(1);
  }
  
  move() {
   this.dx = (sigma*(-this.x + this.y)) * dt;
   this.dy = (-this.x*this.z + rho*this.x - this.y)*dt;
   this.dz = (this.x*this.y - beta*this.z)*dt;
   
   this.x += this.dx;
   this.y += this.dy;
   this.z += this.dz;
  }
}

function setup() {
  createCanvas(800, 800, WEBGL);
  blendMode(ADD);
  
  for (var i = 0; i < 500; i++) {
    floaters.push(new Floater()); 
  }
  
  sigma = 10;
  rho = 28;
  beta = 8/3;
  
  dt = 0.01;
  
  x = 1.10;
  y = 2.00;
  z = 7.00;
}


function draw() {
  background(0);
  
  dx = (sigma * (-x + y)) * dt;
  dy = (-x*z + rho*x - y) * dt;
  dz = (x*y - beta*z) * dt;
  
  x += dx;
  y += dy;
  z += dz;
  
  points.push(new p5.Vector(x, y, z));
  
  translate(0, 0, -80);
  scale(3.5);
  stroke(255);
  noFill();
  
  beginShape();
    for (let v of points) {
     stroke(255, 50, 50);
     vertex(v.x, v.y, v.z)
    }
  endShape();
  
  if (points.length > 1000) {
   floaters.forEach(function(f) {
     f.move();
     f.draw();
   });
  }
  
  let radius = 300;
  let camX = cos(radians(rot)) * radius;
  let camZ = sin(radians(rot)) * radius;
  camera(camX, 0, camZ, 0, 0, 0, 0, 1, 0);
  rot += 0.5;
  
}