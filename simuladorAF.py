#!/usr/bin/env python3


import os
from tkinter import Tk, Menu, filedialog, messagebox, simpledialog
import tkinter as tk
import tkinter.scrolledtext as tkst
import subprocess, sys





class MainWindows(Tk):
    def __init__(self):
        super().__init__()
        self.Aut = None
        self.title("Simulador AFD")

        self.resizable(0,0)
        self.filename = ""
        self.create_menu_bar()
        self.create_automat_frame()
        tk.Button(self, text="Llegir ...",command=self.run_automat).grid(row=4, column=0, sticky='W', padx=5, pady=2)

    def create_menu_bar(self):
        self.menubar = Menu(self)

        # CASCADA FILE
        self.file = Menu(self.menubar, tearoff=0)
        self.file.add_command(label="Carregar Automat", command=self.Open_file)
        self.file.add_separator()
        self.file.add_command(label="Sortir", command=self.quit)
        # CASCADA RUN
        self.run_aut = Menu(self.menubar, tearoff=0)
        self.run_aut.add_command(label="Llegir...", command=self.run_automat)
        self.run_aut.add_command(label="Esborrar configuracio", command=self.reset_dialog)

        # CASCADA HELP
        self.help = Menu(self.menubar, tearoff=0)
        self.help.add_command(label="Obrir ajuda",command=self.show_help)

        # add FILE, EDIT , HELP to menubar
        self.menubar.add_cascade(label="Automat", menu=self.file)
        self.menubar.add_cascade(label="Iniciar", menu=self.run_aut)
        self.menubar.add_cascade(label="Ajuda", menu=self.help)
        self.config(menu=self.menubar)
    def show_help(self):
        try:
            open( 'help.txt', 'r')
        except (FileNotFoundError,FileExistsError):
            messagebox.showerror(title="Simulador AFD",message="No s'ha trobat el fitxer d'ajuda")
        else:
            if os.name == 'nt':
                osCommandString = "notepad.exe help.txt"
                os.system(osCommandString)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, 'help.txt'])

    def create_automat_frame(self):
        #DetailsFrame
        self.frame_automat_details = tk.LabelFrame(self, text=" Automat configurat ")
        self.frame_automat_details.grid(row=0, columnspan=7, sticky='W', padx=5, pady=5, ipadx=5, ipady=5)
        #elements inside of DetailsFrame
        self.file_automat = tk.Label(self.frame_automat_details, text="Automat Carregat:")
        self.num_states = tk.Label(self.frame_automat_details, text="Numero d'estats:")
        self.final_states = tk.Label(self.frame_automat_details, text="Estats finals:")
        self.accepted_abc = tk.Label(self.frame_automat_details, text="Alfabet acceptat:")
        # placing elements
        self.file_automat.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        self.num_states.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        self.final_states.grid(row=2, column=0, sticky='E', padx=5, pady=2)
        self.accepted_abc.grid(row=3, column=0, sticky='E', padx=5, pady=2)

        # AutomatOutputFrame
        self.frame_AutomatLog = tk.LabelFrame(self, text=" Automat ")
        self.frame_AutomatLog.grid(row=0, column=9, columnspan=2, rowspan=8, sticky='NS', padx=5, pady=5)
        # elements inside of AutomatOutputFrame
        self.automat_output = tkst.ScrolledText(self.frame_AutomatLog,wrap=tk.WORD,width=40, height=10)
        # placing elements
        self.automat_output.grid(row=0)

    def editText(self):

        array=list((self.filename.split("/")))
        if array[len(array)-1]=='':
            self.file_automat.configure(text="Automat Carregat:")
            if self.Aut != None:
                self.Aut.set_file_table("")
            self.filename = ""
            self.automat_output.delete(1.0, tk.END)
            self.file_automat.configure(text="Automat Carregat:")
            self.num_states.configure(text="Automat Carregat:")
            self.final_states.configure(text="Estats finals:")
            self.accepted_abc.configure(text="Alfabet acceptat:")
        else:
            self.file_automat.configure(text="Automat Carregat: "+array[len(array)-1])

    def Open_file(self):
        self.automat_output.configure(state='normal')
        self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Seleccionar fitxer de configuracio",
                                                   filetypes=(("txt files", "*.txt"),
                                                              ("all files", "*.*")))
        if not (self.filename == () or self.filename == ""):
            self.automat_output.delete(1.0, tk.END)
            self.editText()
            messagebox.showinfo(message="Automat configurat", title="Simulador AFD")
            self.Aut = Automat(self.filename,self)
        else:
            if self.Aut != None:
                self.filename = self.Aut.file_table
                
    def reset(self):
        if self.Aut != None:
            self.Aut.set_file_table("")
        self.filename = ""
        self.automat_output.delete(1.0, tk.END)
        self.file_automat.configure(text="Automat Carregat:")
        self.num_states.configure(text="Automat Carregat:")
        self.final_states.configure(text="Estats finals:")
        self.accepted_abc.configure(text="Alfabet acceptat:")
        messagebox.showinfo(message="Automat reiniciat", title="Simulador AFD")
        self.Aut = None

    def reset_dialog(self):

        self.automat_output.configure(state='normal')
        s = messagebox.askquestion(icon='warning', title="Simulador AFD", message="Estas segur de reiniciar?")
        if s == 'yes':
          
            self.reset()


    def run_automat(self):

        self.automat_output.configure(state='normal')
        if not (self.filename == () or self.filename == ""):
            self.automat_output.delete(1.0, tk.END)
            answer = simpledialog.askstring("Simulador AFD", "Sisplau introdueixi una paraula a llegir",
                                            parent=self)
            if answer != None:
                self.Aut.set_word(answer)

                if self.is_valid_string(answer):
                    self.Aut.run()
                else:
                    messagebox.showerror(title="Simulador AFD",message="S'han detectat elements fora de l'alfabet acceptat")
        else:
            messagebox.showinfo(message="No s'ha configurat l'automat", title="Simulador AFD")

    def is_valid_string(self,answer):
        for letter in answer:
            if not (letter in self.Aut.ABC):
                return False
        return True



class Node:
    def __init__(self, nombre, successors, trigger, end_state):
        self.name_label = nombre
        self.succesors = successors
        self.trigger = trigger
        self.is_end = end_state

    def getSuccesors_string(self):
        s = []
        for p in self.succesors:
            s.append(str(p))
        return s

    def getSuccessor(self, i):
        r = self.succesors[i]
        
    def __str__(self):
        d = "" if self.is_end == False else " +"

        return self.name_label + str(self.getSuccesors_string()) + self.trigger + " " + d


class Automat:
    def __init__(self, filename="",window=None):
        self.file_table = filename
        self.cadena = ""
        self.window=window
        self.setup_automat()
    def set_word(self, newWord):
        self.cadena = newWord
    def set_file_table(self, filename):
        self.file_table = filename
    def letters_in_abc(self, string):
        for letter in string:
            if not(letter in self.ABC):
                return False
        return True
    def setup_automat(self):

        self.load_final_states()
        num_states = len(self.raw_states)

        self.reference_states = []
        self.automat_nodes = []

        # creates reference states
        abc_cmp=False
        self.ABC=[]
        # reference states
        for index in range(num_states):
            s = self.raw_states[index].split(",")
            self.reference_states.append(Node(s[0], [], "*", False))

        # creates and load states
        for i in range(num_states):
            nombre_configurado, siguientes = self.raw_states[i].split(",")
            # pointer states  ------> config states
            siguientes = list(siguientes.split("-"))
            sucessores = []
            for px in siguientes:
                etx = px.split("/")
                sucx = self.find_create_new_node(etx[0], etx[1])
                if abc_cmp==False:
                    self.ABC.append(etx[1])
                sucessores.append(sucx)
            abc_cmp=True
            finalz = True if nombre_configurado in self.final_states_labels else False

            self.automat_nodes.append(Node(nombre_configurado, sucessores, '*', finalz))
        self.window.accepted_abc.configure(text="Alfabet acceptat:"+str(self.ABC))
    def load_final_states(self):
        f = open(self.file_table, 'r')
        fl = f.read().split("\n")
        data = list(fl)
        self.final_states_labels, data = self.get_final_states(data)
        self.raw_states = list(data)
    def get_final_states(self, file):
        labels = []
        data = []
        for linea in file:
            array_char = list(linea)
            if array_char == []:
                pass
            elif len(array_char) != 0 and array_char[0] == "!":
                pass
            else:
                if len(array_char) != 0 and array_char[0] == "#":
                    if len(array_char) != 1:
                        final_state = linea.split("#")

                        labels.append(final_state[1])
                elif len(array_char) != 0 and array_char[0] == "$":
                    if len(array_char) != 1:
                        #print("estat inicial ", array_char[1])
                        pass
                else:
                    data.append(linea)
        self.window.num_states.configure(text="Numero d'estats: " + str(len(data)))
        self.window.final_states.configure(text="Estats finals: "+str(labels))



        return labels, data
    def find_create_new_node(self, etiqueta_a_buscar, trigger):
        original_node = self.find_create_node_no_modif_original(etiqueta_a_buscar)
        node_set = self.modify(original_node, trigger)
        return node_set
    def modify(self, Suc1, trigger):
        newNode = Node(Suc1.name_label, Suc1.succesors, trigger, Suc1.is_end)
        return newNode
    def find_create_node_no_modif_original(self, state_label):
        for state in self.reference_states:
            if state_label == state.name_label:
                return state
    def find_by_next_label(self, caracter, predecesores):
        for succ in predecesores:
            if succ.trigger == caracter:
                # print("puntero -->", succ.nombre)
                return succ.name_label
        return "!"
    def find_state_by_pointer(self, pointer):
        index = 0
        for state in self.automat_nodes:
            if state.name_label == pointer:
                return state, index
            index = index + 1

        return None, -1
    def run(self):
        string = list(self.cadena)


        if len(string)!=0:
            self.window.automat_output.insert('end', "Entrada " + str(string) + "\n")
            iterador = 0

            estado_siguiente = self.automat_nodes[0]

            while string != []:
                last_state = estado_siguiente.name_label
                self.window.automat_output.insert('end',"Llegit '" + string[0] +"' a l'estat '" + estado_siguiente.name_label + "'\n")
                puntero = self.find_by_next_label(string[0], self.automat_nodes[iterador].succesors)

                string = string[1:]
                estado_siguiente, iterador = self.find_state_by_pointer(puntero)
                if (len(string) == 0 and estado_siguiente.is_end == False):
                    self.window.automat_output.insert('end', "Error de lectura\nfinalitzat a l'estat "+estado_siguiente.name_label+"\n")
                    messagebox.showerror(title="Simulador AFD",message="La paraula no ha estat acceptada")
                    break
                if (len(string) == 0 and estado_siguiente.is_end):

                    self.window.automat_output.insert('end',
                                                      "Lectura correcta\nfinalitzat a l'estat '" + estado_siguiente.name_label + "'\n")
                    messagebox.showinfo(title="Simulador AFD",message="La paraula ha estat acceptada")

        else:
            messagebox.showerror(title="Simulador AFD",message="No es poden llegir paraules buides")
    def __str__(self):
        return self.file_table


if __name__ == '__main__':
    root = MainWindows()
    root.mainloop()
