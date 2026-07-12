import ctypes
import os
import tkinter as tk
from tkinter import PhotoImage, ttk

from pomodoro_enum import EstadoPomodoro
from segredo import segredos


class PomodoroTimer:
    def __init__(self, root) -> None:
        self.root: tk.Tk = root
        self.root.iconbitmap("Python-Logo-PNG-Picture.ico")

        self.root.iconphoto(True, PhotoImage(file="pomodoro_image.png"))  # Aceita PNG

        self.notebook = ttk.Notebook(self.root)

        self.__novo_aba("Pomodoro")
        self.__novo_aba("Intevalo longo")
        self.__novo_aba("Intervalo curto")

        self.notebook.pack(fill="x")

        self.notebook.bind("<<NotebookTabChanged>>", self.trocar_tempo)
        self.root.bind("<Button-1>", self.teste)
        self.root.bind("<Button-2>", self.teste)
        self.root.bind("<Button-3>", self.teste)
        self.root.bind(
            "<Key>",
            lambda event: print(
                f"{event.char if event.char else event.keysym} teste de tecla"
            ),
        )

        self.pomodoro_time = 25
        self.short_break = 15
        self.long_break = 10

        self.root.title("Pomodoro Timer")
        self.root.geometry("300x200")

        self.time_var = tk.StringVar()
        self.remaining_time = self.__calculador_do_tempo(self.pomodoro_time)
        minutes, seconds = divmod(self.remaining_time, 60)
        self.time_var.set(f"{minutes:02}:{seconds:02}")

        self.__barra_de_menu()

        self.after_id = None
        self.running = False
        self.paused = False

        self.label = tk.Label(root, textvariable=self.time_var, font=("Helvetica", 48))
        self.label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=10)

    def teste(self, event) -> None:
        print(event)
        if (200 < event.x < 250) and (120 < event.y < 190):
            print(segredos())

    def __calculador_do_tempo(self, tempo) -> int:
        return tempo * 60

    def trocar_tempo(self, event) -> None:
        indice = self.notebook.index(self.notebook.select())

        print(event)

        estados = (
            EstadoPomodoro.POMODORO,
            EstadoPomodoro.SHORT_BREAK,
            EstadoPomodoro.LONG_BREAK,
        )

        self.estado = estados[indice]

        self.running = False

        match self.estado:
            case EstadoPomodoro.POMODORO:
                self.remaining_time = self.pomodoro_time * 60

            case EstadoPomodoro.SHORT_BREAK:
                self.remaining_time = self.short_break * 60

            case EstadoPomodoro.LONG_BREAK:
                self.remaining_time = self.long_break * 60

        self.atualizar_display()

    def atualizar_display(self):
        minutos, segundos = divmod(self.remaining_time, 60)
        self.time_var.set(f"{minutos:02}:{segundos:02}")

    def novo(self) -> None:
        print("ANODER")

    def abrir(self) -> None:
        print("KIBI SURDO")

    def __barra_de_menu(self) -> None:
        self.barra_menu = tk.Menu(self.root)
        self.__barra_de_menu_arquivo()
        self.__barra_de_menu_sair()
        self.root.config(menu=self.barra_menu)

    def __novo_aba(self, texto) -> None:
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=texto)

    def __barra_de_menu_arquivo(self) -> None:

        menu_arquivo = tk.Menu(self.barra_menu, tearoff=False)
        menu_arquivo.add_command(label="Novo", command=self.novo)
        menu_arquivo.add_command(label="Abrir", command=self.abrir)

        menu_arquivo.add_separator()
        menu_arquivo.add_command(
            label="Configuração", command=self.__janela_configuracao
        )

        # Submenu
        recentes = tk.Menu(menu_arquivo, tearoff=False)
        recentes.add_command(label="Projeto A")
        recentes.add_command(label="Projeto B")
        menu_arquivo.add_cascade(label="Recentes", menu=recentes)

        menu_arquivo.add_separator()

        menu_arquivo.add_command(label="Sair", command=self.root.destroy)
        self.barra_menu.add_cascade(label="Arquivo", menu=menu_arquivo)

        self.root.config(menu=self.barra_menu)

    def __barra_de_menu_sair(self) -> None:
        self.barra_menu.add_command(label="Sair", command=self.root.destroy)

    def __janela_configuracao(self) -> None:
        janela = tk.Toplevel(self.root)
        janela.title("Configurações")
        janela.geometry("300x200")

        tk.Label(janela, text="Pomodoro (minutos)").pack()
        entrada_pomodoro = tk.Entry(janela)
        entrada_pomodoro.insert(0, str(self.pomodoro_time))
        entrada_pomodoro.pack(pady=5)

        tk.Label(janela, text="Pausa curta (minutos)").pack()
        entrada_short = tk.Entry(janela)
        entrada_short.insert(0, str(self.short_break))
        entrada_short.pack(pady=5)

        tk.Label(janela, text="Pausa longa (minutos)").pack()
        entrada_long = tk.Entry(janela)
        entrada_long.insert(0, str(self.long_break))
        entrada_long.pack(pady=5)

        def salvar():
            try:
                work = int(entrada_pomodoro.get())
                short_break = int(entrada_short.get())
                long_break = int(entrada_long.get())

                if work <= 0 or short_break <= 0 or long_break <= 0:
                    raise ValueError

                self.pomodoro_time = work
                self.short_break = short_break
                self.long_break = long_break

                if not self.running:
                    print(self.running)
                    self.remaining_time = self.pomodoro_time * 60
                    self.atualizar_display()
                    print(self.remaining_time)
                    print(self.pomodoro_time)

                self.reset_timer()
                janela.destroy()

            except ValueError:
                tk.Label(
                    janela,
                    text="Digite apenas números inteiros maiores que zero.",
                    fg="red",
                ).pack()

        tk.Button(janela, text="Salvar", command=salvar).pack(pady=10)

    def update_time(self):
        if self.running:
            self.atualizar_display()
            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.after_id = self.root.after(1000, self.update_time)
            else:
                self.timer_finished()

    def start_timer(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.update_time()

    def pause_timer(self):
        if self.running:
            self.cancel_after()
            self.running = False
            self.paused = True

    def reset_timer(self):
        self.running = False
        self.paused = False
        self.remaining_time = self.pomodoro_time * 60
        self.atualizar_display()
        self.cancel_after()

    def timer_finished(self) -> None:
        self.running = False
        self.root.after(100, self.lock_screen)

    def start_break(self):

        self.running = False

        self.remaining_time = 5 * 60

        self.time_var.set("05:00")

        self.start_timer()

    def start_work(self):

        self.running = False

        self.remaining_time = 25 * 60

        self.time_var.set("25:00")

        self.start_timer()

    def lock_screen(self):
        if os.name == "nt":  # Windows
            self.cancel_after()
            ctypes.windll.user32.LockWorkStation()
            ctypes.windll.kernel32.Beep(800, 5000)
        elif os.name == "posix":  # macOS and Linux
            # This is a placeholder, as locking the screen in macOS/Linux typically requires different handling
            # For macOS, use: os.system('/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend')
            # For Linux, use: os.system('gnome-screensaver-command --lock')
            print("Locking screen on macOS/Linux is not implemented in this script.")

    def cancel_after(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None


def pomodoro() -> None:
    root = tk.Tk()
    PomodoroTimer(root)
    root.mainloop()
