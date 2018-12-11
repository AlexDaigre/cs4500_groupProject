

'''
#Authors: Alex Daigre, Jeff Butera, Flynn Keeler, Justin Henn, Paul Ries, Zachary Jorn
#Date: 12/10/2018
#Course Title: Intro to the Software Profession
#v1.0
#This program is compiled in Python 3.7
#Purpose: This program is a game for the robot Cozmo to fine a cube that the player sets on a custom made board.
#   The player creates a maxe on the game board using direction tiles, shice lead Cozmo to the cube.
#   Cozmo goes though that maze by reading the direction tiles, once he finds the cube, he perfroms an animation.
'''

import time
import cozmo
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
from cozmo.util import degrees, distance_mm, speed_mmps

#All motion objects.
right_turn = False
left_turn = False
forward = False
backward = False


# This will be called whenever an EvtObjectAppeared is dispatched whenever an Object comes into view.
def handle_object_appeared(evt, **kw):

    if isinstance(evt.obj, CustomObject):
        print("Cozmo started seeing a %s" % str(evt.obj.object_type))
        if evt.obj.object_type == CustomObjectTypes.CustomType02:
            global right_turn 
            right_turn = True
        if evt.obj.object_type == CustomObjectTypes.CustomType03:
            global left_turn 
            left_turn = True
        if evt.obj.object_type == CustomObjectTypes.CustomType04:
            global forward
            forward = True
        if evt.obj.object_type == CustomObjectTypes.CustomType05:
            global backward
            backward = True


#define a unique wall (150mm x 120mm (x10mm thick for all walls) with a 20mm x 20mm Circles2 image on front and back
def custom_objects(robot: cozmo.robot.Robot):
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)

    #More objects can be added by copying the below sections, and changing the "CustomType##" and "CustomObjectMarkers.SHAPE"
    #to whatever pre-recognized shape in the Cozmo directory.
    wall_obj = robot.world.define_custom_wall(CustomObjectTypes.CustomType02,
                                              CustomObjectMarkers.Circles2,
                                              140, 130, #65 by 65 originally
                                              20, 20, False)
    wall_obj1 = robot.world.define_custom_wall(CustomObjectTypes.CustomType03,
                                              CustomObjectMarkers.Diamonds2,
                                              140, 130,
                                              20, 20, False)
    wall_obj2 = robot.world.define_custom_wall(CustomObjectTypes.CustomType04,
                                              CustomObjectMarkers.Triangles2,
                                              140, 130,
                                              20, 20, False)
    wall_obj3 = robot.world.define_custom_wall(CustomObjectTypes.CustomType05,
                                              CustomObjectMarkers.Hexagons2,
                                              140, 130,
                                              20, 20, False)

    print("Show the above markers to Cozmo and you will see the related objects "
          "annotated in Cozmo's view window, you will also see print messages "
          "everytime a custom object enters or exits Cozmo's view.")
    print("Press CTRL-C to quit")

    # Move arms ("lift") up initially for the movement.
    robot.move_lift(100)

    while True:
        robot.set_head_angle(degrees(-16)).wait_for_completed()
        cubes = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=1)

        global right_turn
        global left_turn
        global forward
        global backward
        robot.set_head_angle(degrees(-25)).wait_for_completed()
        print(forward)
        
        #The robot.drive_straght(distance_mm(###) can be modified for different sized boards or for troubleshooting
        #measurements.
        #Keep in mind that the distance forward is different for driving forward and the turning.
        
        #DIAMOND/RIGHT TURN
        if right_turn:
            robot.drive_straight(distance_mm(135), speed_mmps(100)).wait_for_completed()
            robot.turn_in_place(degrees(90)).wait_for_completed()
            robot.set_head_angle(degrees(-25))
            time.sleep(0.5)

        #CIRCLE/LEFT TURN
        elif left_turn:
            robot.drive_straight(distance_mm(135), speed_mmps(100)).wait_for_completed()
            robot.turn_in_place(degrees(-90)).wait_for_completed()
            robot.set_head_angle(degrees(-25))
            time.sleep(0.5)

        #TRIANGLES/STRAIGHT
        elif forward:
            robot.drive_straight(distance_mm(130), speed_mmps(100)).wait_for_completed()
            robot.set_head_angle(degrees(-25))
            time.sleep(0.5)

        #ADDIONAL OBJECT ACTIONS ADD HERE:
        
        
        #################################
            
        #HEXAGON/STOP
        elif backward:
            break

        if len(cubes) == 0:
            print("Cube not found")
        else:
            print("Cube found")
            if right_turn is False and left_turn is False and forward is False and backward is False:
                print("Quitting")


                robot.move_lift(-100)
                time.sleep(0.5)

                robot.drive_straight(distance_mm(40), speed_mmps(50)).wait_for_completed()
                scales = ["", "", "", "", "", "", "", "Praise the Sun!"]

                # Find voice_pitch_delta value that will range the pitch from -1 to 1 over all of the scales
                voice_pitch = -1.0
                voice_pitch_delta = 2.0 / (len(scales) - 1)

                # Move head and lift down to the bottom, and wait until that's achieved
                robot.move_head(-5)  # start moving head down so it mostly happens in parallel with lift
                robot.set_lift_height(0.0).wait_for_completed()
                robot.set_head_angle(degrees(-25.0)).wait_for_completed()

                # Start slowly raising lift and head
                robot.move_lift(0.15)
                robot.move_head(0.15)

                robot.turn_in_place(degrees(-360)).wait_for_completed()

                # "Sing" each note of the scale at increasingly high pitch
                for note in scales:
                    robot.say_text(note, voice_pitch=voice_pitch, duration_scalar=10).wait_for_completed()
                    voice_pitch += voice_pitch_delta


                break

        right_turn = False
        left_turn = False
        forward = False
        backward = False
        time.sleep(0.5)


cozmo.run_program(custom_objects, use_viewer=True)
