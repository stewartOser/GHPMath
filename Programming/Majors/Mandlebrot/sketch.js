// What do you call the Mandlebrot set when you
// grill it, wrap it in a bun, and eat it?

// Mandlebrotwurst
let slider;

var iter = 500;
var pal = [];

let a1, a2, b1, b2;
let rmin = -2;
let imin = -2;
let rmax = 2;
let imax = 2;

function setPallette() {
  // thats called camelCase, remember
  pal.push([0, 0, 0]);
  for (var i = 1; i < 20; i++) {
    var a = [20*i + 4*i, 20*i, 100+40*i];
    pal.push(a);
  }
}


function iterate(real, imag) {
  let n = 0;

  let zre = 0;
  let zim = 0;
  while (n < iter && zre*zre + zim*zim < 4) {
    n++;
    let tre = zre*zre - zim*zim + real;
    let tim = 2*zre*zim + imag;
    
    zre = tre;
    zim = tim;
  }

  return n;
}

function setup() {
  slider = createSlider(500, 1000, 500, 10);
  slider.position(width/2 - slider.length / 2, 10);
  createCanvas(800, 800);
  noLoop();

  setPallette();
}

function draw() {
  background(0);

  slider.input(function() {
    iter = slider.value();
    draw(); // Redraw the Mandelbrot set
  });

  // console.log(slider.value(), iter);

  var tw = rmax - rmin;
  var th = imax - imin;
  for (var row = 0; row < height; row++) {
    for (var col = 0; col < width; col++) {
      cre = rmin + (tw/800)*(col);
      cim = imax - (th/800)*(row);

      n = iterate(cre,cim);
      if(n == iter){
        stroke(0);
      } else {
        stroke(pal[n % 20]);
      }

      point(col, row);
    }
  }
}

function mousePressed() {
  if (mouseY > 0) {
    a1 = rmin + (mouseX/800)*(rmax-rmin);
    a2 = imax - (mouseY/800)*(imax-imin);
  }
}

function mouseReleased() {
  if (mouseY > 0) {
    b1 = rmin + (mouseX/800)*(rmax-rmin);
    b2 = imax - (mouseY/800)*(imax-imin);

    if (a1 > b1) {
      let t = b1;
      b1 = a1;
      a1 = t;
    }

    if (a2 > b2) {
      let t = a2;
      a2 = b2;
      b2 = t;
    }

    b2 = b1 + (a2-a1);
    rmin = a1;
    rmax = b1;
    imin = a2;
    imax = b2;

    draw();
  }
}
