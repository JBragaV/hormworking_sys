from pathlib import Path

from windows_toasts import (
    AudioSource,
    InteractableWindowsToaster,
    Toast,
    ToastAudio,
    ToastButton,
    ToastDisplayImage,
    ToastDuration,
    ToastImage,
    ToastScenario,
    WindowsToaster,
)

BASE_PATH = Path(__file__).parent


class NotificacaoWindows:
    def __init__(self) -> None:
        print("__init__")
        self.__actions = {
            "break": self.start_break,
            "restart": self.restart_pomodoro,
            "skip": self.skip_break,
        }
        self.n = WindowsToaster("Python")

    def set_controller(self, controller):
        self.controller = controller

    def on_activated(self, event):
        match event.arguments:
            case "restart":
                self.controller.reset_timer()
                self.controller.start_timer()

            case "break":
                self.controller.start_break()

    def start_break(self):
        print("Iniciando pausa")

    def restart_pomodoro(self):
        print("Reiniciando Pomodoro")

    def skip_break(self):
        print("Pulando pausa")

    def pomodoro_notification(self) -> None:
        toast = Toast()
        toast.duration = ToastDuration.Long
        toast.text_fields = [
            "🍅 Pomodoro finalizado",
            "Hora de fazer uma pausa de 5 minutos.",
        ]
        toast.on_activated = lambda _: print("Toast clicked!")
        self.n.show_toast(toast)

    def scenario_notification(self) -> None:
        toast = Toast()
        toast.duration = ToastDuration.Long
        toast.text_fields = ["⏰ Hora da pausa", "Levante, beba água e descanse."]
        toast.scenario = ToastScenario.Reminder

        self.n.show_toast(toast)

    def notification_with_button(self) -> None:
        toast = Toast()
        toast.duration = ToastDuration.Long
        toast.text_fields = ["Pomodoro concluído", "O que deseja fazer?"]

        toast.AddAction(ToastButton(content="☕ Pausa", arguments="break"))

        toast.AddAction(ToastButton(content="▶ Novo ciclo", arguments="restart"))

        def activated(argument):
            print(argument.arguments)

        toast.on_activated = activated

        self.n.show_toast(toast)

    def notification_with_image(self) -> None:
        print("Tem imagem aqui")
        toast = Toast()
        toast.duration = ToastDuration.Long
        img_path = BASE_PATH / "img" / "python_2000x2000.jpeg"

        toast.text_fields = ["Pomodoro", "Excelente trabalho!"]

        toast.AddImage(ToastDisplayImage(ToastImage(str(img_path))))
        self.n.show_toast(toast)

    def notification_with_sound(self) -> None:
        print("Tem som aqui")
        toast = Toast()
        toast.duration = ToastDuration.Long
        toast.audio = ToastAudio(AudioSource.Reminder)
        self.n.show_toast(toast)

    def notification_with_another_sound(self) -> None:
        print("Tem som denovo aqui")
        toast = Toast()
        toast.duration = ToastDuration.Long
        toast.audio = ToastAudio(AudioSource.Alarm10)
        self.n.show_toast(toast)

    def notification_all_together(self) -> None:
        n = InteractableWindowsToaster("Pomodoro")
        toast = Toast()
        toast.duration = ToastDuration.Long
        toast.text_fields = ["🍅 Pomodoro encerrado", "25 minutos concluídos."]

        toast.duration = ToastDuration.Long
        toast.scenario = ToastScenario.Reminder

        toast.AddAction(ToastButton(content="☕ Pausa", arguments="break"))
        toast.AddAction(ToastButton(content="▶ Novo ciclo", arguments="restart"))

        toast.audio = ToastAudio(AudioSource.Reminder)

        toast.on_activated = self.on_activated

        n.show_toast(toast)
