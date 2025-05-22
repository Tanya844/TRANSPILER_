import os
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from transformer import CppTransformer  

def br_in():
    p = filedialog.askopenfilename(
        title="Select C File",
        filetypes=[("C files", "*.c"), ("All files", "*.*")]
    )
    if p:
        if not p.lower().endswith(".c"):
            messagebox.showwarning("Warning", "Please select a valid C file (*.c)")
            return
        iv.set(p)
        ov.set(os.path.splitext(p)[0] + ".cpp")
        try:
            with open(p, "r") as f:
                c = f.read()
                txt_in.delete(1.0, tk.END)
                txt_in.insert(tk.END, c)
            st.set(f"Loaded: {p}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

def br_out():
    p = filedialog.asksaveasfilename(
        title="Save C++ File",
        filetypes=[("C++ files", "*.cpp"), ("All files", "*.*")],
        defaultextension=".cpp"
    )
    if p:
        ov.set(p)

def transp():
    c = txt_in.get(1.0, tk.END)
    if not c.strip():
        messagebox.showwarning("Warning", "No C code to transpile!")
        return
    try:
        tf = CppTransformer()
        cpp = tf.transform(c)
        txt_out.config(state=tk.NORMAL)
        txt_out.delete(1.0, tk.END)
        txt_out.insert(tk.END, cpp)
        txt_out.config(state=tk.DISABLED)
        st.set("Transpilation completed successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Transpilation failed: {e}")
        st.set("Transpilation failed")

def save_out():
    cpp = txt_out.get(1.0, tk.END)
    if not cpp.strip():
        messagebox.showwarning("Warning", "No C++ code to save!")
        return
    p = ov.get()
    if not p:
        br_out()
        p = ov.get()
        if not p:
            return
    try:
        with open(p, "w") as f:
            f.write(cpp)
        st.set(f"Saved to: {p}")
        messagebox.showinfo("Success", f"File saved successfully to:\n{p}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")

def clr_all():
    txt_in.delete(1.0, tk.END)
    txt_out.config(state=tk.NORMAL)
    txt_out.delete(1.0, tk.END)
    txt_out.config(state=tk.DISABLED)
    iv.set("")
    ov.set("")
    st.set("Editor cleared. Ready for new input.")


root = tk.Tk()
root.title("C to C++ Transpiler")
root.geometry("900x700")
root.minsize(800, 600)

mf = ttk.Frame(root, padding="10")
mf.pack(fill=tk.BOTH, expand=True)

iv = tk.StringVar()
ov = tk.StringVar()
st = tk.StringVar(value="Ready")


ttk.Label(mf, text="C to C++ Transpiler", font=("Arial", 12, "bold")).pack(anchor=tk.W)

ttk.Separator(mf, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0,10))

ff = ttk.Frame(mf)
ff.pack(fill=tk.X, pady=(0,10))

ttk.Label(ff, text="Input C File:").grid(row=0, column=0, sticky=tk.W, pady=5)
en_in = ttk.Entry(ff, textvariable=iv, width=50)
en_in.grid(row=0, column=1, sticky=tk.W+tk.E, padx=5)
ttk.Button(ff, text="Browse...", command=br_in).grid(row=0, column=2, padx=5)

ttk.Label(ff, text="Output C++ File:").grid(row=1, column=0, sticky=tk.W, pady=5)
en_out = ttk.Entry(ff, textvariable=ov, width=50)
en_out.grid(row=1, column=1, sticky=tk.W+tk.E, padx=5)
ttk.Button(ff, text="Browse...", command=br_out).grid(row=1, column=2, padx=5)

ff.columnconfigure(1, weight=1)


ef = ttk.Frame(mf)
ef.pack(fill=tk.BOTH, expand=True, pady=(0,10))
ef.columnconfigure(0, weight=1)
ef.columnconfigure(1, weight=1)
ef.rowconfigure(1, weight=1)

ttk.Label(ef, text="C Code:").grid(row=0, column=0, sticky=tk.W, pady=(0,5))
txt_in = scrolledtext.ScrolledText(ef, wrap=tk.NONE, width=40, height=20, font=("Courier New", 10))
txt_in.grid(row=1, column=0, sticky=tk.NSEW, padx=(0,5))

ttk.Label(ef, text="C++ Code:").grid(row=0, column=1, sticky=tk.W, pady=(0,5))
txt_out = scrolledtext.ScrolledText(ef, wrap=tk.NONE, width=40, height=20, font=("Courier New", 10))
txt_out.grid(row=1, column=1, sticky=tk.NSEW, padx=(5,0))
txt_out.config(state=tk.DISABLED)


bf = ttk.Frame(mf)
bf.pack(fill=tk.X, pady=(0,10))

ttk.Button(bf, text="Transpile", command=transp, width=15).pack(side=tk.LEFT, padx=(0,10))
ttk.Button(bf, text="Clear", command=clr_all, width=15).pack(side=tk.LEFT, padx=(0,10))
ttk.Button(bf, text="Save Output", command=save_out, width=15).pack(side=tk.LEFT)


ttk.Label(mf, textvariable=st, relief=tk.SUNKEN, anchor=tk.W).pack(fill=tk.X, side=tk.BOTTOM)

root.mainloop()
