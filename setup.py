from cx_Freeze import setup, Executable

# Dependências adicionais, se necessário
build_exe_options = {
    "packages": ["os",
                 "selenium",
                 "selenium.webdriver",
                 "time",
                 "datetime",
                 "dataclasses",
                 "shutil",
                 "dotenv",
                 "pyautogui",
                ],  # Pacotes necessários
    
    "includes": ["scrapper",
                 "sigep",
                 ],  # Módulos adicionais
    
    "include_files": ["res/"]  # Diretório "res" com arquivos necessários
}

# Caminho para o ícone (substitua 'icon.ico' pelo caminho correto do seu arquivo de ícone)
setup(
    name="Robo SIGEP",
    version="1.0",
    description="Automação capturar contracheque",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=None, icon="res/icon.ico")],  # Aqui você adiciona o ícone
)
