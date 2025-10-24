@echo off
echo ========================================
echo    🔧 Fixing NumPy/OpenCV Compatibility
echo ========================================
echo.

echo 🧹 Cleaning existing packages...
pip uninstall numpy opencv-python opencv-python-headless numba -y

echo.
echo 📦 Installing compatible versions...
echo Installing NumPy 1.24.4 (compatible with Python 3.13)...
pip install numpy==1.24.4 --only-binary=all

echo Installing OpenCV headless (no GUI dependencies)...
pip install opencv-python-headless==4.8.1.78

echo Installing compatible Numba...
pip install numba==0.58.1

echo.
echo 🧪 Testing compatibility...
python -c "import numpy; import cv2; import numba; print('✅ NumPy:', numpy.__version__); print('✅ OpenCV:', cv2.__version__); print('✅ Numba:', numba.__version__); print('✅ All modules working!')"

if errorlevel 1 (
    echo.
    echo ❌ Compatibility test failed!
    echo Trying alternative approach...
    echo.
    pip install numpy==1.21.6 --only-binary=all
    pip install opencv-python-headless==4.6.0.66
    pip install numba==0.56.4
    echo.
    python -c "import numpy; import cv2; import numba; print('✅ Alternative versions working!')"
)

echo.
echo ========================================
echo ✅ Fix completed! Try running start_vodcast.bat again
echo ========================================
pause

