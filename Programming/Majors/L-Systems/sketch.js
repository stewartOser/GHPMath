let ini = 'FpFpFpF';
let rep = 'FnFpFpFFnFnFpF';

let angle = 0;
let r = 4;
let base = 400;

function setup() {
  createCanvas(windowWidth, windowHeight);
  angleMode(DEGREES);
  strokeWeight(1);
  stroke(0);

  noLoop();
}

function draw() {
  background(255);

  let startx = width / 2 - 400 / 2;
  let starty = height / 2 - 400 / 2;
  for (var i = 0; i < ini.length; i++) {
    switch (ini[i]) {
      case 'F':
        let endx = startx + cos(angle)*base;
        let endy = starty + sin(angle)*base;
        line(startx, starty, endx, endy);

        startx = endx;
        starty = endy;
        break;

      case 'a':
        angle -= 60;
        break;

      case 'z':
        angle += 60;
        break;

      case 'p':
        angle += 90;
        break;
      
      case 'n':
        angle -= 90;
        break;
      
      default:
        console.log('Unknown Symbol!');
    }
  }
  base = base / r;
}

function mousePressed() {
  let newIni = '';
  for (var i = 0; i < ini.length; i++) {
    if (ini[i] == 'F') {
      // fancy term CONCATENATION
      newIni += rep;
    } else {
      newIni += ini[i];
    }
  }

  ini = newIni;
  angle = 0;
  draw();
}
