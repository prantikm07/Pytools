import tkinter as tk
from tkinter import filedialog, messagebox
import colorgram
from PIL import Image, ImageDraw, ImageTk
import pyperclip


def extract_colors(path, num):
    try:
        colors = colorgram.extract(path, num)
    except Exception as e:
        raise
    hex_colors = []
    for color in colors:
        r, g, b = color.rgb.r, color.rgb.g, color.rgb.b
        hex_colors.append('#{:02x}{:02x}{:02x}'.format(r, g, b))
    return hex_colors


def create_palette(colors, width=500, height=100):
    if not colors:
        return Image.new('RGB', (width, height), '#ffffff')
    block_width = max(1, width // len(colors))
    palette = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(palette)
    for i, color in enumerate(colors):
        x0, x1 = i * block_width, (i + 1) * block_width
        draw.rectangle([x0, 0, x1, height], fill=color)
    return palette


def copy_to_clipboard(hex_code):
    if hex_code:
        pyperclip.copy(hex_code)


image_refs = {}


def generate_palette():
    path = entry.get().strip()
    if not path:
        messagebox.showerror('Error', 'No file selected')
        return
    try:
        colors = extract_colors(path, 6)
    except Exception as ex:
        messagebox.showerror('Error', f'Failed to generate palette: {ex}')
        return
    palette_img = create_palette(colors)
    tk_palette = ImageTk.PhotoImage(palette_img)
    palette_label.config(image=tk_palette)
    image_refs['palette'] = tk_palette
    for i in range(6):
        if i < len(colors):
            hex_labels[i].config(text=colors[i])
            hex_labels[i].bind('<Button-1>', lambda e, c=colors[i]: copy_to_clipboard(c))
        else:
            hex_labels[i].config(text='')
            hex_labels[i].unbind('<Button-1>')


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[('Image files', '*.jpg *.jpeg *.png')])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)


root = tk.Tk()
root.title('Color Palette Generator')
frame = tk.Frame(root)
frame.pack(pady=10)
entry = tk.Entry(frame, width=50)
entry.pack(side=tk.LEFT, padx=10)
browse_btn = tk.Button(frame, text='Browse', command=open_file)
browse_btn.pack(side=tk.LEFT)
generate_btn = tk.Button(root, text='Generate Palette', command=generate_palette)
generate_btn.pack(pady=10)
info_label = tk.Label(root, text='Click on the hex code to copy', font=('Arial', 10))
info_label.pack()

placeholder_img = Image.new('RGB', (500, 100), '#ffffff')
tk_placeholder = ImageTk.PhotoImage(placeholder_img)
palette_label = tk.Label(root, image=tk_placeholder)
image_refs['placeholder'] = tk_placeholder
palette_label.pack()
hex_frame = tk.Frame(root)
hex_frame.pack(pady=10)
hex_labels = [tk.Label(hex_frame, text='', font=('Arial', 12), width=12, relief='groove') for _ in range(6)]
for label in hex_labels:
    label.pack(side=tk.LEFT, padx=5)
root.mainloop()
