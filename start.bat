@echo off
color 0C

echo.
echo     _                  _            _            _               _            _              _   _        _   
echo    /\_\               / /\         /\ \         / /\            /\ \         /\ \     _    /\ \ /\ \     /\_\ 
echo   / / /         _    / /  \       /  \ \       / /  \          /  \ \       /  \ \   /\_\ /  \ \\ \ \   / / / 
echo   \ \ \__      /\_\ / / /\ \__   / /\ \ \     / / /\ \        / /\ \ \     / /\ \ \_/ / // /\ \ \\ \ \_/ / /  
echo    \ \___\    / / // / /\ \___\ / / /\ \_\   / / /\ \ \      / / /\ \_\   / / /\ \___/ // / /\ \ \\ \___/ /   
echo     \__  /   / / / \ \ \ \/___// /_/_ \/_/  / / /\ \_\ \    / /_/_ \/_/  / / /  \/____// / /  \ \_\\ \ \_/    
echo     / / /   / / /   \ \ \     / /____/\    / / /\ \ \___\  / /____/\    / / /    / / // / /    \/_/ \ \ \     
echo    / / /   / / /_    \ \ \   / /\____\/   / / /  \ \ \__/ / /\____\/   / / /    / / // / /           \ \ \    
echo   / / /___/ / //_/\__/ / /  / / /______  / / /____\_\ \  / / /______  / / /    / / // / /________     \ \ \   
echo  / / /____\/ / \ \/___/ /  / / /_______\/ / /__________\/ / /_______\/ / /    / / // / /_________\     \ \_\  
echo  \/_________/   \_____\/   \/__________/\/_____________/\/__________/\/_/     \/_/ \/____________/      \/_/  
echo                                                                                                                                                              
echo.

color 07
echo Bienvenue dans le programme USEBENCY - Gestion de cles USB chiffrees
echo ===================================================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installe. Veuillez installer Python et reessayer.
    pause
    exit /b
)

REM Vérifier et installer les dépendances
echo Verification et installation des dependances...
pip install colorama cryptography>nul 2>&1
if %errorlevel% neq 0 (
    echo Erreur lors de l'installation des dependances.
    pause
    exit /b
)

REM Vérifier si le script Python existe
if not exist "usebency.py" (
    echo Le fichier usebency.py n'a pas ete trouve.
    echo Assurez-vous qu'il est dans le meme repertoire que ce fichier batch.
    pause
    exit /b
)

echo Toutes les dependances sont installees.
echo.

REM Exécuter le programme Python avec des privilèges administrateur
echo Lancement de USEBENCY...
powershell Start-Process python -ArgumentList "usebency.py" -Verb RunAs

echo.
echo Si une fenetre d'elevation des privileges apparait, veuillez accepter.
echo.
