/* This is the start of a simple p5.js sketch using p5-matter.
 Use this as a template for creating your own sketches! */

var ball;
var floor, leftWall, rightWall;
var testPeg;

var pegArr = [];
var ballArr = [];
var blockArr = [];

function setup() {
  // put setup code here.
  window = createCanvas(600, 600);
  matter.init();
  matter.mouseInteraction(window);

  rectMode(CENTER);
  ellipseMode(CENTER);
  textAlign(CENTER);

  // testPeg = matter.makeBall(width/2, height/2, 5);
  // testPeg.freeze();

  let offSet, eitherOr;
  eitherOr = 0;
  for (var x = 50; x < width; x += 50) {
    for (var y = 100; y < height; y += 50) {
      if (eitherOr % 2 == 1) {
        offset = 25;
      } else {
        offset = 0;
      }

      if (x+offset < width-25) {
        let peg = matter.makeBall(x+offset, y, 5, { isStatic: true });
        pegArr.push(peg);
      }

      eitherOr++;
    }
  }

  for (var i = 75; i < width-50; i += 50) {
    let block = matter.makeBarrier(i, height - 10, 5, 25);
    blockArr.push(block);
  }


  // ball = matter.makeBall(width / 2, 40, 37, { restitution: 0.905 });
  floor = matter.makeBarrier(width / 2, height, width, 10);
  leftWall = matter.makeBarrier(0, height/2, 10, height);
  rightWall = matter.makeBarrier(width, height/2, 10, height);
}

function draw() {
  // put the drawing code here
  background(0);

  stroke(150);
  strokeWeight(3);
  noFill();

  textFont("Oswald"); textSize(50);
  text('PLINKO', width/2, 65);

  noStroke();

  fill(127);
  floor.show();
  leftWall.show();
  rightWall.show();

  blockArr.forEach(function(block) {
    block.show();
  });

  fill(255);
  // ball.show();
  // testPeg.show();
  ballArr.forEach(function(ball) {
    ball.show();
  });

  pegArr.forEach(function(peg) {
    peg.show();
  });

}

function mousePressed() {
  if (mouseY < 100) {
    let newBall = matter.makeBall(mouseX, mouseY, 30, { restitution: 0.905 });
    ballArr.push(newBall);
  }
}
