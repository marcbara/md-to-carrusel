@echo off
echo 🚀 LinkedIn Carousel Generator
echo.

if "%1"=="" (
    echo ❌ Please provide a markdown file!
    echo.
    echo 💡 Usage: generate_carousel.bat "your-file.md"
    echo 📝 Example: generate_carousel.bat "Marketing Report.md"
    echo.
    pause
    exit /b 1
)

echo 📄 Processing: %1
echo.

python generate_carousel.py %1

echo.
echo ✨ Done! Check the generated files.
pause 