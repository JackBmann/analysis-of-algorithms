import Tkinter as tk

import random as rand

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = tk.Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = tk.Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = tk.Button(master, text="Close",
                                      command=master.destroy)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")



class HilbertCurveCanvas:
    def __init__(self,master, d, size = 512):
        self.master = master
        self.d = d
        self.size = size
        self.linw = int(size/(4**(self.d+1)))

        ################## Key
        # 0: Opens up CCW.
        # 1: Opens left CCW.
        # 2: Opens down CCW.
        # 3: Opens right CCW.
        # 4: Opens up CW.
        # 5: Opens left CW.
        # 6: Opens down CW.
        # 7: Opens right CW.

        # substructures (by number) in order of visitation when
        # traveling counter-clockwise
        self.hilbsub = tuple([(4+(i + 1)%4, i, i, 4+(i + 3)%4)
                             for i in range(4)] +
                             [((i + 3)%4, i, i, (i + 1)%4)
                             for i in range(4,8)])
        # map of order of visitation to graphical xy coordinates
        self.hilbmap =( ((0,0), (0,1), (1,1), (1,0)),
                        ((0,1), (1,1), (1,0), (0,0)),
                        ((1,1), (1,0), (0,0), (0,1)),
                        ((1,0), (0,0), (0,1), (1,1)),
                        ((1,0), (1,1), (0,1), (0,0)),
                        ((0,0), (1,0), (1,1), (0,1)),
                        ((0,1), (0,0), (1,0), (1,1)),
                        ((1,1), (0,1), (0,0), (1,0)))
        self.stepsizes = {} # to multiply the by the hilbmap coordinates

        # make canvas and draw
        self.canv = tk.Canvas(self.master,
                              width = self.size, height = self.size)
        self.hilbPoints = []
        self.makeHilbert(0, 0, 4, 0)
        for p in range(len(self.hilbPoints)-1):
            self.canv.create_line(self.hilbPoints[p][0],
                                  self.hilbPoints[p][1],
                                  self.hilbPoints[p+1][0],
                                  self.hilbPoints[p+1][1],
                                  fill="#476042", width=self.linw)
        self.canv.pack()

        self.close_button = tk.Button(self.master, text="Close",
                                      command = self.master.destroy)
        self.close_button.pack()
        
    def makeHilbert(self, x, y, kind, d):
        if d == self.d or rand.random() < .1: # deep enough!
            s = self.stepsize(d+1)  # small step
            b = 2*s                 # big step
            for p in self.hilbmap[kind]:
                self.hilbPoints.append((x + s + b*p[0], y + s + b*p[1]))
            """
            if kind == 0: # opens upwards
                canv.create_line(x+s, y+s, x+s, y+b, fill="#476042", width=self.linw)
                canv.create_line(x+s, y+b, x+b, y+b, fill="#476042", width=self.linw)
                canv.create_line(x+b, y+b, x+b, y+s, fill="#476042", width=self.linw)
            elif kind == 1: # opens left
                canv.create_line(x+s, y+b, x+b, y+b, fill="#476042", width=self.linw)
                canv.create_line(x+b, y+b, x+b, y+s, fill="#476042", width=self.linw)
                canv.create_line(x+b, y+s, x+s, y+s, fill="#476042", width=self.linw)
            elif kind == 2: # opens downwards
                canv.create_line(x+b, y+b, x+b, y+s, fill="#476042", width=self.linw)
                canv.create_line(x+b, y+s, x+s, y+s, fill="#476042", width=self.linw)
                canv.create_line(x+s, y+s, x+s, y+b, fill="#476042", width=self.linw)
            elif kind == 3: # opens right
                canv.create_line(x+b, y+s, x+s, y+s, fill="#476042", width=self.linw)
                canv.create_line(x+s, y+s, x+s, y+b, fill="#476042", width=self.linw)
                canv.create_line(x+s, y+b, x+b, y+b, fill="#476042", width=self.linw)
            """
        else :
            s = self.stepsize(d)
            sub = self.hilbsub[kind]
            for i in range(4):
                dx, dy = self.hilbmap[kind][i]
                self.makeHilbert(x+dx*s,y+dy*s,sub[i],d+1)

    def stepsize(self, d):
        if self.stepsizes.has_key(d):
            return self.stepsizes[d]
        else :
            self.stepsizes[d] = int(self.size/(2**(d+1)))
            return self.stepsizes[d]
                     

root = tk.Tk()
#my_gui = MyFirstGUI(root)
my_hilb = HilbertCurveCanvas(root, 7)
#my_hilb = HilbertCanvas(root, 5)
root.mainloop()

"""
class HilbertCanvas:
    def __init__(self,master, d, size = 512):
        self.master = master
        self.d = d
        self.size = size
        self.linw = int(size/(4**(self.d)))

        ################## Key
        # 0: Opens up.
        # 1: Opens left.
        # 2: Opens down.
        # 3: Opens right.

        # substructures (by number) in order of visitation when
        # traveling counter-clockwise
        self.hilbsub = tuple(((i + 1)%4, (i)%4, (i)%4, (i + 3)%4)
                             for i in range(4))
        # map of order of visitation to graphical xy coordinates
        self.hilbmap = ( ((0,0), (0,1), (1,1), (1,0)),
                           ((0,1), (1,1), (1,0), (0,0)),
                           ((1,1), (1,0), (0,0), (0,1)),
                           ((1,0), (0,0), (0,1), (1,1)))
        self.stepsizes = {} # to multiply the by the hilbmap coordinates

        # make canvas and draw
        self.canv = tk.Canvas(self.master, width = self.size, height = self.size)
        self.drawHilbert(self.canv, 0, 0, 0, 0)
        self.canv.pack()

        self.close_button = tk.Button(self.master, text="Close",
                                      command = self.master.destroy)
        self.close_button.pack()
        
    def drawHilbert(self,canv, x, y, kind, d):
        if d == self.d: # deep enough!
            s = self.stepsize(d+1)  # small step
            b = 3*s                 # big step
            if kind == 0: # opens upwards
                canv.create_line(x+s, y+s, x+s, y+b, fill="#476042", width=self.linw)
                canv.create_line(x+s, y+b, x+b, y+b, fill="#476042", width=self.linw)
                canv.create_line(x+b, y+b, x+b, y+s, fill="#476042", width=self.linw)
            elif kind == 1: # opens left
                canv.create_line(x+s, y+b, x+b, y+b, fill="#476042", width=self.linw)
                canv.create_line(x+b, y+b, x+b, y+s, fill="#476042", width=self.linw)
                canv.create_line(x+b, y+s, x+s, y+s, fill="#476042", width=self.linw)
            elif kind == 2: # opens downwards
                canv.create_line(x+b, y+b, x+b, y+s, fill="#476042", width=self.linw)
                canv.create_line(x+b, y+s, x+s, y+s, fill="#476042", width=self.linw)
                canv.create_line(x+s, y+s, x+s, y+b, fill="#476042", width=self.linw)
            elif kind == 3: # opens right
                canv.create_line(x+b, y+s, x+s, y+s, fill="#476042", width=self.linw)
                canv.create_line(x+s, y+s, x+s, y+b, fill="#476042", width=self.linw)
                canv.create_line(x+s, y+b, x+b, y+b, fill="#476042", width=self.linw)
        else :
            s = self.stepsize(d)
            sub = self.hilbsub[kind]
            for i in range(4):
                dx, dy = self.hilbmap[kind][i]
                self.drawHilbert(canv,x+dx*s,y+dy*s,sub[i],d+1)

    def stepsize(self, d):
        if self.stepsizes.has_key(d):
            return self.stepsizes[d]
        else :
            self.stepsizes[d] = int(self.size/(2**(d+1)))
            return self.stepsizes[d]
"""
