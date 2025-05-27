from pycalc.gui import CalculatorGUI
import tkinter as tk

def main():
    root = tk.Tk()
    root.iconbitmap(r'd:/Projects/pycalc/screenshots/icons/pycalc.ico')
    app = CalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
