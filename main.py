import tkinter as tk
from tkinter import ttk
import copy

def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

def validate_int(input):
    return input.isdigit()

def menu():
    clear_frame()
    frm_menu = ttk.Frame(root, padding=10)
    frm_menu.pack(fill="both", expand=True)

    ttk.Label(frm_menu, text="Wybierz rozmiar macierzy", font=("Arial", 14)).pack(pady=10)

    entry_frame = ttk.Frame(frm_menu)
    entry_frame.pack(pady=10)

    row_no_var = tk.StringVar()
    col_no_var = tk.StringVar()

    row_no = ttk.Entry(entry_frame, width=3, textvariable=row_no_var, validate="key",
                       validatecommand=(validate_cmd, "%P"))
    col_no = ttk.Entry(entry_frame, width=3, textvariable=col_no_var, validate="key",
                       validatecommand=(validate_cmd, "%P"))

    row_no.grid(column=0, row=0, padx=5)
    ttk.Label(entry_frame, text="x", background="#1e1e1e", foreground="#ffffff").grid(column=1, row=0, padx=5)
    col_no.grid(column=2, row=0, padx=5)

    button_frame = ttk.Frame(frm_menu)
    button_frame.pack(pady=20)

    ttk.Button(button_frame, text="Wyjdź", command=root.destroy).pack(side="left", padx=10)
    ttk.Button(button_frame, text="Dalej", command=lambda: animate_to_frm(matrix, row_no_var.get(), col_no_var.get())).pack(
        side="left", padx=10)

def show_error(error_message, frm, *args):
    clear_frame()
    error_frame = ttk.Frame(root, padding=10)
    error_frame.pack(fill="both", expand=True)
    ttk.Label(error_frame, text="Błąd:", font=("Arial", 14)).pack(pady=10)
    ttk.Label(error_frame, text=f"{error_message}", font=("Arial", 14)).pack(pady=10)
    ttk.Button(error_frame, text="Wyjdź", command=root.destroy).pack(side="left", padx=10)
    ttk.Button(error_frame, text="Powrót", command=lambda: animate_to_frm(frm, *args)).pack(pady=10)

def matrix(row_no, col_no):
    if row_no == "" or col_no == "":
        show_error("Podaj rozmiar macierzy.", menu)
    else:
        clear_frame()
        frm_matrix = ttk.Frame(root, padding=10)
        frm_matrix.pack(fill="both", expand=True)

        ttk.Label(frm_matrix, text="Podaj wartości macierzy:", font=("Arial", 14)).pack(pady=10)

        entries_supply = []
        entries_demand = []
        entries_cost = []

        row_no = int(row_no)
        col_no = int(col_no)

        frm_matrix_grid = ttk.Frame(frm_matrix, padding=5)
        frm_matrix_grid.pack()

        for y in range(col_no + 1):
            if y == 0:
                ttk.Label(frm_matrix_grid, text="", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
            else:
                ttk.Label(frm_matrix_grid, text=f"D{y}", font=("Arial", 10)).grid(row=0, column=y, padx=5, pady=5)
        ttk.Label(frm_matrix_grid, text="Podaż", font=("Arial", 10)).grid(row=0, column=col_no + 1, padx=5, pady=5)

        for x in range(row_no + 1):
            for y in range(col_no + 2):
                if x == row_no and y == 0:
                    ttk.Label(frm_matrix_grid, text="Popyt", font=("Arial", 10)).grid(row=row_no + 1, column=0, padx=5, pady=5)
                    continue
                if y == 0:
                    if x < row_no:
                        ttk.Label(frm_matrix_grid, text=f"S{x + 1}", font=("Arial", 10)).grid(row=x + 1, column=0, padx=5, pady=5)
                elif x == row_no:
                    if y <= col_no:
                        entry = ttk.Entry(frm_matrix_grid, width=5, validate="key", validatecommand=(validate_cmd, "%P"))
                        entry.grid(row=row_no + 1, column=y, padx=5, pady=5)
                        entries_demand.append(entry)
                elif y == col_no + 1:
                    entry = ttk.Entry(frm_matrix_grid, width=5, validate="key", validatecommand=(validate_cmd, "%P"))
                    entry.grid(row=x + 1, column=col_no + 1, padx=5, pady=5)
                    entries_supply.append(entry)
                else:
                    entry = ttk.Entry(frm_matrix_grid, width=5, validate="key", validatecommand=(validate_cmd, "%P"))
                    entry.grid(row=x + 1, column=y, padx=5, pady=5)
                    entries_cost.append(entry)

        frm_matrix_buttons = ttk.Frame(frm_matrix, padding=10)
        frm_matrix_buttons.pack(fill="both", expand=True)

        ttk.Button(frm_matrix_buttons, text="Wyjdź", command=root.destroy).pack(side="left", padx=10)
        ttk.Button(
            frm_matrix_buttons,
            text="Oblicz",
            command=lambda: process_entries(entries_supply, entries_demand, entries_cost, row_no, col_no)
        ).pack(pady=10)

def process_entries(entries_supply, entries_demand, entries_cost, row_no, col_no):
    try:
        supply = [int(entry.get()) for entry in entries_supply]
        demand = [int(entry.get()) for entry in entries_demand]
        cost = [
            [int(entries_cost[i * col_no + j].get()) for j in range(col_no)]
            for i in range(row_no)
        ]
    except ValueError:
        show_error("Podaj poprawne dane liczbowe.", matrix, row_no, col_no)
        return

    if sum(supply) != sum(demand):
        show_error("Wprowadź problem zbilansowany.", matrix, row_no, col_no)
        return

    animate_to_frm(show_matrix, supply, demand, cost, row_no, col_no)

def show_matrix(supply, demand, cost, row_no, col_no):
    clear_frame()
    frm_matrix_grid = ttk.Frame(root, padding=3)
    frm_matrix_grid.grid()

    step_text = ttk.Label(frm_matrix_grid, text="Macierz:", font=("Arial", 14))
    step_text.grid(column=0, row=0, columnspan=col_no + 2, padx=5, pady=5)

    for j in range(col_no):
        ttk.Label(frm_matrix_grid, text=f"D{j + 1}", font=("Arial", 12)).grid(column=j + 1, row=1, padx=5, pady=5)
    ttk.Label(frm_matrix_grid, text="Podaż", font=("Arial", 10)).grid(row=1, column=col_no + 1, padx=5, pady=5)

    entry_grid = []
    for i in range(row_no):
        ttk.Label(frm_matrix_grid, text=f"S{i + 1}", font=("Arial", 12)).grid(column=0, row=i + 2, padx=5, pady=5)

        row_entries = []
        for j in range(col_no):
            var = tk.StringVar(value=str(cost[i][j]))
            entry = tk.Entry(frm_matrix_grid, textvariable=var, font=("Arial", 12), width=10, state="readonly",
                             justify="center")  # Zwiększona szerokość z 5 do 10
            entry.grid(column=j + 1, row=i + 2, padx=3, pady=3)
            row_entries.append(entry)
        entry_grid.append(row_entries)

    supply_labels = [ttk.Label(frm_matrix_grid, text=str(s), font=("Arial", 12)) for s in supply]
    demand_labels = [ttk.Label(frm_matrix_grid, text=str(d), font=("Arial", 12)) for d in demand]

    for i, lbl in enumerate(supply_labels):
        lbl.grid(column=col_no + 1, row=i + 2, padx=5, pady=5)

    for j, lbl in enumerate(demand_labels):
        lbl.grid(column=j + 1, row=row_no + 2, padx=5, pady=5)

    ttk.Label(frm_matrix_grid, text="Popyt", font=("Arial", 10)).grid(row=row_no + 2, column=0, padx=5, pady=5)

    algorithm_state = {
        "supply": supply[:],
        "demand": demand[:],
        "cost": cost,
        "step": 1,
        "allocations": [[0 for _ in range(col_no)] for _ in range(row_no)],
        "highlighted": None,
        "total_cost": 0,
        "current_step_function": None
    }

    def highlight_cell(row, col):
        if entry_grid[row][col]["readonlybackground"] not in ["orange", "#8b13d1"]:
            entry_grid[row][col].config(state="normal")
            entry_grid[row][col].config(bg="#FFEB3B", readonlybackground="#FFEB3B")
            entry_grid[row][col].config(state="readonly")

    def highlight_row(row):
        for col in range(col_no):
            if entry_grid[row][col]["readonlybackground"] not in ["orange", "#8b13d1"]:
                entry_grid[row][col].config(state="normal")
                entry_grid[row][col].config(bg="red", readonlybackground="red")
                entry_grid[row][col].config(state="readonly")

    def highlight_column(col):
        for row in range(row_no):
            if entry_grid[row][col]["readonlybackground"] not in ["orange", "#8b13d1"]:
                entry_grid[row][col].config(state="normal")
                entry_grid[row][col].config(bg="red", readonlybackground="red")
                entry_grid[row][col].config(state="readonly")

    def next_step():
        if algorithm_state["current_step_function"]:
            algorithm_state["current_step_function"]()

    def step_choose_minimum():
        current_supply = algorithm_state["supply"]
        current_demand = algorithm_state["demand"]
        current_cost = algorithm_state["cost"]

        if algorithm_state["highlighted"]:
            i, j = algorithm_state["highlighted"]
            entry_grid[i][j].config(state="normal")
            entry_grid[i][j].config(bg="#8b13d1", readonlybackground="#8b13d1")
            entry_grid[i][j].config(state="readonly")
            algorithm_state["highlighted"] = None

        min_value = float('inf')
        min_pos = None
        for i in range(row_no):
            for j in range(col_no):
                if current_supply[i] > 0 and current_demand[j] > 0 and current_cost[i][j] < min_value:
                    min_value = current_cost[i][j]
                    min_pos = (i, j)

        if min_pos is None:
            calculate_total_cost()
            return

        i, j = min_pos
        highlight_cell(i, j)
        algorithm_state["highlighted"] = (i, j)
        step_text.config(text=f"Krok {algorithm_state['step']} - Wybór najmniejszej wartości ({min_value})")

        algorithm_state["current_step_function"] = lambda: step_allocation(i, j)

    def step_allocation(i, j):
        current_supply = algorithm_state["supply"]
        current_demand = algorithm_state["demand"]
        allocations = algorithm_state["allocations"]

        allocation = min(current_supply[i], current_demand[j])
        allocations[i][j] = allocation
        algorithm_state["total_cost"] += allocation * algorithm_state["cost"][i][j]

        current_supply[i] -= allocation
        current_demand[j] -= allocation

        supply_labels[i].config(text=str(current_supply[i]))
        demand_labels[j].config(text=str(current_demand[j]))

        entry_grid[i][j].config(state="normal")
        entry_grid[i][j].delete(0, tk.END)
        entry_grid[i][j].insert(0, f"{algorithm_state['cost'][i][j]} ({allocation})")
        entry_grid[i][j].config(bg="orange", readonlybackground="orange")
        entry_grid[i][j].config(state="readonly")

        step_text.config(text=f"Krok {algorithm_state['step']} - Aktualizacja popytu i podaży")
        algorithm_state["current_step_function"] = lambda: step_elimination(i, j)

    def step_elimination(i, j):
        current_supply = algorithm_state["supply"]
        current_demand = algorithm_state["demand"]

        eliminated = []
        if current_supply[i] == 0:
            highlight_row(i)
            eliminated.append(f"dostawcy S{i + 1}")
        if current_demand[j] == 0:
            highlight_column(j)
            eliminated.append(f"odbiorcy D{j + 1}")

        if eliminated:
            step_text.config(text=f"Krok {algorithm_state['step']} - Wyeliminowanie {', '.join(eliminated)}")

        algorithm_state["step"] += 1
        algorithm_state["current_step_function"] = step_choose_minimum

    def calculate_total_cost():
        clear_frame()
        frm_result = ttk.Frame(root, padding=10)
        frm_result.grid()

        ttk.Label(frm_result, text="Obliczanie kosztu całkowitego", font=("Arial", 16)).grid(row=0, column=0, pady=10)

        equation_parts = []
        for i in range(row_no):
            for j in range(col_no):
                if algorithm_state["allocations"][i][j] > 0:
                    allocation = algorithm_state["allocations"][i][j]
                    equation_parts.append(f"{allocation}*{cost[i][j]}")

        equation = " + ".join(equation_parts)
        total_cost = algorithm_state["total_cost"]

        ttk.Label(frm_result, text=f"Równanie: {equation}", font=("Arial", 14)).grid(row=1, column=0, pady=10)
        ttk.Label(frm_result, text=f"Koszt całkowity: {total_cost}", font=("Arial", 14)).grid(row=2, column=0, pady=10)

        ttk.Button(frm_result, text="Powrót do menu", command=lambda: animate_to_frm(menu)).grid(row=3, column=0, pady=20)
        ttk.Button(frm_result, text="Wyjdź", command=root.destroy).grid(row=4, column=0, pady=5)

    ttk.Button(frm_matrix_grid, text="Wyjdź", command=root.destroy).grid(column=0, row=row_no + 3, columnspan=(col_no + 2) // 2, padx=5, pady=10, sticky="ew")
    ttk.Button(frm_matrix_grid, text="Dalej", command=next_step).grid(column=(col_no + 2) // 2, row=row_no + 3, columnspan=(col_no + 2) // 2, padx=5, pady=10, sticky="ew")

    algorithm_state["current_step_function"] = step_choose_minimum

def animate_to_frm(frm, *args):
    for alpha in range(100, 0, -5):
        root.attributes("-alpha", alpha / 100)
        root.update_idletasks()
        root.after(10)

    frm(*args)

    for alpha in range(0, 101, 5):
        root.attributes("-alpha", alpha / 100)
        root.update_idletasks()
        root.after(10)

root = tk.Tk()
root.title("Problem Transportowy")
root.eval('tk::PlaceWindow . center')
root.resizable(False, False)
validate_cmd = root.register(validate_int)
root.configure(bg="#1e1e1e")

style = ttk.Style(root)
style.configure("TFrame", background="#1e1e1e")
style.configure("TLabel", background="#1e1e1e", foreground="#ffffff")
style.configure("TButton", background="#1e1e1e", foreground="#8903a3", font=("Arial", 10))

menu()
root.mainloop()
