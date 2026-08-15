# Sorting Algorithms Visualizer and Comparator

A small Python desktop app that animates **Bubble Sort**, **Merge Sort**, and **Quick Sort** on the same data, reports elapsed time and comparison counts, and highlights the fastest run.

## Requirements

- Python 3.10 or newer (3.11+ recommended)
- Windows, macOS, or Linux with Tkinter available (included with most official Python builds)

## Setup

1. Open this folder in **Visual Studio Code**: `File → Open Folder…` and select the project directory.

2. Open a terminal in VS Code (**Ctrl+`**) or **Terminal → New Terminal**.

3. Create a virtual environment (recommended):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

## Run

From the project root (where `main.py` lives), with the virtual environment activated:

```powershell
python main.py
```

### Run from VS Code

- Open `main.py`, press **F5**, or use **Run → Run Without Debugging**.
- If prompted for a Python interpreter, pick the one from `.venv`.

## Usage

1. **Load data**: type numbers separated by commas or spaces, then **Load**, or click **Random**.
2. **One algorithm**: press **Bubble Sort**, **Merge Sort**, or **Quick Sort**. The panel shows time (ms), comparisons, and Big-O notes; the chart animates the steps.
3. **Run All**: measures all three on a copy of the current array, shows which was fastest by time, then plays the three animations in sequence.
4. **Speed**: lower delay (slider left) runs faster; **Pause** / **Resume** control playback; **Reset** stops animation and redraws the original bars.
5. **Dark mode**: toggles the window and chart theme.

## Example input

```text
42 17 9 88 3 61 25
```

or

```text
5, 2, 8, 1, 9
```

## Project layout

| Path | Role |
|------|------|
| `main.py` | Starts the app; selects the `TkAgg` Matplotlib backend |
| `gui/app.py` | Main window, controls, results text |
| `gui/animator.py` | Non-blocking animation loop (`after`) with pause/resume |
| `algorithms/` | Bubble, merge, and quick sort step generators |
| `visualization/chart.py` | Bar chart colors and updates |
| `utils/` | Input parsing and statistics helpers |

## License

Use and modify freely for learning or your own projects.
