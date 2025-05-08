var ballArr = [];
var floor, leftWall, rightWall;
var testPeg;
var pegArr = [];
var blockArr = [];

function makeRectanglePegArray() {
  let offset;
  for (var y = 100; y < height; y += 50) {
    for (var x = 25; x < width; x += 50) {
      if ((y / 10) % 2 == 1) {
        offset = 25;
      } else {
        offset = 0;
      }
      var peg = matter.makeBall(x + offset, y, 5, { isStatic: true });
      pegArr.push(peg);
    }
  }
}

function makeTrianglePegArray() {
  let offset = 0;
  for (var layer = 1; layer < height/50 - 1; layer++) {
    for (var i = 1; i < 13 - layer; i++) {
      var peg = matter.makeBall(i*50 + offset, height - 50*layer, 5, { isStatic: true });
      pegArr.push(peg);
    }
    offset += 25;
  }
}

function setup() {
  // put setup code here.
  var window = createCanvas(600, 600);
  matter.init();
  matter.mouseInteraction(window);

  rectMode(CENTER);
  textAlign(CENTER);

  // makeRectanglePegArray();
  makeTrianglePegArray();

  for (var i = 0; i < width; i += 50) {
    let block = matter.makeBarrier(i, height - 10, 5, 25);
    blockArr.push(block);
  }

  //testPeg = matter.makeBall(width/2, height/2, 5, { 
   // isStatic: true,
   //});
   //testPeg.freeze();

  // ball = matter.makeBall(width / 2, 40, 25);
  floor = matter.makeBarrier(width / 2, height, width, 10, { slop: 10 });
  leftWall = matter.makeBarrier(2.5, height/2, 5, height);
  rightWall = matter.makeBarrier(width-2.5, height/2, 5, height);
}

function draw() {
  // put the drawing code here
  background(0);

  stroke(150);
  strokeWeight(3);
  noFill();

  textSize(50); textFont("Ink Free");
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
  //testPeg.show();
  //ball.show();

  pegArr.forEach(function(peg) {
    peg.show();
  });

  ballArr.forEach(function(ball) {
    ball.show();
  });

  let colors = [[250, 0, 0],
                [200, 50, 0],
                [150, 100, 0],
                [100, 150, 0],
                [50, 200, 0],
                [0, 250, 0]
              ];
  
  for (var i = 0; i < 6; i++){
    fill(colors[5-i]);
    rect(width/2, height, width-100*i, 25);
  }
}

function mousePressed() {
  if (mouseY < 100) {
    var newBall = matter.makeBall(mouseX, mouseY, 30, { restitution: 0.505 });
    ballArr.push(newBall);
  }
}
