// What do you call the Mandlebrot set when you
// grill it, wrap it in a bun, and eat it?

// Mandlebrotwurst

var iter = 500;
var pal = [];

let a1, a2, b1, b2;
let rmin = -2;
let imin = -2;
let rmax = 2;
let imax = 2;

function setPallette() {
  // thats called camelCase, remember
  pal.push([0, 0, 100]);
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
  createCanvas(800, 800);
  noLoop();

  setPallette();
}

function draw() {
  background(0);

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
