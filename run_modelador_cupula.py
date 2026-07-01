import os
import sys
import subprocess
from pathlib import Path


def choose_venv_location(base_dir: Path, modelador_dir: Path) -> Path:
    print("=== Modelador de Cúpula Acústica - Gerenciador de Ambiente ===")
    print(f"[PDCL:PLAN] Diretório base: {base_dir}")
    print(f"[PDCL:PLAN] Diretório do modelador: {modelador_dir}")
    print()
    print("Onde deseja manter o ambiente virtual (venv)?")
    print("  1) Pasta pai (raiz do workspace)")
    print("  2) Pasta do modelador-cupula")

    while True:
        choice = input("Seleção [1/2] (default=1): ").strip() or "1"
        if choice == "1":
            venv_dir = base_dir / "venv"
            print(f"[PDCL:DO] Usando venv na pasta pai: {venv_dir}")
            return venv_dir
        if choice == "2":
            venv_dir = modelador_dir / "venv"
            print(f"[PDCL:DO] Usando venv na pasta do modelador: {venv_dir}")
            return venv_dir
        print("[PDCL:CHECK] Opção inválida. Digite 1 ou 2.")


def ensure_venv(venv_dir: Path) -> None:
    python_exe = sys.executable
    activate_path = (
        venv_dir / ("Scripts" if os.name == "nt" else "bin") / ("activate.bat" if os.name == "nt" else "activate")
    )
    if not activate_path.exists():
        print(f"[PDCL:PLAN] venv não encontrada em {venv_dir}. Criando ambiente virtual...")
        subprocess.check_call([python_exe, "-m", "venv", str(venv_dir)])
        print(f"[PDCL:DO] venv criada em {venv_dir}")
    else:
        print(f"[PDCL:CHECK] venv encontrada em {venv_dir}")


def install_requirements(venv_dir: Path, modelador_dir: Path) -> None:
    scripts_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
    pip_exe = scripts_dir / ("pip.exe" if os.name == "nt" else "pip")

    req_file = modelador_dir / "requirements.txt"

    if not req_file.exists():
        print(f"[PDCL:WARNING] Arquivo requirements.txt não encontrado em {modelador_dir}")
        return

    print(f"[PDCL:DO] Instalando/atualizando dependências a partir de {req_file} ...")
    subprocess.check_call([str(pip_exe), "install", "--upgrade", "pip"])
    subprocess.check_call([str(pip_exe), "install", "-r", str(req_file)])
    print("[PDCL:CHECK] Dependências instaladas com sucesso")


def run_modelador(venv_dir: Path, modelador_dir: Path, args: list[str]) -> int:
    scripts_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
    python_venv = scripts_dir / ("python.exe" if os.name == "nt" else "python")

    print("[PDCL:DO] Iniciando Modelador de Cúpula Acústica...")
    # Executa o run.py do subprojeto usando o Python do venv
    cmd = [str(python_venv), "run.py"] + args
    return subprocess.call(cmd, cwd=str(modelador_dir))


def main(argv: list[str]) -> int:
    base_dir = Path(__file__).resolve().parent
    modelador_dir = base_dir / "modelador-cupula"

    if not modelador_dir.exists():
        print(f"[PDCL:LOG] ERRO: Diretório 'modelador-cupula' não encontrado em {base_dir}")
        return 1

    venv_dir = choose_venv_location(base_dir, modelador_dir)
    ensure_venv(venv_dir)
    install_requirements(venv_dir, modelador_dir)
    exit_code = run_modelador(venv_dir, modelador_dir, argv[1:])
    print("[PDCL:LOG] Modelador finalizado")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
