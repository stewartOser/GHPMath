let x = 1;

function setup() {
  createCanvas(600, 600);
}

function draw() {
  background(255, 0, 255);

  // 10 rectangles (dim. 50)
  // start at 0, 50

  for(var x = 1; x < 5; x ++) {
    for (var y = 1; y < 5; y++) {
      rect(x*50, y*50, 50, 50);
    } 
  }

}