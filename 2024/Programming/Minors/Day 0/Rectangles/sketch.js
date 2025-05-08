function setup() {
  createCanvas(400, 400);
}

function draw() {
  background(0, 0, 0);
  strokeWeight(5); // visibility
  stroke(255);
  // or has it
  fill(0);

  for(var x = 100; x < 300; x += 50){
    rect(x, 100, 50, 50);
  }
  
}
