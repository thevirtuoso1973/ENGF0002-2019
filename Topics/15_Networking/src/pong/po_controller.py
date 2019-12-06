# Simple Frogger Game.  Mark Handley, UCL, 2018

from tkinter import *
from po_model import Model
from po_view import View
from po_settings import Direction
from po_network import Network
from sys import argv
from getopt import getopt, GetoptError
import time

class Controller():
    def __init__(self):
        self.parse_args(argv)
        self.root = Tk();
        self.windowsystem = self.root.call('tk', 'windowingsystem')
        self.views = []
        self.root.bind_all('<KeyPress>', self.keypress)
        self.root.bind_all('<KeyRelease>', self.keyrelease)
        self.running = True
        self.scores = [0,0]
        self.bats = []
        self.ball = None
        self.net = Network(self, self.passwd)
        self.local_ip = self.net.get_local_ip_addr()        
        self.model = Model(self);
        self.add_view(View(self.root, self))
        self.init_net()
        self.model.activate(self.serv, self.autoplay)

    def parse_args(self, argv):
        try:
            if "pong.py" in argv[0]:
                opts, args = getopt(argv[1:], "sac:p:", ["server", "autoplay", "connect=", "passwd="])
            else:
                opts, args = getopt(argv, "sac:p:", ["server", "autoplay", "connect=", "passwd="])
        except GetoptError:
            self.usage()
        self.passwd = "000000"
        self.serv = False
        self.autoplay = False
        self.connect_to = "127.0.0.1"
        for opt, arg in opts:
            if opt in ("-s", "--server"):
                # there's not really a server, but we need to decide
                # ports, and they can't be the same on localhost, so
                # this gives us an asymmetry we can use to determine P1 vs P2
                self.serv = True
            elif opt in ("-a", "--autoplay"):
                self.autoplay = True
            elif opt in ("-c", "--connect"):
                self.connect_to = arg
            elif opt in ("-p", "--passwd"):
                self.passwd = arg
            else:
                self.usage()
        if self.serv:
            print("P2 mode, password is ", self.passwd, "connecting to", self.connect_to)
        else:
            print("P1 mode, password is ", self.passwd, "connecting to", self.connect_to)

    def init_net(self):
        if self.serv:
            self.net.peer(9872, self.connect_to, 9873)
        else:
            self.net.peer(9873, self.connect_to, 9872)

    def usage(self):
        print("pong.py [-s | --server] [-c <ip address> | --connect=<ip address>] \n          [-p <password> | --passwd=<password>]")
        sys.exit(2)            

    def register_bat(self, obj):
        self.bats.append(obj)
        for view in self.views:
            view.register_bat(obj)

    def register_ball(self, ball):
        self.ball = ball
        for view in self.views:
            view.register_ball(ball)

    def rotate_scene(self):
        for view in self.views:
            view.rotate_view()

    def add_view(self, view):
        self.views.append(view)
        view.register_ball(self.ball)
        for obj in self.bats:
            view.register_bat(obj)

    #handle communication updates
    def update_bat(self, bat):
        self.net.send_bat_update(bat.y, bat.velocity)

    def remote_bat_update(self, y, vy):
        self.model.remote_bat_update(y, vy)

    def update_ball(self, ball):
        self.net.send_ball_update(ball.position, ball.velocity)

    def remote_ball_update(self, pos, velocity):
        self.model.remote_ball_update(pos, velocity)

    #some helper functions to hide the controller implementation from
    #the model and the controller
    def update_scores(self, scores):
        self.scores = scores

    def get_scores(self):
        return self.scores
        
    def game_over(self):
        for view in self.views:
            view.game_over()
        
    def keypress(self, event):
        if event.char == 's' or event.keysym == 'Up':
            self.current_keysym = event.keysym
            self.model.move_bat(Direction.UP)
        elif event.char == 'd' or event.keysym == 'Down':
            self.current_keysym = event.keysym
            self.model.move_bat(Direction.DOWN)
        elif event.char == 'q':
            self.running = False
        elif event.char == 'r':
            for view in self.views:
                view.clear_messages()
            self.model.restart()

    def keyrelease(self, event):
        # only cancel the move if the keyup is the same as the most recent keydown
        # avoids problems when overlap between keypresses
        if self.current_keysym == event.keysym:
            self.model.move_bat(Direction.NONE)

    def run(self):
        i = 0
        last_time = time.time()
        while self.running:
            now = time.time()
            self.net.check_for_messages(now)
            self.model.update()
            for view in self.views:
                view.update()
            self.root.update()
            i = i + 1
            if i == 60:
                t = time.time()
                elapsed = t - last_time
                last_time = t
                fps = 60/elapsed
                i = 0;
        self.root.destroy()
