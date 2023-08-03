import sys
from cx_Freeze import setup, Executable

# O nome do seu script Python principal (o que contém o código principal)
script_principal = "main.py"

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use "Win32GUI" para aplicativos GUI no Windows

# Opções para a criação do executável
executables = [Executable(script_principal, base=base)]

# Outras opções (opcional)
build_exe_options = {
    "packages": ["tkinter","funcoes","sqlite3","tkcalendar"],  # Lista de pacotes adicionais (se necessário)
    "excludes": [],  # Lista de módulos/extras a serem excluídos (se necessário)
}

# Configuração da criação do executável
setup(
    name="Gerenciador De Entregas",
    version="1.1",
    description="Gerencia entregas com sqlite e python Criado por William Souza",
    options={"build_exe": build_exe_options},
    executables=executables
)
