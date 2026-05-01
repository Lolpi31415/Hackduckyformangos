"""
Script that is ran at the end of the setup thing that will run after the setup is finished after the text file is made.
"""

import random
import math
import time
import os 
import threading

import tkinter as tk


MESSAGES = [
    "Congratulations!",
    "Hip hip Hooray!!",
    "Your computer is all set up now :>",
    "Have a good time!",
]

class Particle:
    def __init__(self, canvas, x, y, color):
        self.x = x 
        self.y = y

        self.color = color
        self.canvas = canvas

        size = random.randint(4, 15)

        self.shape = "oval"
        self.id = canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
        """Took this from w3 schools idk what outline does"""

        angle = random.uniform(0, 2 * math.pi)
        self.alive = True
        speed = random.uniform(2, 7)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - random.uniform(2, 5)
        """trigonometry, yeppie"""

        self.gravity = random.uniform(0.1, 0.4)
        """makem fall"""

        self.life = 1.0
        self.decay = random.uniform(0.01, 0.035)
        """How fast they disapear so they dont stay like a pest"""

    def update(self):
        self.vy += self.gravity

        self.x += self.vx
        self.y += self.vy

        self.life -= self.decay

        if self.life <= 0:
            self.alive = False
            self.canvas.delete(self.id)
            return

        self.canvas.move(self.id, self.vx, self.vy)

        if self.life < 0.3:
            self.canvas.itemconfig(self.id, fill=self.color, outline="")
            """makes them fade out so it looks cooler"""


"""text window"""

PALETTES = [
    {"bg": "#1a0a2e", "accent": "#ff6bff", "text": "#ffffff", "particle": ["#ff6bff", "#ffcc00", "#00ffcc"]},
    {"bg": "#0a1a2e", "accent": "#00d4ff", "text": "#ffffff", "particle": ["#00d4ff", "#ff6b6b", "#ffcc00"]},
    {"bg": "#1a2e0a", "accent": "#7fff00", "text": "#ffffff", "particle": ["#7fff00", "#ff6bff", "#ffcc00"]},
    {"bg": "#2e0a0a", "accent": "#ff6b6b", "text": "#ffffff", "particle": ["#ff6b6b", "#00d4ff", "#ffcc00"]},
    {"bg": "#2e1a0a", "accent": "#ffaa00", "text": "#ffffff", "particle": ["#ffaa00", "#ff6bff", "#00ffcc"]},
]
"""chose a bunch of random colors and whatnot for the windows and maybe the confetti"""


class Horray:
    def __init__(self, index):
        self.root = tk.Tk()
        self.root.title("Congratulations!")

        W, H = 480, 380
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        """gets the screen width and height so it can be randomaized"""
        ox = random.randint(0, screen_w - W)
        oy = random.randint(0, screen_h - H)

        """should make them not overlap"""

        self.root.geometry(f"{W}x{H}+{ox}+{oy}")
        """makes the window pop up in a random place on the screen"""

        self.root.resizable(False, False)
        """makes the window not resizable so it is fixed"""


        palette = PALETTES[index % len(PALETTES)]
        self.bg = palette["bg"]
        self.accent = palette["accent"]
        self.text_color = palette["text"]
        self.particle_colors = palette["particle"]

        self.root.configure(bg=self.bg)

        """make the canvas"""
        
        self.canvas = tk.Canvas(self.root, width=W, height=H, bg=self.bg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        cvx, cvy = W // 2, H // 2
        msg = MESSAGES[index % len(MESSAGES)]
        self.canvas.create_text(cvx, cvy - 30, text=msg,
                                font=("Courier", 22, "bold"),
                                fill=self.accent, anchor="center")

        self.canvas.create_text(cvx, cvy + 20, text="Your computer is all set up now :>",
                                font=("Courier", 14, "bold"),
                                fill=self.text_color, anchor="center")

        """now for the button to close the window so it looks better than just clicking the x and it makes it more obvious"""
        btn = tk.Button(self.root, text="Exit",
                        command=self.root.destroy,
                        bg=self.accent, fg=self.bg,
                        font=("Courier", 11, "bold"),
                        relief="flat", padx=14, pady=6, cursor="hand2")
        """for windows and i think other OS but this is only for windows lol"""

        self.canvas.create_window(cvx, cvy + 80, anchor="center", window=btn)

        self.particles = []
        self.W = W
        self.H = H
        self.running = True
        """is it running though"""

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self._animate()
        self._burst()

    def _burst(self):
        cvx, cvy = self.W // 2, self.H // 2
        for _ in range(60):
            color = random.choice(self.particle_colors)
            p = Particle(self.canvas, cvx, cvy, color)
            self.particles.append(p)

    """particles when the window closes i think, VS code offered this suggestion and i took it"""

    def _animate(self):
        if not self.running:
            return

        for p in self.particles[:]:
            if p.alive:
                p.update()
            else:
                self.particles.remove(p)

        t = time.time()
        r = int(80 + 15 * math.sin(t * 5))
        """sin makes it random i think"""
        self.canvas.delete("pulse")
        cvx, cvy = self.W // 2, self.H // 2
        self.canvas.create_oval(cvx - r, cvy - r - 30, cvx + r, cvy + r - 30,
                                outline=self.accent, width=2, tags="pulse")

        self.root.after(30, self._animate)

    def on_close(self):
        self.running = False
        self.root.destroy()

    def run(self):
        self.root.mainloop()


def launch_window(index):
    win = Horray(index)
    win.run()


def main():
    NUM_WINDOWS = 6

    threads = []
    for i in range(NUM_WINDOWS):
        t = threading.Thread(target=launch_window, args=(i,), daemon=True)
        threads.append(t)
        t.start()
        time.sleep(0.15)

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()
