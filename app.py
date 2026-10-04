#!/usr/bin/env python3
"""
Display Brightness Manager (Twinkle Tray for Linux)
Multi-monitor brightness controller with true DDC/CI hardware control for external monitors
and native hardware backlight control for laptop displays (preserving Night Light).
"""

import os
import re
import sys
import time
import subprocess
import threading
import tkinter as tk
from tkinter import ttk

# Colors - Modern Dark Theme with Warm Amber Accents
BG_COLOR = "#181825"
CARD_BG = "#1e1e2e"
CARD_BORDER = "#313244"
TEXT_PRIMARY = "#cdd6f4"
TEXT_MUTED = "#a6adc8"
ACCENT_AMBER = "#ffb703"
ACCENT_GOLD = "#ffd166"
ACCENT_GREEN = "#a6e3a1"
ACCENT_CYAN = "#89dceb"
ACCENT_RED = "#f38ba8"
SLIDER_TROUGH = "#313244"

# 64x64 PNG App Icon encoded in base64
APP_ICON_B64 = """
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
"""


class HardwareWorker:
    """Thread-safe, debounced executor for ddcutil hardware commands."""

    def __init__(self):
        self.lock = threading.Lock()
        self.pending_val = None
        self.is_running = False
        self.last_applied = None

    def request_set_brightness(self, value):
        with self.lock:
            self.pending_val = value
            if not self.is_running:
                self.is_running = True
                threading.Thread(target=self._run_loop, daemon=True).start()

    def _run_loop(self):
        while True:
            target = None
            with self.lock:
                if self.pending_val is not None:
                    target = self.pending_val
                    self.pending_val = None
                else:
                    self.is_running = False
                    return

            if target is not None and target != self.last_applied:
                try:
                    subprocess.run(
                        ["ddcutil", "setvcp", "10", str(target), "--brief"],
                        capture_output=True,
                        text=True,
                        timeout=3.0,
                    )
                    self.last_applied = target
                except Exception as e:
                    print("DDC/CI error:", e)

            time.sleep(0.08)  # 80ms throttle to protect I2C bus


class DisplayCard(tk.Frame):
    """Card widget representing a single display with a brightness slider."""

    def __init__(
        self,
        parent,
        display_name,
        subtitle,
        initial_val=50,
        on_change=None,
        is_external=False,
    ):
        super().__init__(
            parent,
            bg=CARD_BG,
            highlightbackground=CARD_BORDER,
            highlightthickness=1,
            padx=18,
            pady=16,
        )
        self.on_change = on_change
        self.current_val = initial_val
        self.is_external = is_external

        # Title Row
        title_row = tk.Frame(self, bg=CARD_BG)
        title_row.pack(fill="x")

        disp_icon = "🖥️" if is_external else "💻"
        name_lbl = tk.Label(
            title_row,
            text=f"{disp_icon}  {display_name}",
            font=("Ubuntu", 12, "bold"),
            fg=TEXT_PRIMARY,
            bg=CARD_BG,
        )
        name_lbl.pack(side="left")

        self.val_label = tk.Label(
            title_row,
            text=f"{initial_val}%",
            font=("Ubuntu", 14, "bold"),
            fg=ACCENT_AMBER,
            bg=CARD_BG,
        )
        self.val_label.pack(side="right")

        # Subtitle
        sub_lbl = tk.Label(
            self, text=subtitle, font=("Ubuntu", 9), fg=TEXT_MUTED, bg=CARD_BG
        )
        sub_lbl.pack(anchor="w", pady=(2, 10))

        # Slider + Sun Icons Row
        slider_row = tk.Frame(self, bg=CARD_BG)
        slider_row.pack(fill="x")

        sun_min = tk.Label(
            slider_row, text="🌑 0", font=("Ubuntu", 9), fg=TEXT_MUTED, bg=CARD_BG
        )
        sun_min.pack(side="left")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Amber.Horizontal.TScale",
            troughcolor=SLIDER_TROUGH,
            background=ACCENT_AMBER,
            sliderthickness=18,
            sliderrelief="flat",
        )

        self.scale = ttk.Scale(
            slider_row,
            from_=0,
            to=100,
            orient="horizontal",
            style="Amber.Horizontal.TScale",
            command=self._on_slider_move,
        )
        self.scale.set(initial_val)
        self.scale.pack(side="left", fill="x", expand=True, padx=10)

        sun_max = tk.Label(
            slider_row, text="100 ☀️", font=("Ubuntu", 9), fg=TEXT_MUTED, bg=CARD_BG
        )
        sun_max.pack(side="right")

    def _on_slider_move(self, val_str):
        val = int(round(float(val_str)))
        if val != self.current_val:
            self.current_val = val
            self.val_label.config(text=f"{val}%")
            if self.on_change:
                self.on_change(val)

    def set_value(self, val, trigger_callback=True):
        val = max(0, min(100, int(round(val))))
        self.current_val = val
        self.scale.set(val)
        self.val_label.config(text=f"{val}%")
        if trigger_callback and self.on_change:
            self.on_change(val)


class BrightnessApp(tk.Tk):
    def __init__(self):
        super().__init__(className="display-brightness-manager")

        self.title("Display Brightness Manager")
        # Wider geometry (490px) to prevent button clipping
        self.geometry("490x560")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)

        self._load_icon()

        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (490 // 2)
        y = (self.winfo_screenheight() // 2) - (560 // 2)
        self.geometry(f"+{x}+{y}")

        self.hardware_worker = HardwareWorker()
        self.link_displays = tk.BooleanVar(value=False)
        self.is_syncing = False

        self._build_ui()

        # Initial read from hardware in background
        threading.Thread(target=self._initial_hardware_read, daemon=True).start()

    def _load_icon(self):
        try:
            self.app_icon = tk.PhotoImage(data=APP_ICON_B64.strip())
            self.iconphoto(True, self.app_icon)
        except Exception as e:
            print("Could not set app icon:", e)

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=BG_COLOR, pady=16)
        header.pack(fill="x", padx=24)

        title_lbl = tk.Label(
            header,
            text="Display Brightness",
            font=("Ubuntu", 17, "bold"),
            fg=TEXT_PRIMARY,
            bg=BG_COLOR,
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            header,
            text="Multi-Monitor Hardware Backlight (Night Light Safe)",
            font=("Ubuntu", 9),
            fg=TEXT_MUTED,
            bg=BG_COLOR,
        )
        sub_lbl.pack(anchor="w")

        # External Monitor Card (HP Z27n)
        self.hp_card = DisplayCard(
            self,
            display_name="HP Z27n IPS Display",
            subtitle="External Monitor (HDMI-1 • 2560x1440 • DDC/CI)",
            initial_val=4,
            on_change=self._on_hp_change,
            is_external=True,
        )
        self.hp_card.pack(fill="x", padx=24, pady=8)

        # Internal Laptop Display Card
        self.laptop_card = DisplayCard(
            self,
            display_name="Laptop Built-in Screen",
            subtitle="Internal Display (eDP-1 • Hardware LEDs • Night Light Safe)",
            initial_val=50,
            on_change=self._on_laptop_change,
            is_external=False,
        )
        self.laptop_card.pack(fill="x", padx=24, pady=8)

        # Presets Bar
        presets_frame = tk.Frame(self, bg=BG_COLOR)
        presets_frame.pack(fill="x", padx=24, pady=(12, 6))

        presets_title = tk.Label(
            presets_frame,
            text="Presets:",
            font=("Ubuntu", 9, "bold"),
            fg=TEXT_MUTED,
            bg=BG_COLOR,
        )
        presets_title.pack(side="left", padx=(0, 6))

        presets = [
            ("🌙 Night (4%)", 4),
            ("🛋️ Cozy (25%)", 25),
            ("💼 Work (50%)", 50),
            ("☀️ Max (100%)", 100),
        ]

        for label, p_val in presets:
            btn = tk.Button(
                presets_frame,
                text=label,
                font=("Ubuntu", 8, "bold"),
                fg=TEXT_PRIMARY,
                bg=CARD_BG,
                activebackground=CARD_BORDER,
                activeforeground=TEXT_PRIMARY,
                relief="flat",
                bd=0,
                padx=9,
                pady=5,
                cursor="hand2",
                command=lambda v=p_val: self.apply_preset(v),
            )
            btn.pack(side="left", padx=3)

        # Bottom Bar: Sync Link Checkbox & Status
        bottom_bar = tk.Frame(self, bg=BG_COLOR)
        bottom_bar.pack(fill="x", padx=24, pady=(16, 16), side="bottom")

        link_chk = tk.Checkbutton(
            bottom_bar,
            text="🔗 Link All Displays",
            variable=self.link_displays,
            font=("Ubuntu", 9),
            fg=TEXT_PRIMARY,
            bg=BG_COLOR,
            selectcolor=CARD_BG,
            activebackground=BG_COLOR,
            activeforeground=TEXT_PRIMARY,
            cursor="hand2",
        )
        link_chk.pack(side="left")

        self.status_msg = tk.Label(
            bottom_bar,
            text="Connecting to displays...",
            font=("Ubuntu", 9),
            fg=ACCENT_CYAN,
            bg=BG_COLOR,
        )
        self.status_msg.pack(side="right")

    def _initial_hardware_read(self):
        # 1. Read HP Z27n via ddcutil
        try:
            res = subprocess.run(
                ["ddcutil", "getvcp", "10", "--brief"],
                capture_output=True,
                text=True,
                timeout=4.0,
            )
            m = re.search(r"VCP\s+10\s+[A-Za-z]\s+(\d+)", res.stdout)
            if m:
                hp_val = int(m.group(1))
                self.after(0, lambda: self.hp_card.set_value(hp_val, False))
        except Exception as e:
            print("Error reading HP brightness:", e)

        # 2. Read Laptop Backlight directly from sysfs
        try:
            bl_path = "/sys/class/backlight/intel_backlight"
            if os.path.exists(os.path.join(bl_path, "brightness")):
                with open(os.path.join(bl_path, "brightness"), "r") as f:
                    cur = int(f.read().strip())
                with open(os.path.join(bl_path, "max_brightness"), "r") as f:
                    mx = int(f.read().strip())
                lap_val = int(round((cur / mx) * 100))
                self.after(0, lambda: self.laptop_card.set_value(lap_val, False))
        except Exception as e:
            print("Error reading laptop backlight:", e)

        self.after(
            0,
            lambda: self.status_msg.config(text="✓ Hardware Ready", fg=ACCENT_GREEN),
        )

    def _on_hp_change(self, val):
        self.status_msg.config(text=f"HP Z27n: {val}%", fg=ACCENT_AMBER)
        self.hardware_worker.request_set_brightness(val)

        if self.link_displays.get() and not self.is_syncing:
            self.is_syncing = True
            self.laptop_card.set_value(val, True)
            self.is_syncing = False

    def _on_laptop_change(self, val):
        self.status_msg.config(text=f"Laptop: {val}%", fg=ACCENT_AMBER)
        threading.Thread(target=self._apply_laptop_hardware_brightness, args=(val,), daemon=True).start()

        if self.link_displays.get() and not self.is_syncing:
            self.is_syncing = True
            self.hp_card.set_value(val, True)
            self.is_syncing = False

    def _apply_laptop_hardware_brightness(self, val):
        """Controls physical laptop backlight LEDs via brightnessctl (preserves Night Light 100%)."""
        val = max(0, min(100, int(round(val))))
        
        # 1. Primary: brightnessctl (Direct hardware LED backlight, zero gamma interference)
        try:
            res = subprocess.run(
                ["brightnessctl", "set", f"{val}%"],
                capture_output=True,
                text=True,
            )
            if res.returncode == 0:
                return
        except Exception:
            pass

        # 2. Secondary: Cinnamon Power DBus Interface
        try:
            res = subprocess.run(
                [
                    "gdbus", "call", "--session",
                    "--dest", "org.cinnamon.SettingsDaemon.Power",
                    "--object-path", "/org/cinnamon/SettingsDaemon/Power",
                    "--method", "org.cinnamon.SettingsDaemon.Power.Screen.SetPercentage",
                    str(val)
                ],
                capture_output=True,
                text=True,
            )
            if res.returncode == 0:
                return
        except Exception:
            pass

    def apply_preset(self, val):
        self.hp_card.set_value(val, True)
        self.laptop_card.set_value(val, True)
        self.status_msg.config(text=f"Preset: {val}%", fg=ACCENT_GREEN)
        self.after(2000, lambda: self.status_msg.config(text="✓ Ready", fg=ACCENT_GREEN))


if __name__ == "__main__":
    app = BrightnessApp()
    app.mainloop()
