#!/usr/bin/env python3
"""
GUI Application for C to C++ Transpiler
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from transformer import CppTransformer  # Import the transformer module

class TranspilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("C to C++ Transpiler")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set application icon (optional)
        # self.root.iconbitmap("icon.ico")  # Uncomment and add your icon if you have one
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create and configure style
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 11))
        self.style.configure("Header.TLabel", font=("Arial", 12, "bold"))
        
        # Create GUI components
        self.create_header()
        self.create_file_section()
        self.create_code_editor()
        self.create_action_buttons()
        self.create_status_bar()
        
        # Initialize variables
        self.input_file_path = None
        self.output_file_path = None
    
    def create_header(self):
        """Create header with title and description"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        header_label = ttk.Label(
            header_frame, 
            text="C to C++ Transpiler", 
            style="Header.TLabel"
        )
        header_label.pack(side=tk.TOP, anchor=tk.W)
        
        desc_label = ttk.Label(
            header_frame,
            text="Convert C code to equivalent C++ code with automatic syntax transformations",
            wraplength=600
        )
        desc_label.pack(side=tk.TOP, anchor=tk.W, pady=(0, 5))
        
        ttk.Separator(self.main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=(0, 10))
    
    def create_file_section(self):
        """Create file input/output section"""
        file_frame = ttk.Frame(self.main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Input file selection
        input_label = ttk.Label(file_frame, text="Input C File:")
        input_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.input_file_var = tk.StringVar()
        input_entry = ttk.Entry(file_frame, textvariable=self.input_file_var, width=50)
        input_entry.grid(row=0, column=1, sticky=tk.W + tk.E, padx=5)
        
        input_button = ttk.Button(file_frame, text="Browse...", command=self.browse_input_file)
        input_button.grid(row=0, column=2, padx=5)
        
        # Output file selection
        output_label = ttk.Label(file_frame, text="Output C++ File:")
        output_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.output_file_var = tk.StringVar()
        output_entry = ttk.Entry(file_frame, textvariable=self.output_file_var, width=50)
        output_entry.grid(row=1, column=1, sticky=tk.W + tk.E, padx=5)
        
        output_button = ttk.Button(file_frame, text="Browse...", command=self.browse_output_file)
        output_button.grid(row=1, column=2, padx=5)
        
        # Configure grid
        file_frame.columnconfigure(1, weight=1)
    
    def create_code_editor(self):
        """Create code editor section with input and output text areas"""
        editor_frame = ttk.Frame(self.main_frame)
        editor_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Configure grid
        editor_frame.columnconfigure(0, weight=1)
        editor_frame.columnconfigure(1, weight=1)
        editor_frame.rowconfigure(1, weight=1)
        
        # Input area
        input_label = ttk.Label(editor_frame, text="C Code:")
        input_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(
            editor_frame, 
            wrap=tk.NONE,
            width=40, 
            height=20,
            font=("Courier New", 10)
        )
        self.input_text.grid(row=1, column=0, sticky=tk.NSEW, padx=(0, 5))
        
        # Output area
        output_label = ttk.Label(editor_frame, text="C++ Code:")
        output_label.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        self.output_text = scrolledtext.ScrolledText(
            editor_frame, 
            wrap=tk.NONE,
            width=40, 
            height=20,
            font=("Courier New", 10)
        )
        self.output_text.grid(row=1, column=1, sticky=tk.NSEW, padx=(5, 0))
        self.output_text.config(state=tk.DISABLED)  # Read-only initially
    
    def create_action_buttons(self):
        """Create action buttons for transpilation"""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Transpile button
        self.transpile_button = ttk.Button(
            button_frame, 
            text="Transpile", 
            command=self.transpile_code,
            width=15
        )
        self.transpile_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        self.clear_button = ttk.Button(
            button_frame, 
            text="Clear", 
            command=self.clear_all,
            width=15
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save button
        self.save_button = ttk.Button(
            button_frame, 
            text="Save Output", 
            command=self.save_output,
            width=15
        )
        self.save_button.pack(side=tk.LEFT)
    
    def create_status_bar(self):
        """Create status bar for displaying messages"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        status_bar = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def browse_input_file(self):
        """Open file dialog to select input C file"""
        file_path = filedialog.askopenfilename(
            title="Select C File",
            filetypes=[("C files", "*.c"), ("All files", "*.*")]
        )
        
        if file_path:
            self.input_file_path = file_path
            self.input_file_var.set(file_path)
            
            # Auto-suggest output file name
            output_path = os.path.splitext(file_path)[0] + ".cpp"
            self.output_file_var.set(output_path)
            self.output_file_path = output_path
            
            # Load file content
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(tk.END, content)
                self.status_var.set(f"Loaded: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def browse_output_file(self):
        """Open file dialog to select output C++ file"""
        file_path = filedialog.asksaveasfilename(
            title="Save C++ File",
            filetypes=[("C++ files", "*.cpp"), ("All files", "*.*")],
            defaultextension=".cpp"
        )
        
        if file_path:
            self.output_file_path = file_path
            self.output_file_var.set(file_path)
    
    def transpile_code(self):
        """Transpile C code to C++ code"""
        c_code = self.input_text.get(1.0, tk.END)
        
        if not c_code.strip():
            messagebox.showwarning("Warning", "No C code to transpile!")
            return
        
        try:
            # Use the transformer to convert C to C++
            transformer = CppTransformer(None)  # No AST needed for quick transform
            cpp_code = transformer.quick_transform(c_code)
            
            # Update output text area
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, cpp_code)
            self.output_text.config(state=tk.NORMAL)  # Make editable for potential manual adjustments
            
            self.status_var.set("Transpilation completed successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Transpilation failed: {str(e)}")
            self.status_var.set("Transpilation failed")
    
    def save_output(self):
        """Save the transpiled C++ code to file"""
        cpp_code = self.output_text.get(1.0, tk.END)
        
        if not cpp_code.strip():
            messagebox.showwarning("Warning", "No C++ code to save!")
            return
        
        # If output path not set, ask for it
        if not self.output_file_path:
            self.browse_output_file()
            if not self.output_file_path:  # User canceled
                return
        
        try:
            with open(self.output_file_path, "w") as f:
                f.write(cpp_code)
            self.status_var.set(f"Saved to: {self.output_file_path}")
            messagebox.showinfo("Success", f"File saved successfully to:\n{self.output_file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def clear_all(self):
        """Clear all input and output fields"""
        self.input_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.input_file_var.set("")
        self.output_file_var.set("")
        self.input_file_path = None
        self.output_file_path = None
        self.status_var.set("Ready")

def main():
    root = tk.Tk()
    app = TranspilerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()