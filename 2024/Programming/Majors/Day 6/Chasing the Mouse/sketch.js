var snake = [];
let img;
var difficulty = 2;

function Segment() {
  this.x = random(width);
  this.y = random(height);
  if (snake.length == 0) {
    this.d = 30;
  } else if (snake.length == 1){
    this.d = 20;
  } else {
    var choose = floor(random(-1,2));
    this.d = snake[snake.length-1].d + choose*3;

    if (this.d < 15) {
      this.d = 0;
    };
  };
  this.clr = [random(100, 220), 
              random(100, 255), 
              random(60)];
  
  this.draw = function() {
    fill(this.clr[0], this.clr[1], 
                      this.clr[2]);
    circle(this.x, this.y, this.d);
  };

};

function preload() {
  img = loadImage('grass.png');
}

function moveSnake() {
  // make that a variable for easier changing
  var frac = difficulty*250/1000
  snake[0].x = snake[0].x + frac*(mouseX - snake[0].x);
  snake[0].y = snake[0].y + frac*(mouseY - snake[0].y);

  for (var i = 1; i < snake.length; i++) {
    snake[i].x = snake[i].x + frac*(snake[i-1].x - snake[i].x);
    snake[i].y = snake[i].y + frac*(snake[i-1].y - snake[i].y);
  };
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  rectMode(CENTER);
  angleMode(DEGREES);

  // Create the snake
  var startLength = 10;
  for (var i = 0; i < startLength; i++) {
    var segment = new Segment();
    snake.push(segment);
  };
};

function draw() {
  background(30, 200, 60);

  // make grass
  var gridSize = 10;
  for (var i = 10; i < width; i += gridSize) {
    for (var j = 10; j < height; j += gridSize) {
      if (i % 3 == 0 && j % 3 == 0) {
        fill(255);
        image(img, i, j);
      };
    };
  };
  
  // Build the snake
  for (var i = 0; i < snake.length; i++) { 
     // snake.length allows for adjustment of 
     // snake length without causing errors
    snake[i].draw();
  };

  if (mouseIsPressed) {
    moveSnake();
  };

  if (0 < abs(snake[0].x - mouseX) && abs(snake[0].x - mouseX) < 1/(difficulty*1000) && 0 < abs(snake[0].y - mouseY) && abs(snake[0].y - mouseY) < 1/(difficulty*1000)) {
    background(0);
    fill(255);
    textSize(32);
    text('YOU WERE EATEN', width/2-125, height/2);
    frameRate(0);
  };

  cursor('rat.cur')
};

function mouseDragged() {
  var randChance = floor(random(50));
  if (randChance == 14) {
    var newSegment = new Segment();
    snake.push(newSegment);
    snake[snake.length-1].x = snake[snake.length-2].x;
    snake[snake.length-1].y = snake[snake.length-2].y;
  };
};
