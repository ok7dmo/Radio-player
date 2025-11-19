#!/usr/bin/env python3
"""
FT-897 Memory Manager - Tkinter GUI (Windows Compatible)
=========================================================

Lightweight GUI using Tkinter (included with Python) - no installation needed!
Works on Windows, macOS, and Linux out of the box.

Author: Claude AI
Date: 2025-11-19
License: MIT
"""

import sys
import os
from typing import Optional, List
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

from ft897_memory import (
    FT897Image, FT897Channel, MODE_NAMES, MODE_VALUES,
    DUPLEX_NAMES, DUPLEX_VALUES, MODE_PKT, MODE_FM
)


class ChannelEditorWindow(tk.Toplevel):
    """Window for editing a single channel"""

    def __init__(self, parent, channel: FT897Channel):
        super().__init__(parent)
        self.channel = channel
        self.result = None

        self.title(f"Edit Channel {channel.index}")
        self.geometry("400x500")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()

        self.setup_ui()
        self.load_channel_data()

        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def setup_ui(self):
        """Setup the UI"""
        # Main frame with padding
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frequency section
        freq_frame = ttk.LabelFrame(main_frame, text="Frequency", padding="5")
        freq_frame.pack(fill=tk.X, pady=5)

        ttk.Label(freq_frame, text="MHz:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.freq_mhz = tk.StringVar()
        ttk.Entry(freq_frame, textvariable=self.freq_mhz, width=15).grid(row=0, column=1, padx=5)

        ttk.Label(freq_frame, text="kHz (fine):").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.freq_khz = tk.StringVar()
        ttk.Entry(freq_frame, textvariable=self.freq_khz, width=15).grid(row=1, column=1, padx=5)

        # Mode section
        mode_frame = ttk.LabelFrame(main_frame, text="Mode & Duplex", padding="5")
        mode_frame.pack(fill=tk.X, pady=5)

        ttk.Label(mode_frame, text="Mode:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.mode_var = tk.StringVar()
        mode_combo = ttk.Combobox(mode_frame, textvariable=self.mode_var, state="readonly", width=12)
        mode_combo['values'] = list(MODE_NAMES.values())
        mode_combo.grid(row=0, column=1, padx=5, sticky=tk.W)

        ttk.Label(mode_frame, text="Duplex:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.duplex_var = tk.StringVar()
        duplex_combo = ttk.Combobox(mode_frame, textvariable=self.duplex_var, state="readonly", width=12)
        duplex_combo['values'] = list(DUPLEX_NAMES.values())
        duplex_combo.grid(row=1, column=1, padx=5, sticky=tk.W)

        # Offset
        ttk.Label(mode_frame, text="Offset (kHz):").grid(row=2, column=0, sticky=tk.W, padx=5)
        self.offset_var = tk.StringVar()
        ttk.Entry(mode_frame, textvariable=self.offset_var, width=15).grid(row=2, column=1, padx=5)

        # Name
        name_frame = ttk.LabelFrame(main_frame, text="Channel Name", padding="5")
        name_frame.pack(fill=tk.X, pady=5)

        ttk.Label(name_frame, text="Name (8 chars):").pack(side=tk.LEFT, padx=5)
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var, width=20)
        name_entry.pack(side=tk.LEFT, padx=5)

        # Flags
        flags_frame = ttk.LabelFrame(main_frame, text="Flags", padding="5")
        flags_frame.pack(fill=tk.X, pady=5)

        self.skip_var = tk.BooleanVar()
        ttk.Checkbutton(flags_frame, text="Skip in scan", variable=self.skip_var).pack(anchor=tk.W)

        self.ipo_var = tk.BooleanVar()
        ttk.Checkbutton(flags_frame, text="IPO (Pre-amp OFF)", variable=self.ipo_var).pack(anchor=tk.W)

        self.att_var = tk.BooleanVar()
        ttk.Checkbutton(flags_frame, text="Attenuator", variable=self.att_var).pack(anchor=tk.W)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="OK", command=self.on_ok, width=10).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel, width=10).pack(side=tk.RIGHT)

    def load_channel_data(self):
        """Load channel data into widgets"""
        freq_mhz = int(self.channel.frequency / 1_000_000)
        freq_khz = int((self.channel.frequency % 1_000_000) / 1000)

        self.freq_mhz.set(str(freq_mhz))
        self.freq_khz.set(str(freq_khz))
        self.mode_var.set(MODE_NAMES[self.channel.mode])
        self.duplex_var.set(DUPLEX_NAMES[self.channel.duplex])
        self.offset_var.set(str(int(self.channel.offset / 1000)))
        self.name_var.set(self.channel.name)
        self.skip_var.set(self.channel.skip)
        self.ipo_var.set(self.channel.ipo)
        self.att_var.set(self.channel.att)

    def on_ok(self):
        """Handle OK button"""
        try:
            # Validate and update channel
            freq_hz = (int(self.freq_mhz.get()) * 1_000_000) + (int(self.freq_khz.get()) * 1000)
            self.channel.frequency = freq_hz
            self.channel.mode = MODE_VALUES[self.mode_var.get()]
            self.channel.duplex = DUPLEX_VALUES[self.duplex_var.get()]
            self.channel.offset = int(self.offset_var.get()) * 1000
            self.channel.name = self.name_var.get()[:8]  # Max 8 chars
            self.channel.skip = self.skip_var.get()
            self.channel.ipo = self.ipo_var.get()
            self.channel.att = self.att_var.get()
            self.channel._update_raw_data()

            self.result = self.channel
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input:\n{str(e)}")

    def on_cancel(self):
        """Handle Cancel button"""
        self.result = None
        self.destroy()


class StatisticsWindow(tk.Toplevel):
    """Window showing image statistics"""

    def __init__(self, parent, image: FT897Image):
        super().__init__(parent)
        self.image = image

        self.title("Image Statistics")
        self.geometry("700x600")

        self.setup_ui()
        self.update_statistics()

        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def setup_ui(self):
        """Setup the UI"""
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Text widget with scrollbar
        self.text = scrolledtext.ScrolledText(main_frame, width=80, height=30, font=("Courier", 10))
        self.text.pack(fill=tk.BOTH, expand=True)

        # Close button
        ttk.Button(main_frame, text="Close", command=self.destroy, width=10).pack(pady=10)

    def update_statistics(self):
        """Update statistics display"""
        stats = self.image.get_statistics()

        text = "=" * 60 + "\n"
        text += "FT-897 Image Statistics\n"
        text += "=" * 60 + "\n\n"

        text += f"Total channels: {stats['total_channels']}\n"
        text += f"Used channels: {stats['used_channels']}\n"
        text += f"2m repeaters: {stats['repeaters_2m']}\n"
        text += f"2m repeaters in PKT mode: {stats['repeaters_2m_pkt']}\n\n"

        text += "-" * 60 + "\n"
        text += "Band Distribution:\n"
        text += "-" * 60 + "\n"
        if stats['band_distribution']:
            for band in sorted(stats['band_distribution'].keys()):
                count = stats['band_distribution'][band]
                bar = "█" * (count * 40 // max(stats['band_distribution'].values()))
                text += f"{band:>6s}: {count:3d} {bar}\n"

        text += "\n" + "-" * 60 + "\n"
        text += "Mode Distribution:\n"
        text += "-" * 60 + "\n"
        if stats['mode_distribution']:
            for mode in sorted(stats['mode_distribution'].keys()):
                count = stats['mode_distribution'][mode]
                bar = "█" * (count * 40 // max(stats['mode_distribution'].values()))
                text += f"{mode:>6s}: {count:3d} {bar}\n"

        self.text.insert('1.0', text)
        self.text.config(state='disabled')


class FT897App:
    """Main application window"""

    def __init__(self, root):
        self.root = root
        self.root.title("FT-897 Memory Manager")
        self.root.geometry("1200x700")

        self.image: Optional[FT897Image] = None
        self.current_file: Optional[str] = None
        self.modified = False

        self.setup_ui()
        self.update_status()

    def setup_ui(self):
        """Setup the user interface"""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Image...", command=self.load_image, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_image_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Convert 2m to PKT", command=self.convert_2m_to_pkt)
        tools_menu.add_command(label="Statistics", command=self.show_statistics)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.load_image())
        self.root.bind('<Control-s>', lambda e: self.save_image())
        self.root.bind('<Control-q>', lambda e: self.root.quit())

        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Toolbar
        toolbar = ttk.Frame(main_container)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(toolbar, text="📂 Load Image", command=self.load_image).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="💾 Save", command=self.save_image).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="💾 Save As...", command=self.save_image_as).pack(side=tk.LEFT, padx=2)

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        ttk.Button(toolbar, text="📊 Statistics", command=self.show_statistics).pack(side=tk.LEFT, padx=2)

        # Operations frame
        ops_frame = ttk.LabelFrame(main_container, text="Batch Operations", padding="5")
        ops_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(ops_frame, text="🔄 Convert 2m Repeaters to PKT",
                   command=self.convert_2m_to_pkt).pack(side=tk.LEFT, padx=5)

        # Table frame
        table_frame = ttk.Frame(main_container)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Create Treeview (table)
        columns = ('ch', 'freq', 'mode', 'duplex', 'offset', 'name', 'band', 'skip', 'ipo', 'att')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', selectmode='browse')

        # Define headings
        self.tree.heading('ch', text='Ch#')
        self.tree.heading('freq', text='Frequency (MHz)')
        self.tree.heading('mode', text='Mode')
        self.tree.heading('duplex', text='Duplex')
        self.tree.heading('offset', text='Offset (kHz)')
        self.tree.heading('name', text='Name')
        self.tree.heading('band', text='Band')
        self.tree.heading('skip', text='Skip')
        self.tree.heading('ipo', text='IPO')
        self.tree.heading('att', text='ATT')

        # Define column widths
        self.tree.column('ch', width=50)
        self.tree.column('freq', width=120)
        self.tree.column('mode', width=60)
        self.tree.column('duplex', width=80)
        self.tree.column('offset', width=100)
        self.tree.column('name', width=100)
        self.tree.column('band', width=60)
        self.tree.column('skip', width=50)
        self.tree.column('ipo', width=50)
        self.tree.column('att', width=50)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Bind double-click
        self.tree.bind('<Double-1>', lambda e: self.edit_selected_channel())

        # Edit button
        edit_frame = ttk.Frame(main_container)
        edit_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(edit_frame, text="✏️ Edit Selected Channel",
                   command=self.edit_selected_channel).pack(side=tk.LEFT)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("No image loaded")
        status_bar = ttk.Label(main_container, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, pady=(5, 0))

    def load_image(self):
        """Load FT-897 image file"""
        filename = filedialog.askopenfilename(
            title="Load FT-897 Image",
            filetypes=[("FT-897 Image Files", "*.dat *.img"), ("All Files", "*.*")]
        )

        if not filename:
            return

        try:
            self.image = FT897Image()
            self.image.load_from_file(filename)
            self.current_file = filename
            self.modified = False
            self.update_table()
            self.update_status()

            messagebox.showinfo(
                "Success",
                f"Loaded {len(self.image.get_used_channels())} channels from\n{os.path.basename(filename)}"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")

    def save_image(self):
        """Save current image"""
        if not self.image:
            return

        if not self.current_file:
            self.save_image_as()
            return

        try:
            self.image.save_to_file(self.current_file)
            self.modified = False
            self.update_status()
            messagebox.showinfo("Success", f"Saved to\n{os.path.basename(self.current_file)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")

    def save_image_as(self):
        """Save image with new filename"""
        if not self.image:
            return

        filename = filedialog.asksaveasfilename(
            title="Save FT-897 Image",
            defaultextension=".dat",
            filetypes=[("FT-897 Image Files", "*.dat"), ("All Files", "*.*")]
        )

        if not filename:
            return

        try:
            self.image.save_to_file(filename)
            self.current_file = filename
            self.modified = False
            self.update_status()
            messagebox.showinfo("Success", f"Saved to\n{os.path.basename(filename)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")

    def update_table(self):
        """Update channel table"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.image:
            return

        used_channels = self.image.get_used_channels()

        for channel in used_channels:
            info = channel.get_info_dict()

            values = (
                info['index'],
                f"{info['frequency_mhz']:.4f}",
                info['mode_name'],
                info['duplex_name'],
                f"{info['offset_khz']:.1f}",
                info['name'],
                info['band'],
                "✓" if info['skip'] else "",
                "✓" if info['ipo'] else "",
                "✓" if info['att'] else ""
            )

            item_id = self.tree.insert('', 'end', values=values, tags=(channel.index,))

            # Color coding
            if info['mode'] == MODE_PKT:
                self.tree.item(item_id, tags=('pkt',))
            elif info['is_2m_repeater']:
                self.tree.item(item_id, tags=('2m',))

        # Configure tag colors
        self.tree.tag_configure('pkt', background='#c8ffc8')  # Light green
        self.tree.tag_configure('2m', background='#ffffc8')   # Light yellow

    def convert_2m_to_pkt(self):
        """Convert all 2m repeaters to PKT mode"""
        if not self.image:
            messagebox.showwarning("Warning", "No image loaded.")
            return

        repeaters = self.image.get_2m_repeaters()
        if not repeaters:
            messagebox.showinfo("Info", "No 2m repeaters found.")
            return

        if messagebox.askyesno(
            "Confirm",
            f"Convert {len(repeaters)} 2-meter repeaters to PKT mode?"
        ):
            modified = self.image.convert_2m_to_pkt()
            self.modified = True
            self.update_table()
            self.update_status()
            messagebox.showinfo("Success", f"Converted {modified} channels to PKT mode.")

    def edit_selected_channel(self):
        """Edit selected channel"""
        if not self.image:
            return

        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a channel to edit.")
            return

        # Get channel index from selected row
        item = self.tree.item(selected[0])
        channel_index = int(item['values'][0])

        # Find channel
        channel = None
        for ch in self.image.channels:
            if ch.index == channel_index:
                channel = ch
                break

        if not channel:
            return

        # Show editor dialog
        editor = ChannelEditorWindow(self.root, channel)
        self.root.wait_window(editor)

        if editor.result:
            self.modified = True
            self.update_table()
            self.update_status()

    def show_statistics(self):
        """Show image statistics"""
        if not self.image:
            messagebox.showwarning("Warning", "No image loaded.")
            return

        StatisticsWindow(self.root, self.image)

    def show_about(self):
        """Show about dialog"""
        about_text = """FT-897 Memory Manager
Version 1.0 (Tkinter Edition)

A lightweight GUI tool for managing Yaesu FT-897
radio memory images.

Features:
• Load and save FT-897 image files
• View and edit all memory channels
• Convert 2m repeaters to PKT mode
• Statistics and analysis

No external dependencies required!
Works on Windows, macOS, and Linux.

Author: Claude AI
License: MIT"""

        messagebox.showinfo("About", about_text)

    def update_status(self):
        """Update status bar"""
        if not self.image:
            self.status_var.set("No image loaded")
            return

        status = f"File: {os.path.basename(self.current_file) if self.current_file else 'Untitled'}"
        if self.modified:
            status += " [Modified]"

        stats = self.image.get_statistics()
        status += f" | Channels: {stats['used_channels']}/{stats['total_channels']}"
        status += f" | 2m Repeaters: {stats['repeaters_2m']}"

        self.status_var.set(status)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = FT897App(root)

    # Set window icon (if available)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass

    root.mainloop()


if __name__ == "__main__":
    main()
