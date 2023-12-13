from tkinter import *
from PIL import ImageTk,Image
import ws
def sidebar_act(w,definition,thes):

    def toggle_win():
        def display_def(f1, definition):
            Title = Label(f1, text="DEFINITIONS:", bg='#96a3a1')
            label = Label(f1, text=definition, bg='#96a3a1')
            Title.place(x=5, y=60)
            label.place(x=5, y=80)

        def display_thes(f1, thes):
            Title = Label(f1, text="THESAURUS:", bg='#96a3a1')
            Title.place(x=5, y=120)
            for i in range(len(thes)):
                count = i*15
                label = Label(f1, text=thes[i], bg='#96a3a1')
                label.place(x=5, y= count + 140)

        global f1
        f1=Frame(w, width=300, height=500, bg='#96a3a1')
        f1.place(x=0,y=0)
        f1.grid_columnconfigure(0, weight=1)
        #buttons
        display_def(f1, definition)
        display_thes(f1, thes)

        def bttn(x, y, text, bcolor, fcolor, cmd):

            def on_entera(e):
                myButton1['background'] = bcolor #ffcc66
                myButton1['foreground']= '#262626'  #000d33

            def on_leavea(e):
                myButton1['background'] = fcolor
                myButton1['foreground']= '#262626'

            myButton1 = Button(f1,text=text,
                        width=42,
                        height=2,
                        fg='#262626',
                        border=0,
                        bg=fcolor,
                        activeforeground='#262626',
                        activebackground=bcolor,            
                            command=cmd)
                        
            myButton1.bind("<Enter>", on_entera)
            myButton1.bind("<Leave>", on_leavea)

            myButton1.place(x=x,y=y) 

        
        def dele():
            f1.destroy()
            b2=Button(w,image=img1,
                command=toggle_win,
                border=0,
                bg='#262626',
                activebackground='#262626')
            b2.place(x=5,y=8)

        global img2
        img2 = ImageTk.PhotoImage(Image.open("open3.png"))

        Button(f1,
            image=img2,
            border=0,
            command=dele,
            bg='#96a3a1',
            activebackground='#96a3a1').place(x=5,y=10)
        

    #default_home()

    img1 = ImageTk.PhotoImage(Image.open("open3.png"))

    global b2
    b2=Button(w,image=img1,
        command=toggle_win,
        border=0,
        bg='#262626',
        activebackground='#262626')
    b2.place(x=5,y=8)

    #w.mainloop()