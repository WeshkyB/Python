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
import socket

# Protokollierung
logging.basicConfig(filename="anti_monitor_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")


# Funktion 1: Überwachen von Prozessen
def monitor_processes(process_names):
    """Überwacht Prozesse und gibt Benachrichtigungen aus."""
    while True:
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                for process_name in process_names:
                    if process_name.lower() in proc.info['name'].lower():
                        logging.info(f"Prozess gestartet: {proc.info['name']} (PID: {proc.info['pid']})")
                        sg.popup(f"Prozess gestartet: {proc.info['name']} (PID: {proc.info['pid']})")
        except Exception as e:
            logging.error(f"Fehler beim Überwachen von Prozessen: {e}")
        time.sleep(5)


# Funktion 2: Dateiüberwachung
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
    except Exception as e:
        logging.error(f"Fehler bei der Dateiüberwachung: {e}")
    finally:
        observer.stop()
        observer.join()


# Funktion 3: Screenshot erstellen
def take_screenshot():
    """Erstellt regelmäßig Screenshots des Bildschirms."""
    while True:
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot = ImageGrab.grab()
            screenshot.save(f"screenshot_{timestamp}.png")
            logging.info(f"Screenshot erstellt: screenshot_{timestamp}.png")
        except Exception as e:
            logging.error(f"Fehler beim Erstellen eines Screenshots: {e}")
        time.sleep(10)


# Funktion 4: Tastatureingaben überwachen
def monitor_keyboard():
    """Überwacht Tastatureingaben."""
    while True:
        try:
            if keyboard.is_pressed('alt+tab'):
                logging.info("Tastenkombination Alt+Tab erkannt!")
                sg.popup("Tastenkombination Alt+Tab erkannt!")
        except Exception as e:
            logging.error(f"Fehler bei der Tastatureingabeüberwachung: {e}")
        time.sleep(0.5)


# Funktion 5: Netzwerküberwachung
def monitor_network():
    """Überwacht Netzwerkaktivität (Verbindungen)."""
    while True:
        try:
            connections = psutil.net_connections(kind='inet')
            for conn in connections:
                if conn.laddr and conn.raddr:
                    logging.info(f"Netzwerkverbindung: {conn.laddr} -> {conn.raddr}")
            time.sleep(5)
        except Exception as e:
            logging.error(f"Fehler bei der Netzwerküberwachung: {e}")


# Funktion 6: Standortüberwachung (Geofencing)
def monitor_location():
    """Überwacht den Standort anhand der IP-Adresse."""
    previous_ip = None
    while True:
        try:
            current_ip = socket.gethostbyname(socket.gethostname())
            if current_ip != previous_ip:
                logging.info(f"Standort geändert: Neue IP: {current_ip}")
                sg.popup(f"Standort geändert: Neue IP: {current_ip}")
                previous_ip = current_ip
        except Exception as e:
            logging.error(f"Fehler bei der Standortüberwachung: {e}")
        time.sleep(60)


# Haupt-GUI für Benutzersteuerung
def main_gui():
    """Startet die grafische Benutzeroberfläche."""
    sg.theme("DarkBlue")
    layout = [
        [sg.Text("Erweiterte Überwachung", font=("Helvetica", 16), justification="center")],
        [sg.Text("Prozesse (durch Komma getrennt):"), sg.InputText("vision", key="processes")],
        [sg.Text("Überwachter Ordner (Pfad):"), sg.InputText("C:\\Users\\User\\Documents", key="directory")],
        [sg.Button("Starten"), sg.Button("Beenden")]
    ]

    window = sg.Window("Erweiterte Überwachungssoftware", layout)
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

            # Screenshot-Erstellung starten
            thread_screenshot = threading.Thread(target=take_screenshot, daemon=True)
            threads.append(thread_screenshot)
            thread_screenshot.start()

            # Tastatureingaben überwachen
            thread_keyboard = threading.Thread(target=monitor_keyboard, daemon=True)
            threads.append(thread_keyboard)
            thread_keyboard.start()

            # Netzwerküberwachung starten
            thread_network = threading.Thread(target=monitor_network, daemon=True)
            threads.append(thread_network)
            thread_network.start()

            # Standortüberwachung starten
            thread_location = threading.Thread(target=monitor_location, daemon=True)
            threads.append(thread_location)
            thread_location.start()

            sg.popup("Überwachung gestartet!", title="Info")

    window.close()


if __name__ == "__main__":
    main_gui()import psutil
import threading
import time
import PySimpleGUI as sg
import logging
import keyboard
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import ImageGrab
import datetime
import socket

# Protokollierung
logging.basicConfig(filename="anti_monitor_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")


# Funktion 1: Überwachen von Prozessen
def monitor_processes(process_names):
    """Überwacht Prozesse und gibt Benachrichtigungen aus."""
    while True:
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                for process_name in process_names:
                    if process_name.lower() in proc.info['name'].lower():
                        logging.info(f"Prozess gestartet: {proc.info['name']} (PID: {proc.info['pid']})")
                        sg.popup(f"Prozess gestartet: {proc.info['name']} (PID: {proc.info['pid']})")
        except Exception as e:
            logging.error(f"Fehler beim Überwachen von Prozessen: {e}")
        time.sleep(5)


# Funktion 2: Dateiüberwachung
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
    except Exception as e:
        logging.error(f"Fehler bei der Dateiüberwachung: {e}")
    finally:
        observer.stop()
        observer.join()


# Funktion 3: Screenshot erstellen
def take_screenshot():
    """Erstellt regelmäßig Screenshots des Bildschirms."""
    while True:
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot = ImageGrab.grab()
            screenshot.save(f"screenshot_{timestamp}.png")
            logging.info(f"Screenshot erstellt: screenshot_{timestamp}.png")
        except Exception as e:
            logging.error(f"Fehler beim Erstellen eines Screenshots: {e}")
        time.sleep(10)


# Funktion 4: Tastatureingaben überwachen
def monitor_keyboard():
    """Überwacht Tastatureingaben."""
    while True:
        try:
            if keyboard.is_pressed('alt+tab'):
                logging.info("Tastenkombination Alt+Tab erkannt!")
                sg.popup("Tastenkombination Alt+Tab erkannt!")
        except Exception as e:
            logging.error(f"Fehler bei der Tastatureingabeüberwachung: {e}")
        time.sleep(0.5)


# Funktion 5: Netzwerküberwachung
def monitor_network():
    """Überwacht Netzwerkaktivität (Verbindungen)."""
    while True:
        try:
            connections = psutil.net_connections(kind='inet')
            for conn in connections:
                if conn.laddr and conn.raddr:
                    logging.info(f"Netzwerkverbindung: {conn.laddr} -> {conn.raddr}")
            time.sleep(5)
        except Exception as e:
            logging.error(f"Fehler bei der Netzwerküberwachung: {e}")


# Funktion 6: Standortüberwachung (Geofencing)
def monitor_location():
    """Überwacht den Standort anhand der IP-Adresse."""
    previous_ip = None
    while True:
        try:
            current_ip = socket.gethostbyname(socket.gethostname())
            if current_ip != previous_ip:
                logging.info(f"Standort geändert: Neue IP: {current_ip}")
                sg.popup(f"Standort geändert: Neue IP: {current_ip}")
                previous_ip = current_ip
        except Exception as e:
            logging.error(f"Fehler bei der Standortüberwachung: {e}")
        time.sleep(60)


# Haupt-GUI für Benutzersteuerung
def main_gui():
    """Startet die grafische Benutzeroberfläche."""
    sg.theme("DarkBlue")
    layout = [
        [sg.Text("Erweiterte Überwachung", font=("Helvetica", 16), justification="center")],
        [sg.Text("Prozesse (durch Komma getrennt):"), sg.InputText("vision", key="processes")],
        [sg.Text("Überwachter Ordner (Pfad):"), sg.InputText("C:\\Users\\User\\Documents", key="directory")],
        [sg.Button("Starten"), sg.Button("Beenden")]
    ]

    window = sg.Window("Erweiterte Überwachungssoftware", layout)
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

            # Screenshot-Erstellung starten
            thread_screenshot = threading.Thread(target=take_screenshot, daemon=True)
            threads.append(thread_screenshot)
            thread_screenshot.start()

            # Tastatureingaben überwachen
            thread_keyboard = threading.Thread(target=monitor_keyboard, daemon=True)
            threads.append(thread_keyboard)
            thread_keyboard.start()

            # Netzwerküberwachung starten
            thread_network = threading.Thread(target=monitor_network, daemon=True)
            threads.append(thread_network)
            thread_network.start()

            # Standortüberwachung starten
            thread_location = threading.Thread(target=monitor_location, daemon=True)
            threads.append(thread_location)
            thread_location.start()

            sg.popup("Überwachung gestartet!", title="Info")

    window.close()


if __name__ == "__main__":
    main_gui() 
