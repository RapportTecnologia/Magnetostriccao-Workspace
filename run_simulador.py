import os
import sys
import subprocess
from pathlib import Path


def choose_venv_location(base_dir: Path, simulador_dir: Path) -> Path:
    print("=== Simulador de Magnetostricção - Gerenciador de Ambiente ===")
    print(f"[PDCL:PLAN] Diretório base: {base_dir}")
    print(f"[PDCL:PLAN] Diretório do simulador: {simulador_dir}")
    print()
    print("Onde deseja manter o ambiente virtual (venv)?")
    print("  1) Pasta pai (raiz do workspace)")
    print("  2) Pasta do simulador")

    while True:
        choice = input("Seleção [1/2] (default=1): ").strip() or "1"
        if choice == "1":
            venv_dir = base_dir / "venv"
            print(f"[PDCL:DO] Usando venv na pasta pai: {venv_dir}")
            return venv_dir
        if choice == "2":
            venv_dir = simulador_dir / "venv"
            print(f"[PDCL:DO] Usando venv na pasta do simulador: {venv_dir}")
            return venv_dir
        print("[PDCL:CHECK] Opção inválida. Digite 1 ou 2.")


def ensure_venv(venv_dir: Path) -> None:
    python_exe = sys.executable
    if not (venv_dir / ("Scripts" if os.name == "nt" else "bin") / ("activate.bat" if os.name == "nt" else "activate")).exists():
        print(f"[PDCL:PLAN] venv não encontrada em {venv_dir}. Criando ambiente virtual...")
        subprocess.check_call([python_exe, "-m", "venv", str(venv_dir)])
        print(f"[PDCL:DO] venv criada em {venv_dir}")
    else:
        print(f"[PDCL:CHECK] venv encontrada em {venv_dir}")


def install_requirements(venv_dir: Path, simulador_dir: Path) -> None:
    scripts_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
    pip_exe = scripts_dir / ("pip.exe" if os.name == "nt" else "pip")

    req_base = simulador_dir / "scripts"
    req_windows = req_base / "requirements-windows.txt"
    req_default = req_base / "requirements.txt"

    if os.name == "nt":
        # Windows: instalar primeiro requirements-windows.txt (pin específico)
        # e depois requirements.txt (para dependências extras, como langchain_*)
        if not req_windows.exists() and not req_default.exists():
            print(f"[PDCL:WARNING] Nenhum arquivo de requirements encontrado em {req_base}")
            return

        if req_windows.exists():
            print(f"[PDCL:DO] Instalando dependências específicas do Windows a partir de {req_windows} ...")
            subprocess.check_call([str(pip_exe), "install", "-r", str(req_windows)])

        if req_default.exists():
            print(f"[PDCL:DO] Instalando dependências adicionais a partir de {req_default} ...")
            subprocess.check_call([str(pip_exe), "install", "-r", str(req_default)])

        print("[PDCL:CHECK] Dependências instaladas com sucesso")
    else:
        # Linux/macOS: usar apenas requirements.txt padrão
        if not req_default.exists():
            print(f"[PDCL:WARNING] Arquivo requirements.txt não encontrado em {req_base}")
            return

        print(f"[PDCL:DO] Instalando dependências a partir de {req_default} ...")
        subprocess.check_call([str(pip_exe), "install", "-r", str(req_default)])
        print("[PDCL:CHECK] Dependências instaladas com sucesso")


def run_simulador(venv_dir: Path, simulador_dir: Path, args: list[str]) -> int:
    scripts_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
    python_venv = scripts_dir / ("python.exe" if os.name == "nt" else "python")

    print("[PDCL:DO] Iniciando simulador...")
    cmd = [str(python_venv), "-m", "simulador"] + args
    return subprocess.call(cmd, cwd=str(simulador_dir))


def main(argv: list[str]) -> int:
    base_dir = Path(__file__).resolve().parent
    simulador_dir = base_dir / "simulador"

    if not simulador_dir.exists():
        print(f"[PDCL:LOG] ERRO: Diretório 'simulador' não encontrado em {base_dir}")
        return 1

    venv_dir = choose_venv_location(base_dir, simulador_dir)
    ensure_venv(venv_dir)
    install_requirements(venv_dir, simulador_dir)
    exit_code = run_simulador(venv_dir, simulador_dir, argv[1:])
    print("[PDCL:LOG] Simulador finalizado")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
