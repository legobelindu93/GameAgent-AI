import tkinter as tk
from tkinter import ttk
from .profiles import load_profiles
from .engine import State, choose, step

def main():
    root = tk.Tk()
    root.title("GameAgent AI | Simulation")
    root.geometry("900x560")
    profiles = load_profiles()
    sidebar = ttk.Frame(root, padding=12)
    sidebar.pack(side="left", fill="y")
    panel = ttk.Frame(root, padding=20)
    panel.pack(side="right", fill="both", expand=True)
    title = ttk.Label(panel, text="Choose a game", font=("Segoe UI", 20))
    title.pack(anchor="w")
    info = ttk.Label(panel, wraplength=600)
    info.pack(anchor="w", pady=12)
    trace = tk.Text(panel, height=15, state="disabled")
    trace.pack(fill="both", expand=True)
    state = State()
    selected = None
    def log(message):
        trace.configure(state="normal")
        trace.insert("end", message + "\n")
        trace.see("end")
        trace.configure(state="disabled")
    def select(key):
        nonlocal selected, state
        selected, state = key, State()
        p = profiles[key]
        title.configure(text=p["name"])
        info.configure(text="Research targets: " + ", ".join(p["targets"]) + "\nGeneric simulator only; no live game integration.")
        trace.configure(state="normal")
        trace.delete("1.0", "end")
        trace.configure(state="disabled")
        log("New isolated simulation session")
        run.configure(state="normal")
    def tick():
        nonlocal state
        if selected is None or state.hp <= 0 or state.enemy <= 0 or state.turn >= 30:
            run.configure(state="disabled")
            return
        action, reason = choose(state)
        state = step(state, action)
        log(f"Turn {state.turn}: {action.value} | {reason} | HP {state.hp} | Enemy {state.enemy}")
        if state.hp <= 0 or state.enemy <= 0 or state.turn >= 30:
            run.configure(state="disabled")
    run = ttk.Button(panel, text="Simulate one turn", command=tick, state="disabled")
    run.pack(anchor="w", pady=12)
    for key, p in profiles.items():
        ttk.Button(sidebar, text=p["name"], command=lambda k=key: select(k)).pack(fill="x", pady=4)
    root.mainloop()

if __name__ == "__main__":
    main()
