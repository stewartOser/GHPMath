var x = 100;
var l = 0;

// Functions are selfish
function setup() {
  createCanvas(600, 400);
}

function draw() {
  background(240);
  fill(255, 0, 0);
  rect(x, 100, 100, 100);
   x += 10; // Bye!
  if(x > width){
    x = 0; // I'm back!
  }

  

  // I'm a comment!
}
