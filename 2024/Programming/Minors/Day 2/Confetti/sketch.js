let gif;
let global = false;

function preload(){
  gif = loadImage('confetti.gif');
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  gif.resize(width, height);
  rectMode(CENTER);
}

function draw() {
  background(0);

  rect(width/2, height/2, 100, 100);

  if (global) {
    image(gif, 0, 0);
  }
}

function mousePressed() {
  if (width/2-50<=mouseX && mouseX<=width/2+50 && height/2-50 <=mouseY && mouseY <= height/2+50) {
    global = true;
  } else {
    global = false;
  }
}
