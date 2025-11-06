import sys
#pygame SHUT UP
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import traceback
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk, ImageSequence
import requests
from io import BytesIO
import colorsys



'''
hello :3

---------------- BIG ASS WARNING THIS STUFF REQUIRES INTERNET CONNECTION TO EVEN WORK, OTHERWISE IT CRASHES
/todo:make it handle offline


'''

#----------------------CRASH HANDLER FROM SILLY PEOPLE -----------

def crash_handler(exc_type, exc_value, exc_traceback):
    #Handle uncaught exceptions and print clean crash info.
    if issubclass(exc_type, KeyboardInterrupt):
        # Allow Ctrl+C to exit normally
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    print("-" * 60)
    print("\nTHIS APP CRASHED YOU PROBABLY DON'T HAVE INTERNET CONNECTION YOU BONGO HEAD!\n")
    print("-" * 60)
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    print("\n")
    print("-" * 60)
    print("The app will not close automatically. Press Enter to exit.")
    input()  # keep window open

sys.excepthook = crash_handler

#------------------END OF CRASH HANDLER----------

print("Hello and welcome to my silly funny app\nlets hope you have internet connection otherwise you wouldnt even have this app thingy ^w^\nloading app please wait this could take a while...")


#------VARIABLES HERE PLS ----------
early = 0.437

#------STARTS PYGAME --------------
pygame.mixer.init()


#----------------DOWNLOADS IMAGES FROM INTERNET-------


gif_url = "https://media.tenor.com/7lHdnabfyTQAAAAj/herta-kurukuru.gif" #spinny herta gif
response = requests.get(gif_url)
gif_data = BytesIO(response.content)

url = "https://i.redd.it/7mtv74ytsxh91.png" #nahida fan art by u/omgRimuu
response = requests.get(url)
img_data = response.content

#-------------DOING SOME SOUND STUFF-----------
sound_url = "https://www.mobiles24.co/metapreview.php?id=648368&cat=3&h=13939912" #herta kuru kuru sound file
sound_data = BytesIO(requests.get(sound_url).content)
sound = pygame.mixer.Sound(sound_data)
sound_length = sound.get_length()
channel = pygame.mixer.Channel(0) 


#------------------RAINBOW BUTTON SECTION ------------

class RainbowButton(Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.default_bg = kwargs.get("bg", "#1e90ff")
        self.default_fg = kwargs.get("fg", "white")
        self.hue = 0
        self.running = False

        # Bind hover & click events TODO: FIX CLICK AND HOLD
        self.bind("<Enter>", self.start_rainbow)
        self.bind("<Leave>", self.stop_rainbow)
        
    def rainbow_cycle(self):
        #Animate rainbow background for this button only.
        if not self.running:
            return

        #does some colour fix for gif
        r, g, b = colorsys.hsv_to_rgb(self.hue, 1, 1)
        color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        self.config(bg=color, fg=self.default_fg)

        self.hue = (self.hue + 0.01) % 1.0
        self.after(50, self.rainbow_cycle)

    def start_rainbow(self, event=None): #loop of rainbow
        self.running = True
        self.rainbow_cycle()
        if not self.running:
            self.running = True
            self.rainbow_cycle()

    def stop_rainbow(self, event=None): #stops rainbow
        self.running = False
        self.config(bg=self.default_bg, fg=self.default_fg)
#------------------- END OF RAIBOW BUTTON SECTION-------------


#-----------------LAUNCHES THE MAIN WINDOW AND INITILIAZES IT-----
window = Tk()
window.title('Ternarinio kompiuterio emuliatorius')
window.geometry('400x400')

text = Label(window, text="Aurimai, is dariaus ir gireno 50, tai koks atsakymas?")
text.pack()

#-------DEFINES FUNCTIONS ------------------ -------

def massage():
    messagebox.showinfo("Test", "Kažkas įvyko!") #just opens simple new message box with set parameters

def dofunnything(): #big function that does some funny stuff 
    # Create new window
    win = Toplevel(window)
    win.title("Animated GIF + Sound")
    win.geometry("200x166")
    win.resizable(False, False)
    
    #Plays defined sound earlier from set time period
    def play_loop_early():
        if not win.winfo_exists():
            return  # stop if window closed
        channel.play(sound)
        restart_time = max(0, int((sound_length - early) * 1000))
        win.after(restart_time, play_loop_early)  # schedule next restart


    #opens gif downloaded previously
    gif_image = Image.open(gif_data)

    # Label for GIF
    gif_label = Label(win)
    gif_label.pack()

    # Extract all frames of GIF
    frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(gif_image)]

    # Function to animate GIF frames in loop
    def animate(ind=0):
        gif_label.config(image=frames[ind])
        ind = (ind + 1) % len(frames)  # loop back to first frame
        win.after(60, animate, ind)   # loop every 100 ms

    animate()  # start animation'''
    play_loop_early() #plays sound loop

def show_python_info(): #gets information about python: version and interpreter
    # Get Python version
    version = sys.version  # e.g., "3.11.4 (tags/v3.11.4:...)"
    
    # Get Python interpreter path
    interpreter = sys.executable  # e.g., "C:/Python311/python.exe"
    
    # Combine info
    info = f"Python Version:\n{version}\n\nInterpreter Path:\n{interpreter}"
    
    # Show in message box
    messagebox.showinfo("Python Info", info)

#creates top_frame group so buttons could be lined niceley
top_frame = Frame(window)
top_frame.pack(side=TOP, pady=10)

#creates button 1 with set parameters
btn = Button(top_frame, text="Paspausk mygtuką", command=massage)
btn.grid(row=0,column=1, padx=10)

#creates button 2 with some default customization and starts do funny thing function
btn2 = RainbowButton(
    top_frame, 
    text="linksma muzikele",
    fg="#FFFF00", 
    bg="#FFA500",
    font=("Arial", 10),
    command=dofunnything
    )
btn2.grid(row=0,column=0,padx=10)

#creates simple button 3 and calls show python info
btn3 = Button(top_frame, text="debug",command=show_python_info)
btn3.grid(row=0,column=2,padx=10)



#------------IMAGING STUFF FOR BOTTOM OF MAIN WINDOW------------

image = Image.open(BytesIO(img_data)) #loads nahida fan art
image = image.resize((208,325)) #resizes image so it fin in window
photo = ImageTk.PhotoImage(image)

#image label init and creation and shows image
img_label = Label(window, image=photo)
img_label.image = photo
img_label.pack(side=BOTTOM,pady=20)



window.mainloop()

#----------END OF MAIN WINDOW STUFF----




