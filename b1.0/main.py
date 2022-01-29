import time
from tkinter import *
from tkinter.font import Font
import tkinter
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename, askopenfilename
from PIL import Image, ImageTk
import subprocess,os,platform,json

if not os.path.isfile("ide.json"):
    with open("ide.json","w") as f:
        json.dump({"last_fp": "/","last_fpp": "/","col_1": "#000","col_2": "#fff"},f,indent=4)

file_path=""

compiler = Tk()
compiler.title('IDE')
compiler.geometry(f"{compiler.winfo_screenwidth()}x{compiler.winfo_screenheight()}+0+0")
compiler.update()
filetypes=[('Python', '*.py'),("C++","*.cpp"),("JavaScript","*.js")]

def count_substrings(string, substring):
    string_size = len(string)
    substring_size = len(substring)
    count = 0
    for i in range(0,string_size-substring_size+1):
        if string[i:i+substring_size] == substring:
            count+=1
    return count

def set_file_path(path):
    with open("ide.json","r") as f:
        ide=json.load(f)
    global file_path
    file_path = path
    ide["last_fp"]=path
    with open("ide.json","w") as f:
        json.dump(ide,f,indent=4)

def set_file_path2(path):
    with open("ide.json","r") as f:
        ide=json.load(f)
    global file_path
    file_path = path
    ide["last_fpp"]=path
    with open("ide.json","w") as f:
        json.dump(ide,f,indent=4)

def delete_last_after_slash(input:str):
    input=input.split("/")
    input.pop(len(input)-1)
    raw_output=input
    output=""
    for a in raw_output:
        output=output+a+"/"
    return output

def get_last_after_slash(input:str):
    input=input.split("/")
    input=input[len(input)-1]
    return input

def open_manual(dir):
    with open(dir, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        if "." in dir:
            set_file_path(dir)
            dir=delete_last_after_slash(dir)
            print(dir)
        set_file_path2(dir)

def open_manual2(dir):
    if dir=="/":
        dir=askopenfilename(filetypes=filetypes)
    with open(dir, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(dir)

def open_file():
    path = askopenfilename(filetypes=filetypes)
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)
    return path

def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=filetypes)
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)

def run():
    if file_path == '':
        fpath=__file__.split("/")
        path=""
        for a in range(len(fpath)):
            if not a==len(fpath)-1:
                path=path+fpath[a]+"/"
        path=path+"main"
        for a in range(4567):
            if os.path.isfile(path+".py"):
                path=path+str(a)
            else:
                break
        path=path+".py"
        with open(path, 'w') as file:
            file.write(editor.get("1.0", END))
            set_file_path(path)
        command = f'python {path}'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        code_output.see(END)
        code_output.insert(END, output)
        code_output.insert(END,  error)
        code_output.see(END)
    save_as()
    if file_path.endswith(".py"):
        command = f'python {file_path}'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        code_output.see(END)
        code_output.insert(END, output)
        code_output.insert(END, error)
        code_output.see(END)

    elif file_path.endswith(".js"):
        command = f'node {file_path}'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        code_output.see(END)
        code_output.insert(END, output)
        code_output.insert(END, error)
        code_output.see(END)

    elif file_path.endswith(".cpp"):
        subprocess.call(f'gcc -o r {file_path}', shell=True)
        output, error = process.communicate()
        code_output.see(END)
        code_output.insert(END, error)
        code_output.see(END)
        if "win" in platform.system().lower():
            command = f'r.exe'
        else:
            command = f'./r'
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            code_output.see(END)
            code_output.insert(END, output)
            code_output.insert(END, error)
            code_output.see(END)
    elif file_path.endswith(".html") or file_path.endswith(".css"):
        code_output.see(END)
        code_output.insert(END, "There is nothing to run, unavailable for now.")
        code_output.see(END)
    else:
        messagebox.showerror("Unknown Format", f"Supported: {[b for a, b in filetypes]}")

def update_colors():
    with open("ide.json","r") as f:
        ide=json.load(f)
    editor.config({"bg":ide["col_2"],"insertbackground":ide["col_1"],"fg":ide["col_1"]})
    code_output.config(bg=ide["col_2"],insertbackground=ide["col_1"],fg=ide["col_1"])
    current_file.config(bg=ide["col_2"],fg=ide["col_1"])
    mainarea.config(bg=ide["col_2"])
    sidebar.config(bg=ide["col_2"])
    myListBox.config(bg=ide["col_2"],fg=ide["col_1"])
    menu_bar.config(bg=ide["col_2"],fg=ide["col_1"])

def open_settings():
    messagebox.showerror("Error","No Settings yet")

def open_color_settings():
    settingswin = Toplevel(compiler)
    settingswin.title("Color Settings")
    settingswin.geometry("550x150")
    def apply():
        changed=False
        code_1=Input_2.get("1.0",END)
        code_1=code_1.replace("\n","")
        if code_1!="" and (len(code_1) == 4 or len(code_1) == 7) and code_1.startswith("#") and any([a.lower() in "0123456789abcdef" for a in code_1]):
            with open("ide.json","r") as f:
                ide=json.load(f)
            ide["col_1"]=code_1
            with open("ide.json","w") as f:
                json.dump(ide,f,indent=4)
            changed=True
        code_1=Input_1.get("1.0",END)
        code_1=code_1.replace("\n","")
        if code_1!="" and (len(code_1) == 4 or len(code_1) == 7) and code_1.startswith("#") and any([a.lower() in "0123456789abcdef" for a in code_1]):
            with open("ide.json","r") as f:
                ide=json.load(f)
            ide["col_2"]=code_1
            with open("ide.json","w") as f:
                json.dump(ide,f,indent=4)
            changed=True
        if changed==True:
            update_colors()
    def dark_m():
        Input_1.delete("1.0",END)
        Input_1.insert("1.0","#000")
        Input_2.delete("1.0",END)
        Input_2.insert("1.0","#fff")
        apply()
    def light_m():
        Input_1.delete("1.0",END)
        Input_1.insert("1.0","#fff")
        Input_2.delete("1.0",END)
        Input_2.insert("1.0","#000")
        apply()
    text_1=Label(settingswin,text="Hex Primary")
    text_1.grid(column=0)
    Input_1=Text(settingswin,height=1,width=40)
    Input_1.grid(column=0)
    text_2=Label(settingswin,text="Hex Secondary")
    text_2.grid(column=0)
    Input_2=Text(settingswin,height=1,width=40)
    Input_2.grid(column=0)
    submit=Button(settingswin,text="Apply",command=apply)
    submit.grid(column=1,row=1)
    dark_mode=Button(settingswin,text="Dark Mode",command=dark_m)
    dark_mode.grid(column=1,row=2)
    light_mode=Button(settingswin,text="Light Mode",command=light_m)
    light_mode.grid(column=1,row=3)

def open_browser():
    browser=Toplevel(compiler)
    browser.title("New Window")
    browser.geometry(f"{compiler.winfo_screenwidth()}x{compiler.winfo_screenheight()}+0+0")

mainarea_width=int(compiler.winfo_width())
height=int(compiler.winfo_height())
mainarea = Frame(compiler, bg='#CCC', width=mainarea_width/7*4, height=height)
mainarea.pack(expand=True, fill='both', side='right')

sidebar = Frame(compiler, bg='white', relief='sunken', borderwidth=2, height=height,width=mainarea_width-mainarea_width/7*5)
sidebar.pack(expand=False, fill='both',side="right", anchor='nw')

menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

help_menu=Menu(menu_bar,tearoff=0)
help_menu.add_command(label="Settings")
menu_bar.add_cascade(label="Help",menu=help_menu)

menu_bar.add_command(label="Run",command=run)

compiler.config(menu=menu_bar)

current_file=Label(mainarea,text=file_path,bg="#fff",fg="#000",width=int(height/7.17),height=int(mainarea_width/6000))
current_file.pack()

editor = Text(mainarea,bg="#fff",fg="#000",insertbackground="#000",width=int(height/6.5),height=int(mainarea_width/60))
editor.pack()

# configuring a tag with a certain style (font color)
editor.tag_configure("pyblock", foreground="violet")
editor.tag_configure("str",background="orange")

code_output = Text(mainarea,width=int(height/6.5),height=int(mainarea_width//100))
code_output.pack()

home = ImageTk.PhotoImage(Image.open('home.png').resize((40,40),Image.ANTIALIAS))
settings = ImageTk.PhotoImage(Image.open('settings.png').resize((40,40),Image.ANTIALIAS))
brush = ImageTk.PhotoImage(Image.open('brush.png').resize((40,40),Image.ANTIALIAS))
www = ImageTk.PhotoImage(Image.open('www.png').resize((40,40),Image.ANTIALIAS))

frame = Frame(compiler,bg="black")

b_count=3
b_1 = Button(frame,image=home,relief='flat',bg="white",height=height/b_count)
b_2 = Button(frame,image=settings,relief='flat',bg="white",height=height/b_count,command=open_settings)
b_3 = Button(frame,image=brush,relief='flat',bg="white",height=height/b_count,command=open_color_settings)
b_4 = Button(frame,image=www,relief='flat',bg="white",height=height/b_count,command=open_browser)

b_1.pack(side="top")
b_2.pack(side="top")
b_3.pack(side="top")
b_4.pack(side="top")

frame.pack(side="left")

with open("ide.json","r") as f:
    ide=json.load(f)
try:
    file_path = ide["last_fp"]
except:
    path=open_file()
    ide["last_fp"]=path
    with open("ide.json","w") as f:
        json.dump(ide,f,indent=4)

def click(key):
    # print the key that was pressed
    replace=[["(",")"],["[","]"],["{","}"]]
    for a in replace:
        if key.char==a[0]:
            key.char=a[1]

    editor.insert(INSERT,key.char)

def check_block(key):
    if file_path.endswith(".py"):
        editor.tag_remove("pyblock",1.0,END)
        pyblocks=["try","except","if","else","elif","with","as","import","from","async","def", "class","finally","for","in","while","or","and"]
        for a in pyblocks:
            pos_start=1.0
            count=int((count_substrings(editor.get("1.0",END),a)))
            for _ in range(count):
                p= "+%dc" % len(a)
                try:
                    pos_start = editor.search(a, pos_start, END)
                    pos_end = pos_start+p
                    editor.tag_add('pyblock', pos_start, pos_end)
                    pos_start=float(pos_start)+0.01
                except tkinter.TclError:
                    pass
        pos_end="1.0"
        count=int((count_substrings(editor.get("1.0",END),"\""))/2)
        print(count)
        editor.tag_remove("str","1.0",END)
        for a in range(count):
            pos_start=editor.search("\"",pos_end,END)
            pos_start=float(pos_start)+0.01
            pos_end=editor.search("\"",pos_start,END)
            pos_start=float(pos_start)-0.01
            editor.tag_add("str",pos_start,float(pos_end)+0.01)

compiler.bind("\"", click)
compiler.bind("(", click)
compiler.bind("[", click)
compiler.bind("{", click)

checkblocktoggler=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

for a in checkblocktoggler:
    compiler.bind(a,check_block)

compiler.bind("<Tab>")

if file_path !="":
    open_manual2(file_path)

compiler.update()

with open("ide.json","r") as f:
    xd=json.load(f)

with open("ide.json","r") as f:
    ide=json.load(f)
try:
    fileselector=xd["last_fpp"].split("/")
except:
    fileselector="/"
    ide["last_fpp"]="/"
    with open("ide.json","w") as f:
        json.dump(ide,f,indent=4)

current_file.configure(text=get_last_after_slash(ide["last_fp"]))

def get_file_selector():
    global fileselector
    str=""
    for a in fileselector:
        if a!="":
            str=str+"/"+a
    if str=="":
        str="/"
    return str

lastChoose=""
def do_popup(event):
    global lastChoose
    try:
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            lastChoose=get_file_selector()+"/"+data
        else:
            lastChoose=None
    except Exception as e:
        messagebox.showerror("Error",e)
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()
        lastChoose=None

myListBox = Listbox(sidebar,height=height)
m=Menu(myListBox,tearoff=0)

m.add_command(label="Cut")
m.add_command(label="Copy")
m.add_command(label="Paste")
m.add_command(label="Reload")
m.add_separator()
m.add_command(label="Rename")

myListBox.bind("<Button-3>", do_popup)

if get_file_selector()!="" and get_file_selector()!="/":
    myListBox.insert(END, "..")

to_append=[]

for file in os.listdir(get_file_selector()):
    to_append.append(file)

to_append=sorted(to_append)

for file in to_append:
    myListBox.insert(END,file)

myListBox.pack()

def file_select(event):
    try:
        global fileselector
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            to_append=[]
            oldfileselector=fileselector
            print(data)
            if "." in data and not data.startswith(".") and data != "..":
                fileselector=(f"{get_file_selector()}/{data}").split("/")
                open_manual(get_file_selector())
                current_file.configure(text=data)
                fileselector=oldfileselector
            elif data ==".." and get_file_selector()!="" and get_file_selector()!="/":
                myListBox.delete(0,END)
                fileselector=delete_last_after_slash(get_file_selector()).split("/")
                if get_file_selector()!="" and get_file_selector()!="/":
                    myListBox.insert(END, "..")
                for file in os.listdir(get_file_selector()):
                    to_append.append(file)
                to_append=sorted(to_append)
                for file in to_append:
                    myListBox.insert(END,file)
            else:
                myListBox.delete(0,END)
                oldfileselector2=fileselector
                fileselector=(f"{get_file_selector()}/{data}").split("/")
                try:
                    os.listdir(get_file_selector())
                except NotADirectoryError:
                    fileselector=oldfileselector2
                    fileselector=(f"{get_file_selector()}/{data}").split("/")
                    try:
                        open_manual(get_file_selector())
                    except UnicodeDecodeError as e:
                        messagebox.showerror("Error",e)
                    finally:
                        fileselector=oldfileselector
                    current_file.configure(text=data)
                if get_file_selector()!="" and get_file_selector()!="/":
                    myListBox.insert(END, "..")
                for file in os.listdir(get_file_selector()):
                    to_append.append(file)
                to_append=sorted(to_append)
                for file in to_append:
                    myListBox.insert(END,file)
        time.sleep(0.3)
    except Exception as e:
        messagebox.showerror("Error",e)
        fileselector=oldfileselector

myListBox.bind("<<ListboxSelect>>", file_select)

update_colors()
compiler.mainloop()
