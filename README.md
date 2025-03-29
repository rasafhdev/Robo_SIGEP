# 🤖 Automação SIGEP - Consulta Financeira

## 👨‍💻 Autor  
**Rodrigo Asafh 🕎**  
📅 Última versão: 29/03/2025  
📧 Contato:  
- LinkedIn: [linkedin.com/in/rodrigoasafh](https://linkedin.com/in/rodrigoasafh)  
- E-mail: [rasafh.dev@gmail.com](mailto:rasafh.dev@gmail.com)  

---

## 📌 Descrição  
Sistema de automação que realiza consultas financeiras no SIGEP, baixa contracheques em PDF e os organiza automaticamente, com suporte a autenticação por MFA via e-mail.  

### ⚠️ Nota Legal  
Os passos codificados nesta automação replicam **exatamente as ações humanas legítimas**. Portanto:  
✔️ Não envolve invasão ou bypass de segurança  
✔️ Não viola termos de serviço  
✔️ Opera dentro da interface pública do sistema  

---

## 🔧 Funcionalidades  
| Feature                  | Descrição                                 |  
|--------------------------|-------------------------------------------|  
| **Login automático**     | Credenciais via `.env` + MFA por e-mail   |  
| **Navegação**            | Seleção inteligente de órgãos             |  
| **Download**             | Baixa arquivo automáticamente.            |
| **Impressão**            | Faz a impressão automáticamente.          |
| **Organização**          | Captura mês+ano dinamicamente, para montar o nome do arquivo e salvar histórico em pasta específica.|
| **Build executável**     | Pacote standalone com `cx_Freeze`         |  

---

## ⚙️ Stack Tecnológica  
```python
# Core
- Selenium (WebDriver)  # Automação web
- IMAPLib               # Captura de MFA
- PyAutoGUI             # Interação com GUI
- cx_Freeze             # Build de executável
```
## ⚙️ Utilitários
```
- python-dotenv         # Gerenciamento de secrets
- shutil                # Manipulação de arquivos
```
## 📂 Estrutura do Código
```
robo_sigep/
├── main.py            # Código cliente
├── sigep.py           # Lógica principal
├── scrapper.py        # Módulo de e-mail (MFA)
├── setup.py           # Configuração do build
├── res/
│   └── icon.ico       # Ícone do aplicativo
```

🚀 Como Usar
```
Pré-requisitos
Chrome ≥ 120
Python 3.12.5+

# Instalação

pip install -r requirements.txt
cp .env.example .env  # Configure suas credenciais


# Execução
python automacao.py   # Modo desenvolvimento
python setup.py build # Gerar executável
```

# 📜 Licença
```
MIT License - Uso livre mediante:
✔️ Menção ao autor original
✔️ Manutenção do copyright
✖️ Proibido uso comercial sem autorização explícita
ℹ️ Para usos além da licença padrão, contate o autor.
```
