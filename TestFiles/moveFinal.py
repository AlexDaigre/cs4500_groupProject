#!/usr/bin/env python3

# Copyright (c) 2017 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''

'''

import time
import cozmo
from cozmo.objects import CustomObject, CustomObjectMarkers, CustomObjectTypes
from cozmo.util import degrees, distance_mm, speed_mmps

found_wall = False
found_wall1 = False
found_wall2 = False
found_wall3 = False

def handle_object_appeared(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.

    if isinstance(evt.obj, CustomObject):
        print("Cozmo started seeing a %s" % str(evt.obj.object_type))
        if evt.obj.object_type == CustomObjectTypes.CustomType02:
            global found_wall 
            found_wall = True
        if evt.obj.object_type == CustomObjectTypes.CustomType03:
            global found_wall1 
            found_wall1 = True
        if evt.obj.object_type == CustomObjectTypes.CustomType04:
            global found_wall2
            found_wall2 = True
        if evt.obj.object_type == CustomObjectTypes.CustomType05:
            global found_wall3
            found_wall3 = True


def custom_objects(robot: cozmo.robot.Robot):
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)

    # define a unique wall (150mm x 120mm (x10mm thick for all walls)
    # with a 50mm x 30mm Circles2 image on front and back
    wall_obj = robot.world.define_custom_wall(CustomObjectTypes.CustomType02,
                                              CustomObjectMarkers.Circles2,
                                              140, 130, #65 by 65 original
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

    # Move lift down and tilt the head up
    robot.move_lift(100)
#    robot.set_head_angle(degrees(-25))#.wait_for_completed()
    while True:
        robot.set_head_angle(degrees(-16)).wait_for_completed()
        cubes = robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=1)

        global found_wall
        global found_wall1
        global found_wall2
        global found_wall3
        robot.set_head_angle(degrees(-25)).wait_for_completed()
        print(found_wall2)
        #DIAMOND/RIGHT TURN
        if found_wall == True:
            robot.drive_straight(distance_mm(130), speed_mmps(100)).wait_for_completed()
            robot.turn_in_place(degrees(90)).wait_for_completed()
            robot.set_head_angle(degrees(-25))#.wait_for_completed()
            time.sleep(0.5)

        #CIRCLE/LEFT TURN
        elif found_wall1 == True:
            robot.drive_straight(distance_mm(130), speed_mmps(100)).wait_for_completed()
            robot.turn_in_place(degrees(-90)).wait_for_completed()
            robot.set_head_angle(degrees(-25))#.wait_for_completed()
            time.sleep(0.5)

        #TRIANGLES/STRAIGHT
        elif found_wall2 == True:
            robot.drive_straight(distance_mm(130), speed_mmps(100)).wait_for_completed()
            robot.set_head_angle(degrees(-25))#.wait_for_completed()
            time.sleep(0.5)

        #HEXAGON/TURN AROUND
        elif found_wall3 == True:
            robot.turn_in_place(degrees(-180)).wait_for_completed()
            robot.set_head_angle(degrees(-25))#.wait_for_completed()
            time.sleep(0.5)

        #lookaround.stop()
        if len(cubes) == 0:
            print("Cube not found")
        else:
            print("Cube found")
            if found_wall is False and found_wall is False and found_wall2 is False and found_wall3 is False:
                print("Quitting")
                break

        found_wall = False
        found_wall1 = False
        found_wall2 = False
        found_wall3 = False
        time.sleep(0.5)


cozmo.run_program(custom_objects, use_viewer=True)