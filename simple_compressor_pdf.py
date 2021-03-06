# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox
import os
import subprocess
import platform
import traceback


def os_name(name_os, name_original, name_reemplazo):
    if name_os == "posix":
        arquitectura = platform.architecture()[0]
        if arquitectura == "64bit":
#            print(arquitectura)
            procesado_gs = f"bins/linux/x64/gs-9533-linux-x86_64 -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET " \
                           f"-dBATCH -sOutputFile={name_reemplazo}".split()
            procesado_gs.append(f"{name_original}")
            return procesado_gs
        elif arquitectura == "32bit":
            procesado_gs = f"bins/linux/x32/gs-9533-linux-x86 -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET " \
                           f"-dBATCH -sOutputFile={name_reemplazo}".split()
            procesado_gs.append(f"{name_original}")
            return procesado_gs
    elif name_os == "nt":
        comando = f'-sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH ' \
                  f'-sOutputFile={name_reemplazo}'.split()
        comando.append(name_original)
        comando.insert(0, f"bins\\bin\\gswin64c.exe")
#        print(comando)
        return comando
        

def abrir_fichero():
    try:
        boton_abrir['image'] = ""
        boton_abrir['image'] = img_wait
        filename = filedialog.askopenfiles(filetypes=[("Pdf files", "*.pdf")], title="Seleccione documentos PDFs")
        for nombre_file in filename:
            name = os.path.basename(nombre_file.name)
            reemplazo = f"{name[:-4].replace(' ', '_')}-compressed.pdf"
            if os.path.exists(reemplazo):
                msg_sn = messagebox.askyesno(message=f"¿Reemplazar?\n{name}", title="Conflicto ficheros")
                if msg_sn is True:
                    subprocess.run(os_name(os.name, name, reemplazo))
                    messagebox.showinfo(message="Listo!")
#                    print("Finish")
                else:
                    continue
            else:
                subprocess.run(os_name(os.name, name, reemplazo))
                messagebox.showinfo(message="Listo!")
#                print("Finish")
    except:
        rastreo = traceback.format_exc()
#        print(rastreo)
        return rastreo
    finally:
        boton_abrir['image'] = img_open


def command_about():
    texto = "Simple Compressor PDF\n 'If you like this little program,\nfeel free leave me a comment,\n" \
            "or improvement proposal.'"

    bs = tk.Tk()
    bs.title("")

    color = "#3382b3"
    fuente = font.Font(family="Helvetica", weight="bold")

    fr_ab = tk.Frame(bs, bg="#3382b3")
    lbl_title = tk.Label(fr_ab, text="kurotom - 2021", bg=color)
    lbl_text = tk.Label(fr_ab, text="", bg=color)
    lbl_text['text'] = texto
    lbl_title.config(fg="white", font=fuente)
    lbl_text.config(fg="white")
    lbl_title.grid(ipadx=10, ipady=10)
    lbl_text.grid(ipadx=10, ipady=10)
    fr_ab.grid()
    bs.grid()


def salir():
    base.quit()


base = tk.Tk()
base.title("Simple PDF Compressor")

imagen_canvas = tk.PhotoImage(file="icons/compress_icon.png").subsample(4, 3)
img_about = tk.PhotoImage(file="icons/about.png").subsample(2, 2)
img_open = tk.PhotoImage(file="icons/open.png").subsample(1, 1)
img_quit = tk.PhotoImage(file="icons/quit_icon.png").subsample(2, 2)
img_wait = tk.PhotoImage(file="icons/wait.png").subsample(1, 1)

canvas = tk.Canvas(base, width=400, height=300, borderwidth=0)
canvas.create_image(200, 40, image=imagen_canvas, anchor="nw")

boton_abrir = tk.Button(base, image=img_open, command=abrir_fichero, borderwidth=5, highlightthickness=3, bg="#e08d3c")
boton_quit = tk.Button(base, image=img_quit, command=salir, borderwidth=5, highlightthickness=3, relief="raised",
                       bg="#ff6f69")
label_about = tk.Button(base, image=img_about, command=command_about, relief="raised", borderwidth=5,
                        highlightthickness=3, bg="#6ca580")

canvas.place(x=0, y=0)
canvas.config(bg="#65c3ba")

boton_abrir.place(x=40, y=70)
boton_quit.place(x=3, y=249)
label_about.place(x=3, y=3)

base.geometry("400x300")
base.update()
base.resizable(width=0, height=0)
base.mainloop()

