# Atualizado em: 29/09/2024
# Lembre de executar o PowerShell como administrador!

# Muda a diretiva de execução de "Restricted" para permitir a execução de extensões .ps1 no PowerShell.
Set-ExecutionPolicy AllSigned
Set-ExecutionPolicy RemoteSigned

# Instalação de dependências em sistemas Windows:
winget install python
winget install Microsoft.VCRedist.2015+.x64 # Pacotes do Microsof Visual C++ 2015-2022 para sistema x64.
pip install pillow
pip install jes4py # Se surgir erro nessa etapa, reinicie após instalar o Microsof Visual C++ 2015-2022.

# Testado em Windows 11 Home.