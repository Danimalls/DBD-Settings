import os, sys, shutil
from tkinter import messagebox, ttk
import tkinter as tk


def main():
    def set_write(*args):
        for arg in args:
            os.chmod(arg, 0o666)

    def set_read(*args):
        for arg in args:
            os.chmod(arg, 0o444)

    window = tk.Tk()
    window.withdraw()

    engineini_steam = os.path.expandvars("%localappdata%\\DeadByDaylight\\Saved\\Config\\WindowsNoEditor\\Engine.ini")
    gameUserSettingsini_steam = os.path.expandvars("%localappdata%\\DeadByDaylight\\Saved\\Config\\WindowsNoEditor\\GameUserSettings.ini")
    engineini_steam_backup = os.path.expandvars("%localappdata%\\DeadByDaylight\\Saved\\Config\\WindowsNoEditor\\Backup\\Engine.ini")
    gameUserSettingsini_steam_backup = os.path.expandvars("%localappdata%\\DeadByDaylight\\Saved\\Config\\WindowsNoEditor\\Backup\\GameUserSettings.ini")

    engineini_epic = os.path.expandvars("%localappdata%\\DeadByDaylight\\Saved\\Config\\EGS\\Engine.ini")
    gameUserSettingsini_epic = os.path.expandvars("%localappdata%\\DeadByDaylight\\Saved\\Config\\EGS\\GameUserSettings.ini")
    engineini_epic_backup = os.path.expandvars("%localappdata%\\DeadByDaylight\\Saved\\Config\\EGS\\Backup\\Engine.ini")
    gameUserSettingsini_epic_backup = os.path.expandvars("%localappdata%\\DeadByDaylight\\Saved\\Config\\EGS\\Backup\\GameUserSettings.ini")

    if os.path.exists(engineini_steam):
        engineini_file = engineini_steam
        gameUserSettingsini_file = gameUserSettingsini_steam
        engineini_backup = engineini_steam_backup
        gameUserSettingsini_backup = gameUserSettingsini_steam_backup
    else:
        engineini_file = engineini_epic
        gameUserSettingsini_file = gameUserSettingsini_epic
        engineini_backup = engineini_epic_backup
        gameUserSettingsini_backup = gameUserSettingsini_epic_backup
    backup_dir = os.path.dirname(engineini_backup)

    set_write(engineini_file, gameUserSettingsini_file)

    if os.path.exists(backup_dir):
        pass
    else:
        os.makedirs(backup_dir, exist_ok=True)
        shutil.copyfile(engineini_file, engineini_backup)
        shutil.copyfile(gameUserSettingsini_file, gameUserSettingsini_backup)
        os.chmod(engineini_backup, 0o444)
        os.chmod(gameUserSettingsini_backup, 0o444)

    engine_file_text = "[/Script/Engine.InputSettings]\nbEnableMouseSmoothing=False\nbDisableMouseAcceleration=True\n\n[/script/engine.engine]\nbSmoothFrameRate=false\nMinSmoothedFrameRate=5\nMaxSmoothedFrameRate=144"
    with open(engineini_steam, "r+") as engine_file:
        file_contents = engine_file.read()
        if engine_file_text in file_contents:
            messagebox.showinfo("Information", "Your engine.ini file already contains the required settings.")
        else:
            engine_file.write(f"{engine_file_text}")
            messagebox.showinfo("Information", "Engine.ini file has been updated!")

    def save_settings():
        settings = get_settings()

        with open(gameUserSettingsini_steam, "r") as file:
            original_contents = file.read()

        updated_contents = ""
        sections = original_contents.split("\n\n")
        for section in sections:
            lines = section.strip().split("\n")
            if lines:
                section_header = lines[0]
                updated_contents += section_header + "\n"
                for line in lines[1:]:
                    try:
                        key, old_value = line.split("=", 1)
                        if key in entries:
                            updated_contents += f"{key}={entries[key].get()}\n"
                        else:
                            updated_contents += line + "\n"
                    except ValueError:
                        pass
                updated_contents += "\n"

        updated_contents = updated_contents.rstrip("\n") + "\n\n"

        try:
            with open(gameUserSettingsini_steam, "w") as file:
                file.write(updated_contents)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def exit_program():
        set_read(engineini_file, gameUserSettingsini_file)
        window.destroy()
        new_window.destroy()
        sys.exit(0)

    def get_settings():
        settings = ""
        for key, value in entries.items():
            settings += f"{key}={value.get()}\n"
        return settings

    new_window = tk.Tk()
    new_window.title("Settings GUI")

    canvas = tk.Canvas(new_window)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    frame = tk.Frame(canvas)
    frame.pack(fill="both", expand=True)

    canvas.create_window((0, 0), window=frame, anchor="nw")

    entries = {}

    with open(gameUserSettingsini_steam, "r") as file:
        user_settings_contents = file.read()

    sections = user_settings_contents.split("\n\n")
    for section in sections:
        lines = section.strip().split("\n")
        if lines:
            for line in lines:
                try:
                    key, value = line.split("=", 1)
                    sub_frame = tk.Frame(frame)
                    sub_frame.pack(anchor="w")
                    label = tk.Label(sub_frame, text=key)
                    label.pack(side="left")
                    entry = tk.Entry(sub_frame, width=40)
                    entry.pack(side="left")
                    entry.insert(tk.END, value)
                    entries[key] = entry
                except ValueError:
                    pass

    def revert_settings():
        shutil.copyfile(engineini_backup, engineini_file)
        shutil.copyfile(gameUserSettingsini_backup, gameUserSettingsini_file)
        messagebox.showinfo("Information", "Program will exit and revert back to original settings")
        exit_program()

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        new_window.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    frame.bind("<Configure>", on_configure)
    canvas.bind_all("<MouseWheel>", on_configure)

    def on_save_enter(event):
        save_button.config(bg="#D9D9D9", fg="#000000")

    def on_save_leave(event):
        save_button.config(bg=new_window.cget("bg"), fg="#000000")

    save_button = tk.Button(new_window, text="Save", command=save_settings)
    save_button.pack(pady=10)
    save_button.bind("<Enter>", on_save_enter)
    save_button.bind("<Leave>", on_save_leave)

    def on_exit_enter(event):
        exit_button.config(bg="#D9D9D9", fg="#000000")

    def on_exit_leave(event):
        exit_button.config(bg=new_window.cget("bg"), fg="#000000")

    exit_button = tk.Button(new_window, text="Exit", command=exit_program)
    exit_button.pack(pady=10)
    exit_button.bind("<Enter>", on_exit_enter)
    exit_button.bind("<Leave>", on_exit_leave)

    def on_revert_enter(event):
        revert_button.config(bg="#D9D9D9", fg="#000000")

    def on_revert_leave(event):
        revert_button.config(bg=new_window.cget("bg"), fg="#000000")

    revert_button = tk.Button(new_window, text="Revert settings to default", command=revert_settings)
    revert_button.pack(pady=10)
    revert_button.bind("<Enter>", on_revert_enter)
    revert_button.bind("<Leave>", on_revert_leave)

    legend_frame = tk.Frame(new_window)
    legend_frame.pack(pady=10)

    legend_label = tk.Label(legend_frame, text="Scalability group (sg) settings legend")
    legend_label.pack()

    legend_info = [
        ("0", "Low"),
        ("1", "Medium"),
        ("2", "High"),
        ("3", "Not sure (seems identical to 4)"),
        ("4", "Ultra")
    ]

    for key, value in legend_info:
        legend_row = tk.Frame(legend_frame)
        legend_row.pack(anchor="w")
        key_label = tk.Label(legend_row, text=f"{key} =")
        key_label.pack(side="left")
        value_label = tk.Label(legend_row, text=value)
        value_label.pack(side="left")

    # Calculate the center coordinates of the screen
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    window_width = 800  # Set your desired window width
    window_height = 600  # Set your desired window height
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the window's size and position
    new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    new_window.protocol("WM_DELETE_WINDOW", exit_program)

    new_window.mainloop()

if __name__ == "__main__":
    main()
