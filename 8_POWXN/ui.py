import copy
import tkinter as tk
from tkinter import messagebox, ttk

# =====================================================================
# DISPLAYED PYTHON CODE (Line numbers map directly to the highlighter)
# =====================================================================
FAST_CODE_LINES = [
    (1, "def myPow(self, x: float, n: int) -> float:"),
    (2, "    def helper(x, n):"),
    (3, "        if x == 0: return 0"),
    (4, "        if n == 0: return 1          # Base case"),
    (5, ""),
    (6, "        res = helper(x, n // 2)      # 1. Split n in half"),
    (7, "        res = res * res              # 2. Square the half-result"),
    (8, "        return x * res if n % 2 else res  # 3. Odd exponent fix"),
    (9, ""),
    (10, "    result = helper(x, abs(n))"),
    (11, "    return result if n >= 0 else (1 / result)"),
]

NAIVE_CODE_LINES = [
    (1, "def myPow_Naive(self, x: float, n: int) -> float:"),
    (2, "    def helper(x, n):"),
    (3, "        if x == 0: return 0"),
    (4, "        if n == 0: return 1          # Base case"),
    (5, ""),
    (6, "        # BAD: Calls helper() TWICE instead of res = res * res!"),
    (7, "        res = helper(x, n // 2) * helper(x, n // 2)"),
    (8, "        return x * res if n % 2 else res"),
    (9, ""),
    (10, "    result = helper(x, abs(n))"),
    (11, "    return result if n >= 0 else (1 / result)"),
]


class PowRecursionVisualizer(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("LeetCode 50: Pow(x, n) — Interactive Recursion Tree UI")
        self.geometry("1340x820")
        self.minsize(1100, 700)
        self.configure(bg="#0f172a")

        # State variables
        self.x_val = 2.0
        self.n_val = 10
        self.mode = "fast"  # "fast" (res = res * res) or "naive" (helper * helper)
        self.steps = []
        self.current_step_idx = 0
        self.is_playing = False
        self.play_job = None

        self._setup_styles()
        self._build_ui()
        self._bind_shortcuts()
        self.generate_simulation(2.0, 10, "fast")

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#0f172a")
        style.configure(
            "Panel.TFrame", background="#1e293b", relief="flat", borderwidth=1
        )
        style.configure(
            "TLabel",
            background="#0f172a",
            foreground="#f8fafc",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Header.TLabel",
            background="#1e293b",
            foreground="#38bdf8",
            font=("Segoe UI", 11, "bold"),
        )
        style.configure(
            "Action.TButton",
            background="#2563eb",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=(10, 5),
        )
        style.map("Action.TButton", background=[("active", "#1d4ed8")])
        style.configure(
            "Preset.TButton",
            background="#334155",
            foreground="#e2e8f0",
            font=("Segoe UI", 9),
            padding=(8, 4),
        )
        style.map("Preset.TButton", background=[("active", "#475569")])

    def _build_ui(self):
        # 1. TOP CONTROL BAR
        top_bar = ttk.Frame(self, style="Panel.TFrame", padding=10)
        top_bar.pack(fill=tk.X, padx=12, pady=(12, 6))

        # Inputs
        ttk.Label(
            top_bar, text="Base (x):", background="#1e293b", foreground="#cbd5e1"
        ).pack(side=tk.LEFT, padx=(4, 4))
        self.x_entry = tk.Entry(
            top_bar,
            width=7,
            bg="#0f172a",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            font=("Consolas", 11),
            relief="flat",
            highlightthickness=1,
            highlightbackground="#475569",
        )
        self.x_entry.insert(0, "2.0")
        self.x_entry.pack(side=tk.LEFT, padx=(0, 12), ipady=3)

        ttk.Label(
            top_bar, text="Exponent (n):", background="#1e293b", foreground="#cbd5e1"
        ).pack(side=tk.LEFT, padx=(4, 4))
        self.n_entry = tk.Entry(
            top_bar,
            width=7,
            bg="#0f172a",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            font=("Consolas", 11),
            relief="flat",
            highlightthickness=1,
            highlightbackground="#475569",
        )
        self.n_entry.insert(0, "10")
        self.n_entry.pack(side=tk.LEFT, padx=(0, 12), ipady=3)

        ttk.Button(
            top_bar,
            text="Build Tree",
            style="Action.TButton",
            command=self._on_apply_inputs,
        ).pack(side=tk.LEFT, padx=(0, 16))

        # Presets
        ttk.Label(
            top_bar, text="Presets:", background="#1e293b", foreground="#94a3b8"
        ).pack(side=tk.LEFT, padx=(4, 6))
        presets = [
            ("2¹⁰ (Even)", 2.0, 10),
            ("2⁵ (Odd)", 2.0, 5),
            ("2⁻³ (Negative)", 2.0, -3),
            ("3⁷ (Odd Chain)", 3.0, 7),
            ("2⁰ (Zero)", 2.0, 0),
        ]
        for label, px, pn in presets:
            ttk.Button(
                top_bar,
                text=label,
                style="Preset.TButton",
                command=lambda x=px, n=pn: self._load_preset(x, n),
            ).pack(side=tk.LEFT, padx=3)

        # Mode Switcher (Right side of top bar)
        self.mode_btn = tk.Button(
            top_bar,
            text="Mode: ✅ Fast (res = res * res)",
            bg="#059669",
            fg="#ffffff",
            activebackground="#047857",
            activeforeground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=12,
            pady=4,
            cursor="hand2",
            command=self._toggle_mode,
        )
        self.mode_btn.pack(side=tk.RIGHT, padx=4)

        # 2. PLAYBACK & STEP BAR
        play_bar = ttk.Frame(self, style="Panel.TFrame", padding=8)
        play_bar.pack(fill=tk.X, padx=12, pady=6)

        ttk.Button(
            play_bar, text="⏮ Start", style="Preset.TButton", command=self.step_first
        ).pack(side=tk.LEFT, padx=3)
        ttk.Button(
            play_bar,
            text="◀ Prev (←)",
            style="Preset.TButton",
            command=self.step_prev,
        ).pack(side=tk.LEFT, padx=3)

        self.play_btn = ttk.Button(
            play_bar,
            text="▶ Auto-Play (Space)",
            style="Action.TButton",
            command=self.toggle_play,
        )
        self.play_btn.pack(side=tk.LEFT, padx=6)

        ttk.Button(
            play_bar,
            text="Next (→) ▶",
            style="Preset.TButton",
            command=self.step_next,
        ).pack(side=tk.LEFT, padx=3)
        ttk.Button(
            play_bar, text="End ⏭", style="Preset.TButton", command=self.step_last
        ).pack(side=tk.LEFT, padx=3)

        # Step scrubber slider
        self.step_scale = tk.Scale(
            play_bar,
            from_=0,
            to=1,
            orient=tk.HORIZONTAL,
            showvalue=False,
            bg="#1e293b",
            fg="#f8fafc",
            troughcolor="#0f172a",
            highlightthickness=0,
            activebackground="#38bdf8",
            command=self._on_slider_move,
        )
        self.step_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=14)

        self.step_counter_lbl = ttk.Label(
            play_bar,
            text="Step 1 / 1",
            background="#1e293b",
            foreground="#38bdf8",
            font=("Consolas", 11, "bold"),
        )
        self.step_counter_lbl.pack(side=tk.RIGHT, padx=8)

        self.stats_lbl = ttk.Label(
            play_bar,
            text="Calls: 0 | Multiplications: 0",
            background="#1e293b",
            foreground="#fbbf24",
            font=("Consolas", 10, "bold"),
        )
        self.stats_lbl.pack(side=tk.RIGHT, padx=14)

        # 3. MAIN WORKSPACE (3 Columns: Code + Math | Recursion Tree Canvas | Call Stack)
        workspace = ttk.Frame(self)
        workspace.pack(fill=tk.BOTH, expand=True, padx=12, pady=(4, 12))

        # --- LEFT COLUMN: Code & Live Explanation ---
        left_col = ttk.Frame(workspace, width=410)
        left_col.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        left_col.pack_propagate(False)

        # Code Panel
        code_panel = ttk.Frame(left_col, style="Panel.TFrame", padding=10)
        code_panel.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(
            code_panel, text="🐍 Live Python Execution", style="Header.TLabel"
        ).pack(anchor=tk.W, pady=(0, 6))

        self.code_canvas = tk.Canvas(
            code_panel, bg="#0f172a", height=255, highlightthickness=0
        )
        self.code_canvas.pack(fill=tk.X)

        # Live Math Inspector Panel
        explain_panel = ttk.Frame(left_col, style="Panel.TFrame", padding=12)
        explain_panel.pack(fill=tk.BOTH, expand=True)
        ttk.Label(
            explain_panel,
            text="🔍 Step & Math Breakdown",
            style="Header.TLabel",
        ).pack(anchor=tk.W, pady=(0, 6))

        self.step_title_lbl = tk.Label(
            explain_panel,
            text="",
            bg="#1e293b",
            fg="#fbbf24",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            justify="left",
            wraplength=380,
        )
        self.step_title_lbl.pack(fill=tk.X, pady=(2, 8))

        self.explain_text = tk.Text(
            explain_panel,
            bg="#0f172a",
            fg="#e2e8f0",
            font=("Consolas", 10),
            relief="flat",
            wrap=tk.WORD,
            padx=10,
            pady=10,
            height=12,
            state=tk.DISABLED,
        )
        self.explain_text.pack(fill=tk.BOTH, expand=True)

        # Legend inside Left Column bottom
        legend_frame = tk.Frame(explain_panel, bg="#1e293b")
        legend_frame.pack(fill=tk.X, pady=(8, 0))
        legends = [
            ("#2563eb", "Calling Down"),
            ("#d97706", "Base Case"),
            ("#9333ea", "res = res * res"),
            ("#059669", "Returned"),
        ]
        for color, text in legends:
            swatch = tk.Frame(legend_frame, bg=color, width=12, height=12)
            swatch.pack(side=tk.LEFT, padx=(0, 4))
            tk.Label(
                legend_frame,
                text=text,
                bg="#1e293b",
                fg="#cbd5e1",
                font=("Segoe UI", 8),
            ).pack(side=tk.LEFT, padx=(0, 10))

        # --- CENTER COLUMN: Interactive Recursion Tree Canvas ---
        center_col = ttk.Frame(workspace, style="Panel.TFrame", padding=8)
        center_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        header_row = tk.Frame(center_col, bg="#1e293b")
        header_row.pack(fill=tk.X, pady=(0, 6))
        ttk.Label(
            header_row,
            text="🌳 Recursion Tree (Drag to Pan, Scroll to Move)",
            style="Header.TLabel",
        ).pack(side=tk.LEFT)

        self.tree_canvas = tk.Canvas(
            center_col, bg="#0b1120", highlightthickness=0, cursor="fleur"
        )
        self.tree_canvas.pack(fill=tk.BOTH, expand=True)

        # Canvas panning and scrolling bindings
        self.tree_canvas.bind("<ButtonPress-1>", self._start_pan)
        self.tree_canvas.bind("<B1-Motion>", self._do_pan)
        self.tree_canvas.bind("<MouseWheel>", self._on_mousewheel)

        # --- RIGHT COLUMN: Call Stack Visualizer ---
        right_col = ttk.Frame(workspace, style="Panel.TFrame", width=230, padding=10)
        right_col.pack(side=tk.RIGHT, fill=tk.Y)
        right_col.pack_propagate(False)

        ttk.Label(right_col, text="📚 Call Stack (LIFO)", style="Header.TLabel").pack(
            anchor=tk.W, pady=(0, 6)
        )
        self.stack_canvas = tk.Canvas(
            right_col, bg="#0f172a", highlightthickness=0
        )
        self.stack_canvas.pack(fill=tk.BOTH, expand=True)

    def _bind_shortcuts(self):
        self.bind("<Right>", lambda e: self.step_next())
        self.bind("<Left>", lambda e: self.step_prev())
        self.bind("<space>", lambda e: self.toggle_play())
        self.bind("<Home>", lambda e: self.step_first())
        self.bind("<End>", lambda e: self.step_last())

    # =====================================================================
    # SIMULATION ENGINE (Generates every step of the recursion tree)
    # =====================================================================
    def generate_simulation(self, x: float, n: int, mode: str):
        self.pause_play()
        self.x_val = x
        self.n_val = n
        self.mode = mode

        nodes = {}
        steps = []
        call_stack = []
        node_counter = [0]
        calls_count = [0]
        mults_count = [0]

        def snapshot(active_line, active_id, title, explanation):
            steps.append(
                {
                    "nodes": copy.deepcopy(nodes),
                    "stack": list(call_stack),
                    "line": active_line,
                    "active_id": active_id,
                    "title": title,
                    "explanation": explanation,
                    "calls": calls_count[0],
                    "mults": mults_count[0],
                }
            )

        # Pre-build entire tree structure so node coordinates stay stable
        def prebuild_tree(cur_n, depth, parent_id=None):
            nid = node_counter[0]
            node_counter[0] += 1
            nodes[nid] = {
                "id": nid,
                "x": x,
                "n": cur_n,
                "depth": depth,
                "parent_id": parent_id,
                "children": [],
                "status": "pending",  # pending, calling, waiting, base, squaring, done
                "half_res": None,
                "squared_res": None,
                "ret_val": None,
                "badge": "",
            }
            if parent_id is not None:
                nodes[parent_id]["children"].append(nid)

            if x != 0 and cur_n > 0:
                if mode == "fast":
                    prebuild_tree(cur_n // 2, depth + 1, nid)
                else:
                    prebuild_tree(cur_n // 2, depth + 1, nid)
                    prebuild_tree(cur_n // 2, depth + 1, nid)
            return nid

        root_id = prebuild_tree(abs(n), 0, None)

        # Initial step: Entry into myPow
        snapshot(
            10,
            root_id,
            f"Start: myPow(x={x:g}, n={n})",
            f"We call helper({x:g}, abs({n})) -> helper({x:g}, {abs(n)}).\n\n"
            + (
                "Mode: FAST O(log n)\nEach level calls helper(x, n // 2) ONCE and squares the result using `res = res * res`."
                if mode == "fast"
                else "Mode: NAIVE O(n) TRAP\nWithout `res = res * res`, calling `helper() * helper()` branches into TWO duplicate calls at every level!"
            ),
        )

        # Trace execution recursively
        def trace(nid):
            node = nodes[nid]
            cur_n = node["n"]
            calls_count[0] += 1
            node["status"] = "calling"
            call_stack.append(f"helper({x:g}, {cur_n})")

            snapshot(
                2,
                nid,
                f"Call helper({x:g}, {cur_n})",
                f"Pushed helper({x:g}, {cur_n}) onto the Call Stack (Depth {node['depth']}).\n"
                f"Goal: Calculate {x:g}^{cur_n}.",
            )

            if x == 0:
                node["status"] = "base"
                node["ret_val"] = 0.0
                node["badge"] = "Base: 0"
                snapshot(
                    3,
                    nid,
                    "Base Case: x == 0",
                    "Since base x is 0, return 0 immediately.",
                )
                node["status"] = "done"
                call_stack.pop()
                return 0.0

            if cur_n == 0:
                node["status"] = "base"
                node["ret_val"] = 1.0
                node["badge"] = "Base: 1"
                snapshot(
                    4,
                    nid,
                    "Base Case Reached: n == 0",
                    f"Any non-zero number to the power of 0 is 1 ({x:g}^0 = 1).\n"
                    f"Now the recursion can start unwinding back up the tree!",
                )
                node["status"] = "done"
                call_stack.pop()
                return 1.0

            half_n = cur_n // 2
            node["status"] = "waiting"

            if mode == "fast":
                child_id = node["children"][0]
                snapshot(
                    6,
                    nid,
                    f"Split Exponent: {cur_n} // 2 = {half_n}",
                    f"To find {x:g}^{cur_n}, we pause helper({x:g}, {cur_n}) and ask for the half-power:\n"
                    f"res = helper({x:g}, {half_n})",
                )

                half_res = trace(child_id)

                # Back in current frame: res = res * res
                node["status"] = "squaring"
                node["half_res"] = half_res
                squared = half_res * half_res
                node["squared_res"] = squared
                mults_count[0] += 1
                node["badge"] = f"res*res = {squared:g}"

                snapshot(
                    7,
                    nid,
                    f"Square It! res = {half_res:g} * {half_res:g} = {squared:g}",
                    f"WHY `res = res * res` HAPPENS HERE:\n"
                    f"• Child helper({x:g}, {half_n}) returned res = {half_res:g} (which is {x:g}^{half_n}).\n"
                    f"• Squaring `res * res` ({half_res:g} × {half_res:g}) gives {squared:g} (which is {x:g}^{half_n * 2}) in ONE multiplication!",
                )

                # Odd/even check
                if cur_n % 2 == 1:
                    final_res = x * squared
                    mults_count[0] += 1
                    node["ret_val"] = final_res
                    node["badge"] = f"{squared:g} * {x:g} = {final_res:g}"
                    Explain_odd = (
                        f"n = {cur_n} is ODD ({cur_n} % 2 == 1).\n"
                        f"Since {cur_n} // 2 = {half_n} dropped 1 exponent ({half_n} + {half_n} = {half_n * 2}), "
                        f"we multiply by an extra x ({x:g}):\n"
                        f"{x:g} * {squared:g} = {final_res:g}  ({x:g}^{cur_n})."
                    )
                else:
                    final_res = squared
                    node["ret_val"] = final_res
                    node["badge"] = f"Return {final_res:g}"
                    Explain_odd = (
                        f"n = {cur_n} is EVEN ({cur_n} % 2 == 0).\n"
                        f"Squaring `res` already gave us the exact power {x:g}^{cur_n} = {final_res:g}.\n"
                        f"Return {final_res:g} directly!"
                    )

                node["status"] = "done"
                snapshot(
                    8,
                    nid,
                    f"Return {final_res:g} from helper({x:g}, {cur_n})",
                    Explain_odd,
                )
                call_stack.pop()
                return final_res

            else:
                # NAIVE MODE: calls helper twice
                left_id, right_id = node["children"][0], node["children"][1]
                snapshot(
                    7,
                    nid,
                    f"Left Branch: helper({x:g}, {half_n})",
                    f"Calling first helper({x:g}, {half_n})...",
                )
                left_val = trace(left_id)

                snapshot(
                    7,
                    nid,
                    f"Duplicate Right Branch: helper({x:g}, {half_n})",
                    f"Because we did NOT save `res` and do `res = res * res`, Python now has to recompute "
                    f"helper({x:g}, {half_n}) all over again from scratch!",
                )
                right_val = trace(right_id)

                node["status"] = "squaring"
                squared = left_val * right_val
                mults_count[0] += 1
                if cur_n % 2 == 1:
                    final_res = x * squared
                    mults_count[0] += 1
                    node["badge"] = f"{left_val:g}*{right_val:g}*{x:g}={final_res:g}"
                else:
                    final_res = squared
                    node["badge"] = f"{left_val:g}*{right_val:g}={final_res:g}"

                node["ret_val"] = final_res
                node["status"] = "done"
                snapshot(
                    8,
                    nid,
                    f"Return {final_res:g} from helper({x:g}, {cur_n})",
                    f"Combined duplicate branches: {left_val:g} * {right_val:g}"
                    + (f" * {x:g}" if cur_n % 2 else "")
                    + f" = {final_res:g}.",
                )
                call_stack.pop()
                return final_res

        pos_result = trace(root_id)
        final_answer = pos_result if n >= 0 else (1.0 / pos_result if pos_result != 0 else 0.0)

        snapshot(
            11,
            root_id,
            f"Finished! Final Output = {final_answer:.6g}",
            f"helper({x:g}, {abs(n)}) returned {pos_result:g}.\n"
            + (
                f"Since n = {n} is negative, we return 1 / {pos_result:g} = {final_answer:.6g}."
                if n < 0
                else f"Since n = {n} >= 0, final result is {final_answer:g}."
            )
            + f"\n\nTotal Recursive Calls: {calls_count[0]}\nTotal Multiplications: {mults_count[0]}",
        )

        self.steps = steps
        self.current_step_idx = 0
        self.step_scale.configure(to=max(0, len(self.steps) - 1))
        self.render_current_step()

    # =====================================================================
    # RENDERING LOGIC (Tree Canvas, Code Highlighter, Call Stack)
    # =====================================================================
    def render_current_step(self):
        if not self.steps:
            return
        step = self.steps[self.current_step_idx]

        # Update top counters
        total = len(self.steps)
        self.step_counter_lbl.configure(
            text=f"Step {self.current_step_idx + 1} / {total}"
        )
        self.stats_lbl.configure(
            text=f"Recursive Calls: {step['calls']}  |  Multiplications: {step['mults']}"
        )

        # Sync scale without re-triggering callback loop
        self.step_scale.set(self.current_step_idx)

        # Update Explanation Box
        self.step_title_lbl.configure(text=step["title"])
        self.explain_text.configure(state=tk.NORMAL)
        self.explain_text.delete("1.0", tk.END)
        self.explain_text.insert(tk.END, step["explanation"])
        self.explain_text.configure(state=tk.DISABLED)

        # Render sub-canvases
        self._render_code(step["line"])
        self._render_stack(step["stack"])
        self._render_tree(step["nodes"], step["active_id"])

    def _render_code(self, active_line: int):
        self.code_canvas.delete("all")
        lines = FAST_CODE_LINES if self.mode == "fast" else NAIVE_CODE_LINES
        row_h = 22

        for idx, (line_no, text) in enumerate(lines):
            y = 6 + idx * row_h
            is_active = line_no == active_line

            if is_active:
                bg_color = "#854d0e" if line_no != 7 else "#581c87"
                self.code_canvas.create_rectangle(
                    4, y - 2, 390, y + row_h - 2, fill=bg_color, outline="#eab308"
                )

            num_color = "#fbbf24" if is_active else "#475569"
            txt_color = "#ffffff" if is_active else "#cbd5e1"
            font_style = (
                ("Consolas", 9, "bold") if is_active else ("Consolas", 9)
            )

            self.code_canvas.create_text(
                22, y + 8, text=f"{line_no:2d}", fill=num_color, font=font_style
            )
            self.code_canvas.create_text(
                38,
                y + 8,
                text=text,
                fill=txt_color,
                font=font_style,
                anchor="w",
            )

    def _render_stack(self, stack: list):
        self.stack_canvas.delete("all")
        w = self.stack_canvas.winfo_width() or 200
        h = self.stack_canvas.winfo_height() or 500

        if not stack:
            self.stack_canvas.create_text(
                w // 2,
                h // 2,
                text="Stack is empty\n(No active calls)",
                fill="#64748b",
                font=("Segoe UI", 10, "italic"),
                justify="center",
            )
            return

        box_h = 36
        gap = 6
        for i, frame_label in enumerate(stack):
            # Draw from bottom up (standard stack visualization)
            y_bottom = h - 16 - i * (box_h + gap)
            y_top = y_bottom - box_h
            is_top = i == len(stack) - 1

            fill_col = "#2563eb" if is_top else "#1e293b"
            border_col = "#60a5fa" if is_top else "#475569"

            self.stack_canvas.create_rectangle(
                12,
                y_top,
                w - 12,
                y_bottom,
                fill=fill_col,
                outline=border_col,
                width=2 if is_top else 1,
            )
            prefix = "▶ " if is_top else f"#{i+1} "
            self.stack_canvas.create_text(
                w // 2,
                (y_top + y_bottom) // 2,
                text=f"{prefix}{frame_label}",
                fill="#ffffff" if is_top else "#cbd5e1",
                font=("Consolas", 10, "bold" if is_top else "normal"),
            )

    def _render_tree(self, nodes: dict, active_id: int):
        self.tree_canvas.delete("all")
        if not nodes:
            return

        cw = self.tree_canvas.winfo_width() or 680
        ch = self.tree_canvas.winfo_height() or 560

        # Compute clean layout coordinates
        leaf_counter = [0]
        x_coords = {}
        y_coords = {}
        h_spacing = 128 if self.mode == "naive" else 160
        v_spacing = 92

        def assign_coords(nid):
            node = nodes[nid]
            children = node["children"]
            y_coords[nid] = 55 + node["depth"] * v_spacing
            if not children:
                x_coords[nid] = leaf_counter[0] * h_spacing
                leaf_counter[0] += 1
            else:
                for cid in children:
                    assign_coords(cid)
                x_coords[nid] = (
                    x_coords[children[0]] + x_coords[children[-1]]
                ) / 2.0

        assign_coords(0)

        # Center tree horizontally inside canvas
        all_x = list(x_coords.values())
        tree_width = max(all_x) - min(all_x) if all_x else 0
        offset_x = max(90, (cw - tree_width) / 2.0 - min(all_x))

        for nid in x_coords:
            x_coords[nid] += offset_x

        # 1. Draw Edges first
        for nid, node in nodes.items():
            x1, y1 = x_coords[nid], y_coords[nid]
            for cid in node["children"]:
                child = nodes[cid]
                x2, y2 = x_coords[cid], y_coords[cid]

                if child["status"] == "pending":
                    edge_col = "#1e293b"
                    dash = (4, 4)
                    width = 1.5
                elif child["status"] == "done":
                    edge_col = "#10b981"
                    dash = ()
                    width = 2.5
                else:
                    edge_col = "#38bdf8"
                    dash = ()
                    width = 2.5

                self.tree_canvas.create_line(
                    x1,
                    y1 + 24,
                    x2,
                    y2 - 24,
                    fill=edge_col,
                    width=width,
                    dash=dash,
                    arrow=tk.LAST,
                )

                # Edge label (n // 2 or return value)
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                if child["status"] == "done" and child["ret_val"] is not None:
                    self.tree_canvas.create_text(
                        mx + 28,
                        my,
                        text=f"↑ {child['ret_val']:g}",
                        fill="#34d399",
                        font=("Consolas", 9, "bold"),
                    )
                elif child["status"] != "pending":
                    self.tree_canvas.create_text(
                        mx - 24,
                        my,
                        text=f"n//2={child['n']}",
                        fill="#7dd3fc",
                        font=("Consolas", 8),
                    )

        # 2. Draw Nodes
        node_w, node_h = 62, 24
        palette = {
            "pending": ("#0f172a", "#334155", "#475569"),
            "calling": ("#1d4ed8", "#60a5fa", "#ffffff"),
            "waiting": ("#1e293b", "#38bdf8", "#cbd5e1"),
            "base": ("#b45309", "#fbbf24", "#ffffff"),
            "squaring": ("#7e22ce", "#e879f9", "#ffffff"),
            "done": ("#065f46", "#34d399", "#ffffff"),
        }

        for nid, node in nodes.items():
            cx, cy = x_coords[nid], y_coords[nid]
            bg, border, fg = palette.get(node["status"], palette["pending"])
            is_active = nid == active_id

            # Glow ring for active node
            if is_active:
                self.tree_canvas.create_rectangle(
                    cx - node_w - 5,
                    cy - node_h - 5,
                    cx + node_w + 5,
                    cy + node_h + 5,
                    outline="#fbbf24",
                    width=2,
                    dash=(3, 2),
                )

            # Main node card
            self.tree_canvas.create_rectangle(
                cx - node_w,
                cy - node_h,
                cx + node_w,
                cy + node_h,
                fill=bg,
                outline=border,
                width=2.5 if is_active else 1.5,
            )

            # Call label
            self.tree_canvas.create_text(
                cx,
                cy - 7,
                text=f"helper({node['x']:g}, {node['n']})",
                fill=fg,
                font=("Consolas", 9, "bold"),
            )

            # Math badge inside bottom of node
            sub_text = node["badge"] if node["badge"] else (
                "odd (n%2=1)" if node["n"] % 2 == 1 else "even (n%2=0)"
            )
            sub_col = "#fde047" if node["badge"] else "#64748b"
            self.tree_canvas.create_text(
                cx,
                cy + 10,
                text=sub_text,
                fill=sub_col,
                font=("Consolas", 8, "bold" if node["badge"] else "normal"),
            )

        # Update scrollregion so deep trees can be panned freely
        bbox = self.tree_canvas.bbox("all")
        if bbox:
            pad = 60
            self.tree_canvas.configure(
                scrollregion=(
                    bbox[0] - pad,
                    bbox[1] - pad,
                    bbox[2] + pad,
                    bbox[3] + pad,
                )
            )

    # =====================================================================
    # INTERACTION HANDLERS (Buttons, Presets, Pan/Scroll)
    # =====================================================================
    def _on_apply_inputs(self):
        try:
            x = float(self.x_entry.get().strip())
            n = int(self.n_entry.get().strip())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid float for x and an integer for n.",
            )
            return

        if self.mode == "naive" and abs(n) > 15:
            messagebox.showwarning(
                "Exponent Too Large for Naive Mode",
                "In Naive O(n) mode, the tree doubles at every depth!\n"
                "Capping |n| to 15 so the branching tree fits on screen.\n"
                "(Switch to Fast Mode to test large exponents!)",
            )
            n = 15 if n > 0 else -15
            self.n_entry.delete(0, tk.END)
            self.n_entry.insert(0, str(n))

        self.generate_simulation(x, n, self.mode)

    def _load_preset(self, x: float, n: int):
        self.x_entry.delete(0, tk.END)
        self.x_entry.insert(0, str(x))
        self.n_entry.delete(0, tk.END)
        self.n_entry.insert(0, str(n))
        self._on_apply_inputs()

    def _toggle_mode(self):
        if self.mode == "fast":
            self.mode = "naive"
            self.mode_btn.configure(
                text="Mode: ❌ Naive (helper * helper)",
                bg="#dc2626",
                activebackground="#b91c1c",
            )
            if abs(self.n_val) > 15:
                self.n_val = 10
                self.n_entry.delete(0, tk.END)
                self.n_entry.insert(0, "10")
        else:
            self.mode = "fast"
            self.mode_btn.configure(
                text="Mode: ✅ Fast (res = res * res)",
                bg="#059669",
                activebackground="#047857",
            )
        self.generate_simulation(self.x_val, self.n_val, self.mode)

    def step_next(self):
        if self.current_step_idx < len(self.steps) - 1:
            self.current_step_idx += 1
            self.render_current_step()
        else:
            self.pause_play()

    def step_prev(self):
        self.pause_play()
        if self.current_step_idx > 0:
            self.current_step_idx -= 1
            self.render_current_step()

    def step_first(self):
        self.pause_play()
        self.current_step_idx = 0
        self.render_current_step()

    def step_last(self):
        self.pause_play()
        if self.steps:
            self.current_step_idx = len(self.steps) - 1
            self.render_current_step()

    def _on_slider_move(self, val):
        idx = int(float(val))
        if idx != self.current_step_idx and 0 <= idx < len(self.steps):
            self.current_step_idx = idx
            self.render_current_step()

    def toggle_play(self):
        if self.is_playing:
            self.pause_play()
        else:
            if self.current_step_idx >= len(self.steps) - 1:
                self.current_step_idx = 0
            self.is_playing = True
            self.play_btn.configure(text="⏸ Pause (Space)")
            self._auto_step()

    def pause_play(self):
        self.is_playing = False
        self.play_btn.configure(text="▶ Auto-Play (Space)")
        if self.play_job is not None:
            self.after_cancel(self.play_job)
            self.play_job = None

    def _auto_step(self):
        if not self.is_playing:
            return
        if self.current_step_idx < len(self.steps) - 1:
            self.current_step_idx += 1
            self.render_current_step()
            self.play_job = self.after(750, self._auto_step)
        else:
            self.pause_play()

    def _start_pan(self, event):
        self.tree_canvas.scan_mark(event.x, event.y)

    def _do_pan(self, event):
        self.tree_canvas.scan_dragto(event.x, event.y, gain=1)

    def _on_mousewheel(self, event):
        self.tree_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == "__main__":
    app = PowRecursionVisualizer()
    app.mainloop()