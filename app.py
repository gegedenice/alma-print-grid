import tkinter as tk
from tkinter import messagebox, simpledialog
from client.alma_client import AlmaClient
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import platform

class AlmaGridApp:
    def __init__(self, master):
        self.master = master
        master.title("Alma Grid App")

        self.grid_frame = tk.Frame(master, padx=20, pady=20)
        self.grid_frame.pack()

        self.grid = [[None for _ in range(4)] for _ in range(5)]
        self.rotation_flags = [[False for _ in range(4)] for _ in range(5)]
        self.split_flags = [[False for _ in range(4)] for _ in range(5)]  # Pour garder la trace des lignes
        self.current_row = 0
        self.current_col = 0
        self.entries = []
        self.labels = []  # Pour les labels d'état

        cell_width = 16 * 37.795  # Conversion cm à pixels
        cell_height = 22 * 37.795  # Conversion cm à pixels

        # Crée la grille d'entrées
        for i in range(5):
            row_entries = []
            row_labels = []
            for j in range(4):
                frame = tk.Frame(self.grid_frame)
                frame.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

                entry = tk.Entry(frame, width=10, font=("Arial", 24), justify="center", bd=2, relief="groove")
                entry.pack(side=tk.TOP)
                row_entries.append(entry)

                rotate_button = tk.Button(frame, text="Rotate", command=lambda r=i, c=j: self.toggle_rotation(r, c))
                rotate_button.pack(side=tk.LEFT)

                split_button = tk.Button(frame, text="Split", command=lambda r=i, c=j: self.toggle_split(r, c))
                split_button.pack(side=tk.RIGHT)

                label = tk.Label(frame, text="Horizontally\nOne Line", justify="center")
                label.pack(side=tk.BOTTOM)
                row_labels.append(label)

                entry.config(width=int(cell_width / 7))

            self.entries.append(row_entries)
            self.labels.append(row_labels)

        for i in range(5):
            self.grid_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.grid_frame.grid_columnconfigure(j, weight=1)

        self.master.bind('<Return>', self.process_barcode)

        # Boutons
        
        self.preview_button = tk.Button(master, text="Preview PDF", command=self.preview_pdf, font=("Arial", 16), bg="#007BFF", fg="white", padx=10, pady=5)
        self.preview_button.pack(pady=10)
        
        self.print_button = tk.Button(master, text="Print to PDF", command=self.real_print, font=("Arial", 16), bg="#4CAF50", fg="white", padx=10, pady=5)
        self.print_button.pack(pady=10)

        self.focus_on_current_entry()

    def toggle_rotation(self, row, col):
        self.rotation_flags[row][col] = not self.rotation_flags[row][col]
        state = "vertical" if self.rotation_flags[row][col] else "horizontal"
        current_lines_state = "Two Lines" if self.split_flags[row][col] else "One Line"
        self.labels[row][col].config(text=f"{state.capitalize()}\n{current_lines_state}")

    def toggle_split(self, row, col):
        if self.grid[row][col]:
            if self.split_flags[row][col]:
                # Réunir les lignes si déjà divisé
                parts = self.grid[row][col].split('\n', 1)  # Divise sur le premier caractère de nouvelle ligne
                self.grid[row][col] = parts[0] + " " + parts[1]  # Rejoindre les parties
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, self.grid[row][col])
                self.split_flags[row][col] = False
                self.labels[row][col].config(text=self.labels[row][col]["text"].split('\n')[0] + "\nOne Line")
            else:
                # Diviser sur le premier espace
                parts = self.grid[row][col].split(' ', 1)  # Divise sur le premier espace
                if len(parts) > 1:
                    self.grid[row][col] = parts[0] + "\n" + parts[1]  # L'ordre est maintenant corrigé
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, self.grid[row][col])
                    self.split_flags[row][col] = True
                    self.labels[row][col].config(text=self.labels[row][col]["text"].split('\n')[0] + "\nTwo Lines")
                else:
                    messagebox.showinfo("Info", "Cannot split. No space found.")
                    return
        else:
            messagebox.showinfo("Info", "Cell is empty. Please fill it first.")
            return

    def process_barcode(self, event):
        # A adapter pour la lecture de CB avec douchette
        barcode = simpledialog.askstring("Scan Barcode", "Please enter the barcode:") # Simule l'entrée de code-barres

        if self.current_row < 5 and self.current_col < 4:
            item_value = AlmaClient.dummy_search_item(format="call-number",item_barcode=barcode)
            #item_value = AlmaClient.search_item(format="call-number",item_barcode=barcode)
            self.grid[self.current_row][self.current_col] = item_value
            self.entries[self.current_row][self.current_col].delete(0, tk.END)
            self.entries[self.current_row][self.current_col].insert(0, item_value)

            if self.current_col == 3:
                self.current_col = 0
                self.current_row += 1
            else:
                self.current_col += 1

            self.focus_on_current_entry()

        else:
            messagebox.showinfo("Info", "All boxes are filled.")

    def focus_on_current_entry(self):
        self.entries[self.current_row][self.current_col].focus_set()

    def save_grid(self):
        c = canvas.Canvas("alma_grid.pdf", pagesize=A4)
        width, height = A4

        cell_width = width / 4
        cell_height = height / 6

        for i in range(5):
            for j in range(4):
                text = str(self.grid[i][j]) if self.grid[i][j] else ""
                x = j * cell_width
                y = height - (i * cell_height + cell_height)

                if self.rotation_flags[i][j]:
                    c.saveState()
                    c.translate(x + cell_width / 2, y + cell_height / 2)
                    c.rotate(90)
                    c.drawString(-10, 0, text)
                    c.restoreState()
                else:
                    if self.split_flags[i][j]:
                        lines = text.split('\n')  # Chaque partie sur une nouvelle ligne
                        for index, line in enumerate(lines):
                            # Centrer verticalement et horizontalement
                            c.drawString(x + (cell_width / 2 - c.stringWidth(line) / 2), y + cell_height / 2 + (index * 15), line)
                    else:
                        c.drawString(x + cell_width / 2 - 10, y + cell_height / 2, text)

        c.save()
        messagebox.showinfo("Info", "Grid printed to alma_grid.pdf")
        
    def real_print(self):
        # Imprimer le PDF
        if platform.system() == "Windows":
            os.startfile("alma_grid.pdf", "print")
        elif platform.system() == "Darwin":  # macOS
            os.system("lp alma_grid.pdf")  # Utilise l'impression en ligne de commande
        else:  # Linux et autres
            os.system("lp alma_grid.pdf")  # Utilise l'impression en ligne de commande

    def preview_pdf(self):
        # Régénère le PDF avant d'ouvrir
        self.save_grid()  # Appelle save_grid pour mettre à jour le PDF
        if os.path.exists("alma_grid.pdf"):
            if platform.system() == "Windows":
                os.startfile("alma_grid.pdf")
            elif platform.system() == "Darwin":  # macOS
                os.system("open alma_grid.pdf")
            else:  # Linux et autres
                os.system("xdg-open alma_grid.pdf")
        else:
            messagebox.showwarning("Warning", "Please print the PDF first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlmaGridApp(root)
    root.mainloop()
