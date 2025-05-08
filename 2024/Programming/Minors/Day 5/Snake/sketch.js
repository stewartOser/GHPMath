var snake = [];

function Body() {
  // objective, but ok
  this.d = 30;
  this.x = random(this.d/2, width-this.d/2);
  this.y = random(this.d/2, height-this.d/2);

  this.clr = [random(255), random(255), random(255)];

  // So methodical y'all
  this.draw = function() {
    fill(this.clr); // gotta be careful that this.clr is at most 4 numbers below 255
    circle(this.x, this.y, this.d);
  }
}

function setup() {
  createCanvas(800, 800);
  for (var i = 0; i < 50; i++) {
    // The code
    var b = new Body();
    // this function should be called plastic surgery
    snake.push(b);
  } // Wow that was simple
}

function draw() {
  background(220);

  for (var part = 0; part < snake.length; part++) {
    // i code so i can be lazy
    snake[part].draw();
    // freedom for mousekind
  }
}

function mouseDragged() {
  // why is 0 so special lol
  var factor = 0.25; // if you dare, increase this above 1
  snake[0].x = factor*(mouseX - snake[0].x) + snake[0].x;
  snake[0].y = factor*(mouseY - snake[0].y) + snake[0].y;
  // funny odd is the best kind of funny tho
  // unoriginal no cap
  for (var part = 1; part < snake.length; part++) {
    // 0 deserves better than us all
    snake[part].x = factor*(snake[part-1].x - snake[part].x) + snake[part].x;
    snake[part].y = factor*(snake[part-1].y - snake[part].y) + snake[part].y;
  }
}
