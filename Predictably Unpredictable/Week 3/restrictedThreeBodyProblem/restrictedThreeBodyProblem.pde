Planet[] planets = {};
Satellite sat;
final double G = 200;
final float dt = 0.02;
final float M = 150;
final float r = 150;

class Planet {
  float initAngle, angle, x, y, xVel, yVel, dist, diameter, gravity, mass;
  PVector pos, vel;
  Planet (float initAngle, float xVel, float yVel, float dist, float diameter) {
    this.angle = initAngle;
    this.dist = dist;
    this.x = width/2 + this.dist*cos(this.angle);
    this.y = height/2 + this.dist*sin(this.angle);
    
    this.xVel = xVel;
    this.yVel = yVel;
    
    this.pos = new PVector(this.x, this.y);
    
    this.diameter = diameter;
    
    mass = M;
    gravity = 100;
  }
  
  PVector gravityFrom(Planet b) {
     float planetMass = b.getMass();
     
     PVector vec = new PVector(b.getXPosition() - this.x, b.getYPosition() - this.y);
     PVector gravity = vec.copy().normalize();
     float magnitude = vec.copy().mag();
        
     double gravityMagnitude = G * (this.mass * planetMass) / (Math.pow(magnitude, 2));
     gravity.mult((float) gravityMagnitude);
     
     return gravity;
  }
  
  void drawPlanet() {
    // this.orbit();
    circle(this.x, this.y, this.diameter);
  }
  
  float getMass() {
     return mass; 
  }
  
  float getGravity() {
     return gravity; 
  }
  
  float getXPosition() {
     return this.x; 
  }
  
  float getYPosition() {
    return this.y; 
  }
  
  float getXVelocity() {
     return this.xVel; 
  }
  
  float getYVelocity() {
    return this.yVel; 
  }
  
  float getRadius() {
    return this.diameter / 2;
  }
  
  void setXPosition(float x) {
    this.x = x;
  }
  
  void setYPosition(float y) {
    this.y = y; 
  }
  
  void setXVelocity(float xVel) {
    this.xVel = xVel;
  }
  
  void setYVelocity(float yVel) {
    this.yVel = yVel; 
  }
}

class Satellite {
  Planet[] planets;
  float x, y, xVel, yVel, diameter, mass;
  float[] pathX, pathY;
  Satellite (Planet[] planets) {
    this.planets = planets;
  
    float spawnDist, spawnAngle;
    PVector netAccel = new PVector();
    boolean badSpawn;
    float minPlanetDist = planets[0].getRadius() + 40; // must be safely outside planet radius (50) + margin
  
    do {
      spawnDist = random(r+20, r+120);   // orbit OUTSIDE the planets' own orbit (r=200)
      spawnAngle = random(TWO_PI);
      float testX = width/2 + spawnDist * cos(spawnAngle);
      float testY = height/2 + spawnDist * sin(spawnAngle);
  
      badSpawn = false;
      netAccel.set(0, 0);
  
      for (Planet p : planets) {
        float dx = p.getXPosition() - testX;
        float dy = p.getYPosition() - testY;
        float d = sqrt(dx*dx + dy*dy);
  
        if (d < minPlanetDist) {
          badSpawn = true;
        }
  
        float aMag = (float)(G * p.getMass() / (d * d));
        netAccel.add(aMag * dx / d, aMag * dy / d);
      }
  
      this.x = testX;
      this.y = testY;
    } while (badSpawn);
  
    float accelMag = netAccel.mag();
    float pullAngle = atan2(netAccel.y, netAccel.x);
    float tangentAngle = pullAngle + HALF_PI;
  
    float vCirc = sqrt(accelMag * spawnDist);
    vCirc = constrain(vCirc, 2, 8);   // clamp to a sane range regardless of local field spikes
  
    float angleJitter = random(-0.15, 0.15);
    float speedFactor = random(0.8, 1.05);
  
    float speed = vCirc * speedFactor;
    this.xVel = speed * cos(tangentAngle + angleJitter);
    this.yVel = speed * sin(tangentAngle + angleJitter);
  
    this.mass = 0.0015;
    this.diameter = 10;
  
    this.pathX = new float[0];
    this.pathY = new float[0];
  }
  
  // Runs the same physics as updatePos() but on a throwaway copy of state,
  // without touching pathX/pathY or drawing anything.
  boolean survivesTrial(int steps) {
    float tx = this.x, ty = this.y, txVel = this.xVel, tyVel = this.yVel;
    
    // Also need a copy of planet positions/velocities so the trial doesn't
    // permanently advance the real simulation.
    float[] px = new float[planets.length];
    float[] py = new float[planets.length];
    float[] pxVel = new float[planets.length];
    float[] pyVel = new float[planets.length];
    for (int i = 0; i < planets.length; i++) {
      px[i] = planets[i].getXPosition();
      py[i] = planets[i].getYPosition();
      pxVel[i] = planets[i].getXVelocity();
      pyVel[i] = planets[i].getYVelocity();
    }
    
    for (int step = 0; step < steps; step++) {
      // advance fake planets (mirrors updatePlanets logic)
      PVector[] accel = new PVector[planets.length];
      for (int i = 0; i < planets.length; i++) {
        PVector total = new PVector();
        for (int j = 0; j < planets.length; j++) {
          if (i == j) continue;
          float dx = px[j] - px[i];
          float dy = py[j] - py[i];
          float d = sqrt(dx*dx + dy*dy);
          float aMag = (float)(G * planets[j].getMass() / (d*d));
          total.add(aMag * dx / d, aMag * dy / d);
        }
        accel[i] = total;
      }
      for (int i = 0; i < planets.length; i++) {
        pxVel[i] += accel[i].x * dt;
        pyVel[i] += accel[i].y * dt;
        px[i] += pxVel[i] * dt;
        py[i] += pyVel[i] * dt;
      }
      
      // advance fake satellite
      PVector totalForce = new PVector();
      for (int i = 0; i < planets.length; i++) {
        float dx = px[i] - tx;
        float dy = py[i] - ty;
        float d = sqrt(dx*dx + dy*dy);
        
        if (d < planets[i].getRadius()) return false; // collision
        
        float fMag = (float)(G * (this.mass * planets[i].getMass()) / (d*d));
        totalForce.add(fMag * dx / d, fMag * dy / d);
      }
      
      float ax = totalForce.x / mass;
      float ay = totalForce.y / mass;
      txVel += ax * dt;
      tyVel += ay * dt;
      tx += txVel * dt;
      ty += tyVel * dt;
      
      if (tx < 0 || tx > width || ty < 0 || ty > height) return false; // flew off
    }
    
    return true; // survived the whole trial
  }
  
  void drawSatellite() {
    circle(this.x, this.y, this.diameter);
  }
  
  PVector[] getDistanceToPlanets() {
    PVector[] dists = new PVector[0];
    for (Planet planet : this.planets) {
      float planetXPosition = planet.getXPosition();
      float planetYPosition = planet.getYPosition();
     
      PVector distanceToPlanet = new PVector(planetXPosition - this.x, planetYPosition - this.y);
      dists = (PVector[]) append(dists, distanceToPlanet);
   }
   
   return dists;
  }
  
  PVector[] getForcesFromPlanets() {
    PVector[] dists = this.getDistanceToPlanets();
    PVector[] forces = new PVector[0];
    for (int i = 0; i < this.planets.length; i++) {
        float planetMass = this.planets[i].getMass();
        PVector gravity = dists[i].copy().normalize();
        float magnitude = dists[i].copy().mag();
        
        double gravityMagnitude = G * (this.mass * planetMass) / (Math.pow(magnitude, 2));
        gravity.mult((float) gravityMagnitude);
        
        forces = (PVector[]) append(forces, gravity);
    }
    return forces;
  }
  
  boolean checkCollision() {
    boolean collided = false;
    for (Planet planet : this.planets) {
      float planetXPosition = planet.getXPosition();
      float planetYPosition = planet.getYPosition();
      
      if (dist(planetXPosition, planetYPosition, this.x, this.y) < planet.getRadius()) {
        collided = true; 
      }
      
      if (this.x < 0 || this.x > width || this.y < 0 || this.y > height) {
        collided = true; 
      }
    }
    
   return collided; 
  }
  
  void updatePos() {
    boolean collided = checkCollision();
    if (collided) {
     System.out.println("I crashed or flew off!"); 
     noLoop();
    }
    
    float ax, ay;
    PVector totalForce = new PVector();
    PVector[] forces = this.getForcesFromPlanets();
    for (PVector force : forces) {
      totalForce.add(force);
    }
    
    ax = totalForce.x / mass;
    ay = totalForce.y / mass;
    
    this.xVel += ax * dt;
    this.yVel += ay * dt;
      
    this.x += this.xVel * dt;
    this.y += this.yVel * dt;
    
    this.pathX = append(this.pathX, this.x);
    this.pathY = append(this.pathY, this.y);
    
    if (pathX.length > 5000) {
      pathX = subset(pathX, 1, pathX.length - 1);
      pathY = subset(pathY, 1, pathY.length - 1);
    }
  }
  
  void drawPath() {
    for (int i = 1; i < pathX.length; i++) {
      line(pathX[i-1], pathY[i-1], pathX[i], pathY[i]);
    }
  }
}

void updatePlanets() {
    
    PVector gravityPlanet1 = planets[0].gravityFrom(planets[1]);
    PVector gravityPlanet0 = planets[1].gravityFrom(planets[0]);
    PVector[] gravityPlanets = {gravityPlanet1, gravityPlanet0};
    
    for (int i = 0; i < planets.length; i++) {
      float ax = gravityPlanets[i].x / planets[i].getMass();
      float ay = gravityPlanets[i].y / planets[i].getMass();
      
      float newXVel = planets[i].getXVelocity() + ax*dt;
      float newYVel = planets[i].getYVelocity() + ay*dt;
      planets[i].setXVelocity(newXVel);
      planets[i].setYVelocity(newYVel);
      
      planets[i].x += planets[i].xVel * dt;
      planets[i].y += planets[i].yVel * dt;
    }
}

void setup() {
  size(800, 800);
  
  Planet planetA = new Planet(0, 0, 7.15, r, 50);
  Planet planetB = new Planet(PI, 0, -7.15, r, 50);
  planets = (Planet[]) append(planets, planetA);
  planets = (Planet[]) append(planets, planetB);
  
  int trialSteps = 25 * 200; // simulate ~200 "frames" worth ahead (~4 sim-seconds)
  int maxAttempts = 500;
  
  for (int attempt = 0; attempt < maxAttempts; attempt++) {
    sat = new Satellite(planets);
    if (sat.survivesTrial(trialSteps)) {
      println("Found a keeper after " + (attempt + 1) + " attempt(s)");
      break;
    }
  }
}

void draw() {
  background(220);
  sat.drawSatellite();
  sat.drawPath();
  for (int i = 0; i < 25; i++) {
    updatePlanets();
    sat.updatePos();
  }
  
  for (Planet planet : planets) {
    planet.drawPlanet(); 
  }
}
