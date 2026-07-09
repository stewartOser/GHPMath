bg;

function setup() {
  bg = loadImage('mandlebrot.png');
  createCanvas(800, 800);
  background(bg);
  ellipseMode(RADIUS);

  noLoop();
}

function mouseDragged() {
  background(bg);
  fill(255, 0, 0);
  circle(mouseX, mouseY, 5);

  var cre = (mouseX - 400) / 200;
  var cim = (400 - mouseY) / 200;

  var zre = 0;
  var zim = 0;

  for (var i = 0; i < 15; i++) {
    var next = f(zre, zim, cre, cim);

    var scrX = 200 * next[0] + 400;
    var scrY = 400 - 200 * next[1];

    var prevX = 200 * zre + 400;
    var prevY = 400 - 200 * zim;

    fill(255);
    circle(scrX, scrY, 5);
    line(prevX, prevY, scrX, scrY);

    zre = next[0];
    zim = next[1];
  }
}

function f(zre, zim, cre, cim) {
  var nextRe = zre*zre - zim*zim + cre;
  var nextIm = 2*zre*zim + cim;

  return [nextRe, nextIm];
}
