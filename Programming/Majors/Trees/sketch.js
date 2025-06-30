let slider;
let change;

function setup() {
    createCanvas(800, 800);
    angleMode(DEGREES);

    slider = createSlider(0, 180, 90, 5);
    slider.position(width/2 - slider.length / 2, 10);
    slider.size(180);

    noLoop();
}

function draw() {
    background(0);
    change = slider.value();

    stroke(255);
    strokeWeight(2);

    let base = 300;
    line(width/2, height, width/2, height-base);

    let level    = 0;
    let maxLevel = 7;
    let angle    = 90;
    branch(base, angle, level + 1, maxLevel, width/2, height-base);
}

function branch(base, angle, level, maxLevel, startx, starty) {
    if (level > maxLevel) {
        return;
    }

    let newBase = base / 2;
    angle       = angle - change;
    let endx = startx + cos(angle)*newBase;
    let endy = starty - sin(angle)*newBase;
    line(startx, starty, endx, endy)

    branch(newBase, angle, level + 1, maxLevel, endx, endy);
    
    angle = angle + change;
    endx = startx + cos(angle)*newBase;
    endy = starty - sin(angle)*newBase;
    line(startx, starty, endx, endy)

    branch(newBase, angle, level + 1, maxLevel, endx, endy);

    angle = angle + change;
    endx = startx + cos(angle)*newBase;
    endy = starty - sin(angle)*newBase;
    line(startx, starty, endx, endy)

    branch(newBase, angle, level + 1, maxLevel, endx, endy);

    console.log(level, angle);
}

function mouseClicked() {
    change = slider.value()
    draw();
}