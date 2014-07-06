/* --------------------------------------------------------------------------
 * Mouse Emulation using Depth Camera
 * --------------------------------------------------------------------------
 * Processing 2.2.1 , Simple OpenNI 1.96, FingerTracker library for Processin
 * --------------------------------------------------------------------------
 * Djemel Nebras , WebValley 2014
 * ----------------------------------------------------------------------------
 * This allows you to control the mouse by waving and to click or grab 
 * depending on the gesture. Not stable .
 * ----------------------------------------------------------------------------
 */
 
import java.util.Map;
import java.util.Iterator;
import java.awt.*;
import java.awt.Robot;
 import java.awt.event.InputEvent;
import fingertracker.*;

import SimpleOpenNI.*;


Robot robot; // Set the mouse 
FingerTracker fingers;
SimpleOpenNI kinect;


SimpleOpenNI context;
int xx , yy ;
int threshold = 580;
int timer;


int handVecListSize = 20;
Map<Integer,ArrayList<PVector>>  handPathList = new HashMap<Integer,ArrayList<PVector>>();
color[]       userClr = new color[]{ color(255,0,0),
                                     color(0,255,0),
                                     color(0,0,255),
                                     color(255,255,0),
                                     color(255,0,255),
                                     color(0,255,255)
                                   };
void setup()
{

 try { 
    robot = new Robot(); // mouse move settings
  } 
  catch (AWTException e) {
    e.printStackTrace();
  }
//  frameRate(200);
  size(640,480);

  context = new SimpleOpenNI(this);
  if(context.isInit() == false)
  {
     println("Can't init SimpleOpenNI, maybe the camera is not connected!"); 
     exit();
     return;  
  }   

  // enable depthMap generation 
  context.enableDepth();
  
  // disable mirror
  context.setMirror(true);
    fingers = new FingerTracker(this, 640, 480);
  fingers.setMeltFactor(70);

  // enable hands + gesture generation
  //context.enableGesture();
  context.enableHand();
  context.startGesture(SimpleOpenNI.GESTURE_WAVE);
  //context.endGesture(SimpleOpenNI.GESTURE_HAND_RAISE);
  
  // set how smooth the hand capturing should be
  //context.setSmoothingHands(.5);
 }

void draw()
{
  // update the cam
  context.update();

  image(context.depthImage(),0,0);
    fingers.setThreshold(threshold);
  int[] depthMap = context.depthMap();
  fingers.update(depthMap);  
  // draw the tracked hands
  if(handPathList.size() > 0)  
  {    
    Iterator itr = handPathList.entrySet().iterator();     
    while(itr.hasNext())
    {
      Map.Entry mapEntry = (Map.Entry)itr.next(); 
      int handId =  (Integer)mapEntry.getKey();
      ArrayList<PVector> vecList = (ArrayList<PVector>)mapEntry.getValue();
      PVector p;
      PVector p2d = new PVector();
      
        stroke(userClr[ (handId - 1) % userClr.length ]);
        noFill(); 
        strokeWeight(1);        
        Iterator itrVec = vecList.iterator(); 
        beginShape();
          while( itrVec.hasNext() ) 
          { 
            p = (PVector) itrVec.next(); 
            
            context.convertRealWorldToProjective(p,p2d);
            vertex(p2d.x,p2d.y);
          }
        endShape();   
  
        stroke(userClr[ (handId - 1) % userClr.length ]);
        strokeWeight(4);
        p = vecList.get(0);
        context.convertRealWorldToProjective(p,p2d);
        point(p2d.x,p2d.y);
        xx=(int)((p2d.x-50)*(displayWidth+300)/640);
        yy=(int)((p2d.y-50)*(displayHeight+300)/480);
        robot.mouseMove(xx,yy);        
    }
  }
  
  stroke(0,255,0);
  for (int k = 0; k < fingers.getNumContours(); k++) {
    fingers.drawContour(k);
  }
  
  if (fingers.getNumFingers()>4){    robot.mousePress( InputEvent.BUTTON1_MASK );
                                      robot.mouseRelease( InputEvent.BUTTON1_MASK );
                                      timer = millis();
                                      while (millis()- timer < 150){
                                        println("one click");
                                      }
                                    }
  else if (fingers.getNumContours()> 1){  robot.mousePress( InputEvent.BUTTON1_MASK ); }
  else if (fingers.getNumContours() < 2){   robot.mouseRelease( InputEvent.BUTTON1_MASK ); }

   noStroke();
  
  // show the threshold on the screen
  fill(255,0,0);
  text(threshold, 10, 20);
}


// -----------------------------------------------------------------
// hand events

void onNewHand(SimpleOpenNI curContext,int handId,PVector pos)
{
  println("onNewHand - handId: " + handId + ", pos: " + pos);
 
  ArrayList<PVector> vecList = new ArrayList<PVector>();
  vecList.add(pos);
  
  handPathList.put(handId,vecList);
}



void onTrackedHand(SimpleOpenNI curContext,int handId,PVector pos)
{
  //println("onTrackedHand - handId: " + handId + ", pos: " + pos );
  
  ArrayList<PVector> vecList = handPathList.get(handId);
  if(vecList != null)
  {
    vecList.add(0,pos);
    if(vecList.size() >= handVecListSize)
      // remove the last point 
      vecList.remove(vecList.size()-1); 
  }  
}

void onLostHand(SimpleOpenNI curContext,int handId)
{
  println("onLostHand - handId: " + handId);
  handPathList.remove(handId);
}

// -----------------------------------------------------------------
// gesture events

void onCompletedGesture(SimpleOpenNI curContext,int gestureType, PVector pos)
{
  println("onCompletedGesture - gestureType: " + gestureType + ", pos: " + pos);

  
  int handId = context.startTrackingHand(pos);
  println("hand stracked: " + handId);
}

// -----------------------------------------------------------------
// Keyboard event
void keyPressed()
{

  
  if(key == '-'){
    threshold -= 10;
  }
  
  if(key == '='){
    threshold += 10;
  
  }
}

 
