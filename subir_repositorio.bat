@echo off
echo ========================================================
echo   SINCRONIZACION AUTOMATICA CON GITHUB
echo ========================================================
echo.
echo Este script subira todos los cambios locales al repositorio:
echo https://github.com/Pablo-app-developer/ANALISIS_COSTOS_CARDIOCENTRO_INTEGRAL_SAS-TDABC.git
echo.
echo 1. Inicializando repositorio git...
git init

echo 2. Configurando remoto...
git remote remove origin 2>nul
git remote add origin https://github.com/Pablo-app-developer/ANALISIS_COSTOS_CARDIOCENTRO_INTEGRAL_SAS-TDABC.git

echo 3. Agregando archivos...
git add .

echo 4. Creando commit...
git commit -m "Actualización Auto-Generada: Modelo TDABC con Matriz Cruzada y Capacidad 176h"

echo 5. Subiendo a GitHub (Rama main)...
echo    Nota: Si es la primera vez, pedira credenciales.
git branch -M main
git push -u origin main

echo.
echo ========================================================
echo   PROCESO COMPLETADO
echo ========================================================
pause
