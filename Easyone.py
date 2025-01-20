import os
import psutil
import threading
import time
import PySimpleGUI as sg
import logging
import keyboard  
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import ImageGrab
import datetime

logging.basicConfig(
    filename="anti_monitor_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

def monitor_processes(process_names):
    """Überwacht Prozesse und gibt Benachrichtigungen aus."""
    while True:
        for proc in psutil.process_iter(['pid', 'name']):
            for process_name in process_names:
                if process_name.lower() in proc.info['name'].lower():
                    logging.info(f"Prozess gestartet: {proc.info['name']} (PID: {proc.info['pid']})")
                    sg.popup(f"Prozess gestartet: {proc.info['name']} (PID: {proc.info['pid']})")
        time.sleep(5)

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        logging.info(f"Datei geändert: {event.src_path}")
        sg.popup(f"Datei geändert: {event.src_path}")

def monitor_files(directory_to_watch):
    """Überwacht einen Ordner auf Änderungen."""
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def monitor_keyboard():
    """Überwacht Tastatureingaben."""
    while True:
        if keyboard.is_pressed('alt+tab'): 
            logging.info("Tastenkombination Alt+Tab erkannt!")
            sg.popup("Tastenkombination Alt+Tab erkannt!")
        time.sleep(0.5)

def take_screenshot():
    """Erstellt regelmäßig Screenshots des Bildschirms."""
    while True:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot = ImageGrab.grab()
        screenshot.save(f"screenshot_{timestamp}.png")
        logging.info(f"Screenshot erstellt: screenshot_{timestamp}.png")
        time.sleep(10) 

def prevent_window_switch():
    """Verhindert den Wechsel zwischen Fenstern durch Alt+Tab."""
    while True:
        if keyboard.is_pressed('alt+tab'):
            keyboard.block_key('tab')  # Verhindert das Drücken von Tab
        time.sleep(0.1)

# GUI für Benutzersteuerung
def main_gui():
    """Startet die grafische Benutzeroberfläche."""
    sg.theme("DarkBlue")
    layout = [
        [sg.Text("Anti-Überwachungsprogramm", font=("Helvetica", 16), justification="center")],
        [sg.Text("Prozesse (durch Komma getrennt):"), sg.InputText("vision", key="processes")],
        [sg.Text("Überwachter Ordner (Pfad):"), sg.InputText("C:\\Users\\User\\Documents", key="directory")],
        [sg.Button("Starten"), sg.Button("Beenden")]
    ]

    window = sg.Window("Anti-Überwachungsprogramm", layout)

    threads = []

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WINDOW_CLOSED or event == "Beenden":
            for thread in threads:
                if thread.is_alive():
                    thread.join(1)
            break

        if event == "Starten":
            # Prozesse überwachen
            process_list = [p.strip() for p in values["processes"].split(",") if p.strip()]
            thread_process = threading.Thread(target=monitor_processes, args=(process_list,), daemon=True)
            threads.append(thread_process)
            thread_process.start()

            # Dateiüberwachung starten
            directory_to_watch = values["directory"]
            thread_file_monitor = threading.Thread(target=monitor_files, args=(directory_to_watch,), daemon=True)
            threads.append(thread_file_monitor)
            thread_file_monitor.start()

            # Tastatureingaben überwachen
            thread_keyboard = threading.Thread(target=monitor_keyboard, daemon=True)
            threads.append(thread_keyboard)
            thread_keyboard.start()

            # Screenshot-Erstellung starten
            thread_screenshot = threading.Thread(target=take_screenshot, daemon=True)
            threads.append(thread_screenshot)
            thread_screenshot.start()

            # Fensterwechsel verhindern
            thread_window_switch = threading.Thread(target=prevent_window_switch, daemon=True)
            threads.append(thread_window_switch)
            thread_window_switch.start()

            sg.popup("Überwachung gestartet!", title="Info")

    window.close()

if __name__ == "__main__":
    main_gui()
