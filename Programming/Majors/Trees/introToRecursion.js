var x = 0;

function fib(num) {
  if (num == 1) {
    return 1
  } 

  // 1 will refer to the first num
  if (num == 2) {
    return 1
  }

  return fib(num - 2) + fib(num - 1);
}

function factorial(num) {
  if (num <= 1) {
    return 1
  }
  
  return num*factorial(num - 1);
}

function whatPurpose(runo) {
  x++;
  console.log("before ", runo, x);
  if (runo < 5) {
    whatPurpose(runo + 1);
  }
  console.log("after ", runo, x);
}

function setup() {
  createCanvas(600, 600);
  noLoop();
}

function draw() {
  background(220);
  // whatPurpose(0);
  console.log("Factorial of 1000 is", factorial(1000));
  console.log("The 100th fib num is\n", fib(100));
}
