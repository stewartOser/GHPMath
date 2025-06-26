class Ball {
  // will be called when we initialize the class
  // to initialize == to make a new instance of
  // instance == object basically
  constructor() {
    // properties begin with this.property
    // these things are known to the object
    // like I know my name is Stewart
    // i would havee this.name = Stewart
    this.x = random(800);
    this.y = random(800);
    this.d = random(10, 100);
    // fourth option is alpha value
    this.clr = [random(255), random(255), random(255), random(255)];
  }

  // methods are actions that our object can take
  // for example, a Stewart object could have a method
  // program(), which would maybe write a program
  draw() {
    fill(this.clr);
    circle(this.x, this.y, this.d);
  }
}

// to make it radius rather than diameter
// ellipseMode(RADIUS)
// in setup

function setup() {
  createCanvas(800, 800);
  background(0);
}

function draw() {
  // new means to instantiate the object
  var orb = new Ball();
  orb.draw();
}
