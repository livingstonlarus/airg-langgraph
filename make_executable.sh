#!/bin/bash
# Make Python scripts executable

chmod +x main.py
chmod +x test_app.py
chmod +x create_example_templates.py

echo "Scripts are now executable. You can run them directly:"
echo "./main.py --interactive"
echo "./test_app.py"
echo "./create_example_templates.py"