// What do you call the Mandlebrot set when you 
// grill it, wrap it in a bun, and eat it?

//Mandlebrotworst.

var iter = 100;
var pal = [];

let a1, a2, b1, b2;
let rmin = -2;
let imin = -2;
let rmax = 2;
let imax = 2;

function setPallete() {
  // that's called camelCase
  pal.push([0, 0, 100]);
  for (var i = 1; i < 20; i++) {
    var a = [10*i + 2*i, 10*i, 100+20*i];
    pal.push(a);
  }
}

function iterate(real, imag) {
  var n = 0;

  zre = 0;
  zim = 0;
  while (n < iter && zre*zre + zim*zim < 4) {
    n++;
    var tre = zre*zre - zim*zim + real;
    var tim = 2*zre*zim + imag;
    // i m a g too
    zre = tre;
    zim = tim;
  }

  return n;
}

function setup() {
  createCanvas(800, 800);
  noLoop();

  setPallete();
}

function draw() {
  background(220);

  for (var row = 0; row < width; row++) {
    for (var col = 0; col < height; col++) {
      var cre = rmin + (col / width) * (rmax - rmin);
      var cim = imax - (row / height) * (imax - imin);

      var n = iterate(cre, cim);
      if (n == iter) {
        stroke(0);
      } else{
        a = pal[n%20];
        stroke(a);
        // Did y'all say red because it's ketchup
        // on the Mandlebrotworst?
      }
      point(col, row);
    }
  }
}

function mousePressed() {
  a1 = rmin + (mouseX / width) * (rmax - rmin);
  b1 = imax - (mouseY / height) * (imax - imin);
}

function mouseReleased() {
  a2 = rmin + (mouseX / width) * (rmax - rmin);
  b2 = imax - (mouseY / height) * (imax - imin);

  if (a1 > a2) {
    var t = a1;
    a1 = a2;
    a2 = t;
  }

  if (b2 > b1) {
    var t = b1;
    b1 = b2;
    b2 = t;
  }

  b2 = b1 - a2 + a1;

  rmin = a1;
  rmax = a2;
  imax = b1;
  imin = b2;

  draw();
}

function mouseWheel() {
  rmin = -2;
  rmax = 2;
  imin = -2;
  imax = 2;

  draw();
}
