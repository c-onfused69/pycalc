from pycalc.gui import CalculatorGUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()