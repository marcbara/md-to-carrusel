#!/bin/bash

echo "🚀 LinkedIn Carousel Generator"
echo

if [ $# -eq 0 ]; then
    echo "❌ Please provide a markdown file!"
    echo
    echo "💡 Usage: ./generate_carousel.sh 'your-file.md'"
    echo "📝 Example: ./generate_carousel.sh 'Marketing Report.md'"
    echo
    exit 1
fi

echo "📄 Processing: $1"
echo

python3 generate_carousel.py "$1"

echo
echo "✨ Done! Check the generated files." 