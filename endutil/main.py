from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.columns import Columns
import platform
import psutil
import socket
import distro
import os

console = Console()

def load_logos(filepath="logos.txt") -> dict:
    if not os.path.exists(filepath):
        return {}

    logos = {}
    current_distro = None
    logo_lines = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("###"):
                if current_distro and logo_lines:
                    logos[current_distro] = "\n".join(logo_lines).rstrip()
                    logo_lines = []
                current_distro = line.strip("# \n")
            else:
                logo_lines.append(line.rstrip())

        # Add last logo
        if current_distro and logo_lines:
            logos[current_distro] = "\n".join(logo_lines).rstrip()

    return logos

def get_cpu_name():
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    return line.strip().split(":")[1].strip()
    except Exception:
        return "Unknown CPU"

def get_uptime():
    from datetime import datetime
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    uptime = now - boot_time
    return str(uptime).split('.')[0]

def get_system_info():
    distro_name = distro.name(pretty=True)
    return {
        "OS": f"{platform.system()} {platform.release()}",
        "Hostname": socket.gethostname(),
        "Distro": distro_name,
        "Kernel": platform.version(),
        "CPU": get_cpu_name(),
        "Cores": str(psutil.cpu_count(logical=True)),
        "RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        "Uptime": get_uptime(),
    }

def get_logo_for_distro(logos: dict, distro_name: str) -> str:
    for name, logo in logos.items():
        if name.lower() in distro_name.lower():
            return logo
    return "🐧"  # fallback logo

def build_table(info: dict) -> Table:
    table = Table.grid(padding=(0, 1))
    table.add_column("Key", style="bold cyan", justify="right")
    table.add_column("Value", style="bold white")

    for key, value in info.items():
        table.add_row(f"{key}:", value)

    return table

def run():
    info = get_system_info()
    logos = load_logos()
    logo = get_logo_for_distro(logos, info["Distro"])
    table = build_table(info)

    logo_panel = Panel.fit(Text(logo, style="bold"), border_style="bright_black")
    info_panel = Panel.fit(table, title=":rocket: System Info", border_style="magenta")

    header = Align.center(Text("EndUtil", style="bold underline magenta", justify="center"))

    console.print("\n")
    console.print(header)
    console.print("\n")
    console.print(Columns([logo_panel, info_panel]))

if __name__ == "__main__":
    run()
