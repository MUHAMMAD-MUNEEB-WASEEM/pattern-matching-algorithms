

import tkinter as tk
from tkinter import messagebox
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Implementing the algorithms
def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    positions = []
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            positions.append(i)
    return positions

def rabin_karp_search(text, pattern, q=101):
    d = 256
    n = len(text)
    m = len(pattern)
    p = 0
    t = 0
    h = 1
    positions = []
    
    for i in range(m - 1):
        h = (h * d) % q
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(n - m + 1):
        if p == t:
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                positions.append(i)
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t = t + q
    return positions

def kmp_search(text, pattern):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    n = len(text)
    m = len(pattern)
    lps = compute_lps(pattern)
    positions = []
    i = 0
    j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return positions

def boyer_moore_search(text, pattern):
    def bad_character_heuristic(pattern):
        bad_char = [-1] * 256
        for i in range(len(pattern)):
            bad_char[ord(pattern[i])] = i
        return bad_char

    def good_suffix_heuristic(pattern):
        m = len(pattern)
        good_suffix = [m] * (m + 1)
        i = m
        j = m + 1
        border_positions = [0] * (m + 1)
        border_positions[i] = j
        while i > 0:
            while j <= m and pattern[i - 1] != pattern[j - 1]:
                if good_suffix[j] == m:
                    good_suffix[j] = j - i
                j = border_positions[j]
            i -= 1
            j -= 1
            border_positions[i] = j
        j = border_positions[0]
        for i in range(m + 1):
            if good_suffix[i] == m:
                good_suffix[i] = j
            if i == j:
                j = border_positions[j]
        return good_suffix

    n = len(text)
    m = len(pattern)
    bad_char = bad_character_heuristic(pattern)
    good_suffix = good_suffix_heuristic(pattern)
    positions = []
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            positions.append(s)
            s += good_suffix[0]
        else:
            s += max(good_suffix[j + 1], j - bad_char[ord(text[s + j])])
    return positions

# Comparative Analysis Function
def compare_algorithms(text, pattern):
    algorithms = {
        'Naive': naive_search,
        'Rabin-Karp': rabin_karp_search,
        'KMP': kmp_search,
        'Boyer-Moore': boyer_moore_search
    }
    results = {}
    times = {}

    for name, algorithm in algorithms.items():
        start_time = time.time()
        positions = algorithm(text, pattern)
        end_time = time.time()
        results[name] = positions
        times[name] = end_time - start_time

    return results, times

# Function to handle button click
def on_search():
    text = text_entry.get("1.0", tk.END).strip()
    pattern = pattern_entry.get().strip()
    if not text or not pattern:
        messagebox.showerror("Input Error", "Both text and pattern are required.")
        return
    
    results, times = compare_algorithms(text, pattern)

    results_text = "Results:\n"
    for name in results:
        results_text += f"{name}: {results[name]}\n"

    results_text += "\nExecution Times:\n"
    for name in times:
        results_text += f"{name}: {times[name]:.6f} seconds\n"

    results_label.config(text=results_text)

    # Clear the previous plot
    for widget in graph_frame.winfo_children():
        widget.destroy()

    # Plotting the graph
    fig, ax = plt.subplots()
    ax.bar(times.keys(), times.values(), color=['blue', 'green', 'red', 'purple'])
    ax.set_xlabel('Algorithms')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Pattern Matching Algorithms Performance')

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Setting up the UI
window = tk.Tk()
window.title("Pattern Matching Algorithms Comparison")

# Header section
header_frame = tk.Frame(window)
header_frame.pack()

teacher_label = tk.Label(header_frame, text="Teacher: Sir Basit", font=("Arial", 14, "bold"))
teacher_label.pack()

roll_numbers = ["Name: Muhammad Zeeshan", "Roll No: Muhammad Muneeb", "Roll No: Asad Saleem"]
for roll_number in roll_numbers:
    roll_label = tk.Label(header_frame, text=roll_number, font=("Arial", 12))
    roll_label.pack()

# Text and pattern input
text_label = tk.Label(window, text="Text:")
text_label.pack()
text_entry = tk.Text(window, height=10, width=50)
text_entry.pack()

pattern_label = tk.Label(window, text="Pattern:")
pattern_label.pack()
pattern_entry = tk.Entry(window)
pattern_entry.pack()

# Search button
search_button = tk.Button(window, text="Search", command=on_search)
search_button.pack()

# Results display
results_label = tk.Label(window, text="", justify=tk.LEFT)
results_label.pack()

# Graph display frame
graph_frame = tk.Frame(window)
graph_frame.pack()

window.mainloop()
