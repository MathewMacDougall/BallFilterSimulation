"""
This program reads Thunderbots game logfiles and simulates
the behaviours of different ball filters. The logfiles must be exported to .tsv files
from the last option in the tsv writer (writes ball and player positions)

Requires python3, matplotlib, numpy, python3-tk
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from BallData import BallData
from Ball import Ball
from Point import Point
from Robot import Robot
from ParticleFilter import ParticleFilter
from MFilter import MFilter
from MathewParticleFilter import MathewParticleFilter

# Constants for the field/simulation
FIELD_LENGTH = 9
FIELD_WIDTH = 6
CENTER_CIRCLE_RADIUS = 0.5
GOAL_WIDTH = 1
GOAL_DEPTH = 0.2

# Constants for the logfile data
LABEL_COLUMN = 0
TIMESTAMP_COLUMN = 1
XPOS_COLUMN = 2
YPOS_COLUMN = 3
CONFIDENCE_COLUMN = 4
XVEL_COLUMN = 5
YVEL_COLUMN = 6
FRIENDLY1X_COLUMN = 7
FRIENDLY1Y_COLUMN = 8
FRIENDLY1VX_COLUMN = 9
FRIENDLY1VY_COLUMN = 10
FRIENDLY2X_COLUMN = 11
FRIENDLY2Y_COLUMN = 12
FRIENDLY2VX_COLUMN = 13
FRIENDLY2VY_COLUMN = 14
FRIENDLY3X_COLUMN = 15
FRIENDLY3Y_COLUMN = 16
FRIENDLY3VX_COLUMN = 17
FRIENDLY3VY_COLUMN = 18
FRIENDLY4X_COLUMN = 19
FRIENDLY4Y_COLUMN = 20
FRIENDLY4VX_COLUMN = 21
FRIENDLY4VY_COLUMN = 22
FRIENDLY5X_COLUMN = 23
FRIENDLY5Y_COLUMN = 24
FRIENDLY5VX_COLUMN = 25
FRIENDLY5VY_COLUMN = 26
FRIENDLY6X_COLUMN = 27
FRIENDLY6Y_COLUMN = 28
FRIENDLY6VX_COLUMN = 29
FRIENDLY6VY_COLUMN = 30
ENEMY1X_COLUMN = 31
ENEMY1Y_COLUMN = 32
ENEMY1VX_COLUMN = 33
ENEMY1VY_COLUMN = 34
ENEMY2X_COLUMN = 35
ENEMY2Y_COLUMN = 36
ENEMY2VX_COLUMN = 37
ENEMY2VY_COLUMN = 38
ENEMY3X_COLUMN = 39
ENEMY3Y_COLUMN = 40
ENEMY3VX_COLUMN = 41
ENEMY3VY_COLUMN = 42
ENEMY4X_COLUMN = 43
ENEMY4Y_COLUMN = 44
ENEMY4VX_COLUMN = 45
ENEMY4VY_COLUMN = 46
ENEMY5X_COLUMN = 47
ENEMY5Y_COLUMN = 48
ENEMY5VX_COLUMN = 49
ENEMY5VY_COLUMN = 50
ENEMY6X_COLUMN = 51
ENEMY6Y_COLUMN = 52
ENEMY6VX_COLUMN = 53
ENEMY6VY_COLUMN = 54

path_to_logfiles = "logfiles/"

# The generated videos will be save with the same name as the logfile
# LOGFILE = "straight_line_no_bots.tsv"
LOGFILE = "bounce_no_bots.tsv"
# LOGFILE = "curve_no_bots.tsv"
# LOGFILE = "germany_GAME_2.tsv"
# LOGFILE = "germany_GAME_1.tsv"
# LOGFILE = "germany_GAME_3.tsv"
# LOGFILE = "germany_small_chip_test_19.tsv"
# LOGFILE = "germany_small_chip_test_19.tsv"
# LOGFILE = "bounce_no_bots_3_particle.tsv"
# LOGFILE = "bounce_no_bots_particle.tsv"
# LOGFILE = "bounce_no_bots_noisy_particle.tsv"
# LOGFILE = "sitting_still_noisy_particle.tsv"
# LOGFILE = "sitting_still_particle.tsv"

FPS = 25

# Choose what filter(s) to display
USE_PARTICLE_FILTER = False
USE_MATHEW_CUSTOM_FILTER = False
USE_MATHEW_PARTICLE_FILTER = True
TRUNCATE_INITIAL_DATA = False

# The ball objects that are updated and plotted
old_filter_ball = Ball(0, 0)
particle_ball = Ball(0, 0)
mathew_custom_ball = Ball(0, 0)
mathew_particle_ball = Ball(0, 0)

pFilter = ParticleFilter(FIELD_LENGTH, FIELD_WIDTH)
mathewCustomFilter = MFilter(FIELD_LENGTH, FIELD_WIDTH)
mathewParticleFilter = MathewParticleFilter(FIELD_LENGTH, FIELD_WIDTH)

# The simulator
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# variables to hold computed/read data from logfile
all_balls = []  # the list of balls detected from vision (each tick)
all_balls_data = []
old_filter_ball_data = []
particle_ball_data = []
mathew_custom_ball_data = []
mathew_particle_ball_data = []
friendly_1_data = []
friendly_2_data = []
friendly_3_data = []
friendly_4_data = []
friendly_5_data = []
friendly_6_data = []
enemy_1_data = []
enemy_2_data = []
enemy_3_data = []
enemy_4_data = []
enemy_5_data = []
enemy_6_data = []

first_tick = False

with open(path_to_logfiles + LOGFILE, 'r') as tsv:
    logfile = csv.reader(tsv, delimiter='\t')

    for row in logfile:
        if row[LABEL_COLUMN] == 'Vision':
            balldata = BallData(float(row[XPOS_COLUMN]), float(row[YPOS_COLUMN]), float(row[CONFIDENCE_COLUMN]))
            all_balls.append(balldata)

            pFilter.add(balldata.position())  # accepts Points
            mathewCustomFilter.add(balldata)  # accepts ballData
            mathewParticleFilter.add(balldata)  # accepts ballData
        elif row[LABEL_COLUMN] == 'Tick':
            if TRUNCATE_INITIAL_DATA is True and first_tick is False:
                del all_balls[:-1]  # remove all but the last elements
                first_tick = True
                print(all_balls)

            time_rec = float(row[TIMESTAMP_COLUMN])
            best_time = time_rec
            time_delta = time_rec - mathew_particle_ball.lock_time

            # Old filter ball
            old_filter_ball = Ball(float(row[XPOS_COLUMN]), float(row[YPOS_COLUMN]), float(row[XVEL_COLUMN]),
                                   float(row[YVEL_COLUMN]),
                                   float(row[TIMESTAMP_COLUMN]))
            old_filter_ball_data.append(old_filter_ball.copy())

            if USE_PARTICLE_FILTER:
                if len(all_balls) > 0:
                    particle_ball.update_position(pFilter.getEstimate(), best_time)
                pFilter.update(time_delta)
                particle_ball_data.append(particle_ball.copy())

            if USE_MATHEW_CUSTOM_FILTER:
                mathew_custom_ball.update_position(mathewCustomFilter.getEstimatedBall(), best_time)
                mathewCustomFilter.update(time_delta)
                mathew_custom_ball_data.append(mathew_custom_ball.copy())

            if USE_MATHEW_PARTICLE_FILTER:
                mathewParticleFilter.update(time_delta, mathew_particle_ball) # passing the ball as a param to pretend the filter has access to it like in the real ai
                mathew_particle_ball.update_position(mathewParticleFilter.getEstimate(), best_time)
                mathew_particle_ball_data.append(mathew_particle_ball.copy())

            # save the values to plot later
            all_balls_data.append(all_balls.copy())

            # reset variables for the next set of vision data
            all_balls.clear()

            # Robot things
            if row[FRIENDLY1X_COLUMN] is 'X':
                friendly_1_data.append(Robot())
            else:
                friendly_1_data.append(Robot(row[FRIENDLY1X_COLUMN], row[FRIENDLY1Y_COLUMN], row[FRIENDLY1VX_COLUMN],
                                             row[FRIENDLY1VY_COLUMN]))
            if row[FRIENDLY2X_COLUMN] is 'X':
                friendly_2_data.append(Robot())
            else:
                friendly_2_data.append(Robot(row[FRIENDLY2X_COLUMN], row[FRIENDLY2Y_COLUMN], row[FRIENDLY2VX_COLUMN],
                                             row[FRIENDLY2VY_COLUMN]))
            if row[FRIENDLY3X_COLUMN] is 'X':
                friendly_3_data.append(Robot())
            else:
                friendly_3_data.append(Robot(row[FRIENDLY3X_COLUMN], row[FRIENDLY3Y_COLUMN], row[FRIENDLY3VX_COLUMN],
                                             row[FRIENDLY3VY_COLUMN]))
            if row[FRIENDLY4X_COLUMN] is 'X':
                friendly_4_data.append(Robot())
            else:
                friendly_4_data.append(Robot(row[FRIENDLY4X_COLUMN], row[FRIENDLY4Y_COLUMN], row[FRIENDLY4VX_COLUMN],
                                             row[FRIENDLY4VY_COLUMN]))
            if row[FRIENDLY5X_COLUMN] is 'X':
                friendly_5_data.append(Robot())
            else:
                friendly_5_data.append(Robot(row[FRIENDLY5X_COLUMN], row[FRIENDLY5Y_COLUMN], row[FRIENDLY5VX_COLUMN],
                                             row[FRIENDLY5VY_COLUMN]))
            if row[FRIENDLY6X_COLUMN] is 'X':
                friendly_6_data.append(Robot())
            else:
                friendly_6_data.append(Robot(row[FRIENDLY6X_COLUMN], row[FRIENDLY6Y_COLUMN], row[FRIENDLY6VX_COLUMN],
                                             row[FRIENDLY6VY_COLUMN]))
            if row[ENEMY1X_COLUMN] is 'X':
                enemy_1_data.append(Robot())
            else:
                enemy_1_data.append(Robot(row[ENEMY1X_COLUMN], row[ENEMY1Y_COLUMN], row[ENEMY1VX_COLUMN],
                                          row[ENEMY1VY_COLUMN]))
            if row[ENEMY2X_COLUMN] is 'X':
                enemy_2_data.append(Robot())
            else:
                enemy_2_data.append(Robot(row[ENEMY2X_COLUMN], row[ENEMY2Y_COLUMN], row[ENEMY2VX_COLUMN],
                                          row[ENEMY2VY_COLUMN]))
            if row[ENEMY3X_COLUMN] is 'X':
                enemy_3_data.append(Robot())
            else:
                enemy_3_data.append(Robot(row[ENEMY3X_COLUMN], row[ENEMY3Y_COLUMN], row[ENEMY3VX_COLUMN],
                                          row[ENEMY3VY_COLUMN]))
            if row[ENEMY4X_COLUMN] is 'X':
                enemy_4_data.append(Robot())
            else:
                enemy_4_data.append(Robot(row[ENEMY4X_COLUMN], row[ENEMY4Y_COLUMN], row[ENEMY4VX_COLUMN],
                                          row[ENEMY4VY_COLUMN]))
            if row[ENEMY5X_COLUMN] is 'X':
                enemy_5_data.append(Robot())
            else:
                enemy_5_data.append(Robot(row[ENEMY5X_COLUMN], row[ENEMY5Y_COLUMN], row[ENEMY5VX_COLUMN],
                                          row[ENEMY5VY_COLUMN]))
            if row[ENEMY6X_COLUMN] is 'X':
                enemy_6_data.append(Robot())
            else:
                enemy_6_data.append(Robot(row[ENEMY6X_COLUMN], row[ENEMY6Y_COLUMN], row[ENEMY6VX_COLUMN],
                                          row[ENEMY6VY_COLUMN]))

        else:
            # We don't care about this line. It might be a debug message or something.
            print("Ignoring this line")

# The animation and plotting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def custom_div_cmap(numcolors=100, name='custom_cmap', mincol='blue', maxcol='orange'):
    """ Create a custom colormap with three colors

    Default is blue to white to red with 11 colors.  Colors can be specified
    in any way understandable by matplotlib.colors.ColorConverter.to_rgb()
    """

    from matplotlib.colors import LinearSegmentedColormap

    cmap = LinearSegmentedColormap.from_list(name=name,
                                             colors=[mincol, maxcol],
                                             N=numcolors)
    return cmap

fig, ax = plt.subplots()
ax.grid()

# Plot the field
field1 = plt.Rectangle((-FIELD_LENGTH / 2, -FIELD_WIDTH / 2), FIELD_LENGTH, FIELD_WIDTH, lw=2, fill=False, ec='black')
field2 = plt.Rectangle((-FIELD_LENGTH / 2 - GOAL_DEPTH, -GOAL_WIDTH / 2), GOAL_DEPTH, GOAL_WIDTH, lw=2, fill=False,
                       ec='black')
field3 = plt.Rectangle((FIELD_LENGTH / 2, -GOAL_WIDTH / 2), GOAL_DEPTH, GOAL_WIDTH, lw=2, fill=False, ec='black')
field4 = plt.Rectangle((0, -FIELD_WIDTH / 2), 0, FIELD_WIDTH, lw=2, fill=False, ec='black')
field5 = plt.Circle((0, 0), radius=CENTER_CIRCLE_RADIUS, lw=2, fill=False, ec='black')

ball_cmap = custom_div_cmap()
all_balls_scatter = plt.scatter([], [], marker='d', cmap=ball_cmap, c=[], s=25, vmin=0.0, vmax=1.0)
old_filter_plot, = plt.plot([], [], 'ko', ms=2, alpha=0.6)
old_filter_velocity, = plt.plot([], [], 'k-', lw=0.4, alpha=0.6)
particle_ball_plot, = plt.plot([], [], 'yo', ms=3)
particle_ball_velocity, = plt.plot([], [], 'y-', lw=0.5)
mathew_custom_plot, = plt.plot([], [], 'co', ms=3)
mathew_custom_velocity, = plt.plot([], [], 'c-', lw=0.5)
mathew_particle_plot, = plt.plot([], [], 'mo', ms=3)
mathew_particle_velocity, = plt.plot([], [], 'm-', lw=0.5)

basepoints_scatter = plt.scatter([], [], marker='x', cmap='winter', s=15, c=[], vmin=0.0, vmax=1.0)

# Friendly players
friendly_1 = plt.Circle((-99, -99), radius=0.09, color="green")
friendly_2 = plt.Circle((-99, -99), radius=0.09, color="green")
friendly_3 = plt.Circle((-99, -99), radius=0.09, color="green")
friendly_4 = plt.Circle((-99, -99), radius=0.09, color="green")
friendly_5 = plt.Circle((-99, -99), radius=0.09, color="green")
friendly_6 = plt.Circle((-99, -99), radius=0.09, color="green")

# enemy players
enemy_1 = plt.Circle((-99, -99), radius=0.09, color="red")
enemy_2 = plt.Circle((-99, -99), radius=0.09, color="red")
enemy_3 = plt.Circle((-99, -99), radius=0.09, color="red")
enemy_4 = plt.Circle((-99, -99), radius=0.09, color="red")
enemy_5 = plt.Circle((-99, -99), radius=0.09, color="red")
enemy_6 = plt.Circle((-99, -99), radius=0.09, color="red")


# Initializes the variables for the animation
def init():
    ax.add_patch(field1)
    ax.add_patch(field2)
    ax.add_patch(field3)
    ax.add_patch(field4)
    ax.add_patch(field5)
    ax.set_ylim(-FIELD_WIDTH / 2 - 0.5, FIELD_WIDTH / 2 + 0.5)
    ax.set_xlim(-FIELD_LENGTH / 2 - 0.5, FIELD_LENGTH / 2 + 0.5)
    # ax.set_aspect(FIELD_WIDTH / FIELD_LENGTH)

    # all_balls_plot.set_data([], [])
    all_balls_scatter.set_offsets([])
    basepoints_scatter.set_offsets([])
    old_filter_plot.set_data([], [])
    old_filter_velocity.set_data([], [])
    particle_ball_plot.set_data([], [])
    particle_ball_velocity.set_data([], [])
    mathew_custom_plot.set_data([], [])
    mathew_custom_velocity.set_data([], [])
    mathew_particle_plot.set_data([], [])
    mathew_particle_velocity.set_data([], [])

    ax.add_patch(friendly_1)
    ax.add_patch(friendly_2)
    ax.add_patch(friendly_3)
    ax.add_patch(friendly_4)
    ax.add_patch(friendly_5)
    ax.add_patch(friendly_6)

    ax.add_patch(enemy_1)
    ax.add_patch(enemy_2)
    ax.add_patch(enemy_3)
    ax.add_patch(enemy_4)
    ax.add_patch(enemy_5)
    ax.add_patch(enemy_6)

    return field1, field2, field3, field4, field5, all_balls_scatter, \
           old_filter_plot, old_filter_velocity, \
           particle_ball_plot, particle_ball_velocity, \
           mathew_custom_plot, mathew_custom_velocity, \
           mathew_particle_plot, mathew_particle_velocity,\
            basepoints_scatter,

basepoints_data = mathewParticleFilter.get_basepoints()

def run(i):
    # update all_balls position in scatter plot
    temp_all_ball_scatter_data = []
    for c in all_balls_data[i]:
        temp_all_ball_scatter_data.append((c.position().x, c.position().y))
    all_balls_scatter.set_offsets(temp_all_ball_scatter_data)

    temp_basepoints_scatter_data = []
    if i < len(basepoints_data):
        print("drawing basepoints {}".format(basepoints_data[i]))
        for w in basepoints_data[i]:
            temp_basepoints_scatter_data.append((w.x, w.y))
        basepoints_scatter.set_offsets(temp_basepoints_scatter_data)
        basepoints_scatter.set_array(np.array([1.0 for r in basepoints_data[i]]))

    # color the vision balls based on their confidence values
    all_balls_scatter.set_array(np.array([c.confidence for c in all_balls_data[i]]))

    # plot the old filter ball data
    old_filter_plot.set_data([old_filter_ball_data[i].position().x], [old_filter_ball_data[i].position().y])
    old_filter_velocity.set_data(
        [old_filter_ball_data[i].position().x,
         old_filter_ball_data[i].position().x + old_filter_ball_data[i].velocity().x],
        [old_filter_ball_data[i].position().y,
         old_filter_ball_data[i].position().y + old_filter_ball_data[i].velocity().y])

    # Plot the particle ball data
    if USE_PARTICLE_FILTER:
        particle_ball_plot.set_data([particle_ball_data[i].position().x], [particle_ball_data[i].position().y])
        particle_ball_velocity.set_data([particle_ball_data[i].position().x,
                                         particle_ball_data[i].position().x + particle_ball_data[i].velocity().x],
                                        [particle_ball_data[i].position().y,
                                         particle_ball_data[i].position().y + particle_ball_data[i].velocity().y])

    # Plot the mathew custom filter ball data
    if USE_MATHEW_CUSTOM_FILTER:
        mathew_custom_plot.set_data([mathew_custom_ball_data[i].position().x],
                                    [mathew_custom_ball_data[i].position().y])
        mathew_custom_velocity.set_data([mathew_custom_ball_data[i].position().x,
                                         mathew_custom_ball_data[i].position().x + mathew_custom_ball_data[i].velocity().x],
                                        [mathew_custom_ball_data[i].position().y,
                                         mathew_custom_ball_data[i].position().y + mathew_custom_ball_data[i].velocity().y])

    # Plot the mathew particle filter ball data
    if USE_MATHEW_PARTICLE_FILTER:
        mathew_particle_plot.set_data([mathew_particle_ball_data[i].position().x],
                                      [mathew_particle_ball_data[i].position().y])
        mathew_particle_velocity.set_data([mathew_particle_ball_data[i].position().x,
                                           mathew_particle_ball_data[i].position().x + mathew_particle_ball_data[i].velocity().x],
                                          [mathew_particle_ball_data[i].position().y,
                                           mathew_particle_ball_data[i].position().y + mathew_particle_ball_data[i].velocity().y])

    # plot friendly robots
    friendly_1.center = (friendly_1_data[i].position().x, friendly_1_data[i].position().y)
    friendly_2.center = (friendly_2_data[i].position().x, friendly_2_data[i].position().y)
    friendly_3.center = (friendly_3_data[i].position().x, friendly_3_data[i].position().y)
    friendly_4.center = (friendly_4_data[i].position().x, friendly_4_data[i].position().y)
    friendly_5.center = (friendly_5_data[i].position().x, friendly_5_data[i].position().y)
    friendly_6.center = (friendly_6_data[i].position().x, friendly_6_data[i].position().y)

    # plot enemy robots
    enemy_1.center = (enemy_1_data[i].position().x, enemy_1_data[i].position().y)
    enemy_2.center = (enemy_2_data[i].position().x, enemy_2_data[i].position().y)
    enemy_3.center = (enemy_3_data[i].position().x, enemy_3_data[i].position().y)
    enemy_4.center = (enemy_4_data[i].position().x, enemy_4_data[i].position().y)
    enemy_5.center = (enemy_5_data[i].position().x, enemy_5_data[i].position().y)
    enemy_6.center = (enemy_6_data[i].position().x, enemy_6_data[i].position().y)

    return field1, field2, field3, field4, field5, all_balls_scatter, \
           old_filter_plot, old_filter_velocity, \
           particle_ball_plot, particle_ball_velocity, \
           mathew_custom_plot, mathew_custom_velocity, \
           mathew_particle_plot, mathew_particle_velocity,\
           basepoints_scatter,

# create animation
ani = animation.FuncAnimation(fig, run, blit=True, interval=1,
                              # interval is 1 so has least delay while generating, since we just write it to a video later
                              repeat=False, init_func=init, frames=len(all_balls_data))

print("Writing out to {}".format(LOGFILE[:-4]))

# write animation to videos/ directory with name of logfile
Writer = animation.writers['ffmpeg']
writer = Writer(fps=FPS, metadata=dict(artist='Me'), bitrate=1800)
ani.save("videos/" + LOGFILE[:-4] + ".mp4", writer=writer)
