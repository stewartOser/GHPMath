// A function groups code together that
// then runs together when it's called!
// setup() runs ONCE at the start

function setup() {
  createCanvas(windowWidth, windowHeight); 
  //Leave this 600, 600
  angleMode(DEGREES);
}
/*
This is a comment
*/

function draw() {
  background(200, 200, 200);
  // This will ERASE the contents of the screen

  // translate(width/2, height/2);
  rotate(0);

  var rectSize = 20;
  for (var row = 20; row < 500; row += rectSize) { // 4 times
    for (var col = 20; col < 500; col += rectSize) { 
      rect(row, col, rectSize, rectSize);
    }
  }
}