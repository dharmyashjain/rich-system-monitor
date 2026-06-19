# Rich System Monitor
# A beautiful real-time system monitor in the terminal.
# Displays CPU usage per core, RAM, disk, and network stats
# in a live-updating Rich dashboard with colored progress bars.
#
# Install: pip install rich psutil
# Usage:   python sysmon.py

import time
import psutil
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.columns import Columns
from rich import box

console = Console()

def make_bar(percent, width=20):
    # Build a simple ASCII progress bar based on percentage
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    # Color changes based on how stressed the resource is
    color = "green" if percent < 60 else "yellow" if percent < 85 else "red"
    return f"[{color}]{bar}[/{color}] {percent:.1f}%"

def build_dashboard():
    # --- CPU usage per core ---
    cpu_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    cpu_table.add_column("Core", style="dim", width=8)
    cpu_table.add_column("Usage", width=35)
    for i, pct in enumerate(psutil.cpu_percent(percpu=True)):
        cpu_table.add_row(f"Core {i}", make_bar(pct))

    # --- Memory stats ---
    mem = psutil.virtual_memory()
    mem_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    mem_table.add_column("", style="dim", width=8)
    mem_table.add_column("", width=35)
    mem_table.add_row("RAM", make_bar(mem.percent))
    mem_table.add_row("Used", f"{mem.used / 1e9:.2f} GB / {mem.total / 1e9:.2f} GB")

    # --- Disk usage ---
    disk = psutil.disk_usage("/")
    disk_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    disk_table.add_column("", style="dim", width=8)
    disk_table.add_column("", width=35)
    disk_table.add_row("Disk", make_bar(disk.percent))
    disk_table.add_row("Free", f"{disk.free / 1e9:.1f} GB free of {disk.total / 1e9:.1f} GB")

    # --- Network I/O counters ---
    net = psutil.net_io_counters()
    net_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 1))
    net_table.add_column("", style="dim", width=10)
    net_table.add_column("", width=25)
    net_table.add_row("Sent", f"{net.bytes_sent / 1e6:.1f} MB")
    net_table.add_row("Recv", f"{net.bytes_recv / 1e6:.1f} MB")

    # Combine all panels into one dashboard layout
    return Panel(
        Columns([
            Panel(cpu_table, title="CPU"),
            Panel(mem_table, title="Memory"),
            Panel(disk_table, title="Disk"),
            Panel(net_table, title="Network"),
        ]),
        title="[bold]System Monitor[/bold]",
        subtitle="Press Ctrl+C to exit"
    )

# Use Rich Live to refresh the dashboard every second
with Live(build_dashboard(), refresh_per_second=1) as live:
    while True:
        time.sleep(1)
        live.update(build_dashboard())
