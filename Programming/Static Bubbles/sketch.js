// bubbleList = []

class Bubble {
  constructor () {
    this.diameter = random(10, 100);
    this.x = random(this.diameter/2, width-this.diameter/2);
    this.y = random(this.diameter/2, height-this.diameter/2);

    this.clr = [random(255), random(255), random(255), random(150, 255)];
  }

  draw() {
    fill(this.clr);
    circle(this.x, this.y, this.diameter);
  }
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  background(220);
}

function draw() {
  // background(220);

  var b = new Bubble();
  b.draw();
  // bubbleList.push(b);

  // bubbleList.forEach(bubble=>{
  //   bubble.draw();
  // });

  // if (bubbleList.length > 200) {
  //   bubbleList.shift();
  // }
}

function mouseClicked() {
  background(220);
}
