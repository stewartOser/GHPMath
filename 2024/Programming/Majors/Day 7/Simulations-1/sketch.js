function dice() {
  // var outcome = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
  var count = 0;
  for (var i = 0; i < 100000; i++) {
    // var roll = floor(random(6)) + floor(random(6));
    // outcome[roll] += 1;

    var red = floor(random(6));
    var green = floor(random(6));
    if (red > green) {
      count++;
    };
  };

  console.log(count/100000);
  console.log(15/36);
};

function shuffle(deck) {
  for (var i = 0; i < 50000; i++) {
    var a = floor(random(52));
    var b = floor(random(52));

    deck[a], deck[b] = deck[b], deck[a]; // multiprocessing
  };

  return deck;
};

function cards(){
  var deck = [];
  for (var suit = 1; suit <= 4; suit++) {
    for (var card = 1; card <= 13; card++) {
      deck.push(card);
    };
  };
  var total = 0;
  for (var trial = 0; trial < 100000; trial++) {
    shuffledDeck = shuffle(deck);
    // console.log(shuffledDeck);

    var p = 0;
    while (shuffledDeck[p] != 1) {
      p++;
    };
    total += p + 1;
  };
  var avg = total / 100000;

  console.log(avg);
};

function setup() {
  createCanvas(800, 800);
  noLoop();
};

function draw() {
  background(220);

  //dice();
  cards();
};
