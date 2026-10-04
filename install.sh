#!/usr/bin/env bash
set -e

APP_NAME="display-brightness-manager"
INSTALL_DIR="$HOME/.local/share/$APP_NAME"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "☀️ Installing $APP_NAME (Twinkle Tray for Linux)..."

# Dependency Checks
MISSING_DEPS=""
if ! command -v ddcutil >/dev/null 2>&1; then
    MISSING_DEPS="$MISSING_DEPS ddcutil i2c-tools"
fi
if ! command -v brightnessctl >/dev/null 2>&1; then
    MISSING_DEPS="$MISSING_DEPS brightnessctl"
fi

if [ -n "$MISSING_DEPS" ]; then
    echo "⚠️  Recommended packages missing:$MISSING_DEPS"
    echo "💡 You can install them by running: sudo apt install -y$MISSING_DEPS"
fi

# Ensure user is in i2c group for ddcutil non-root access
if groups "$USER" | grep -qv "\bi2c\b"; then
    echo "💡 Note: To control external monitors without sudo, ensure you are in the i2c group:"
    echo "   sudo usermod -aG i2c $USER (then log out and log back in)"
fi

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"

# Copy files
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -r "$SCRIPT_DIR/app.py" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/icon.svg" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/app.py"

# Symlink
ln -sf "$INSTALL_DIR/app.py" "$BIN_DIR/$APP_NAME"

# Desktop launcher
cat <<EOF > "$DESKTOP_DIR/$APP_NAME.desktop"
[Desktop Entry]
Type=Application
Name=Display Brightness Manager
GenericName=Brightness Slider (Twinkle Tray)
Comment=Control brightness of external and laptop monitors via DDC/CI
Exec=python3 $INSTALL_DIR/app.py
Icon=$INSTALL_DIR/icon.svg
Terminal=false
Categories=Settings;HardwareSettings;System;
Keywords=brightness;screen;monitor;display;twinkle;tray;ddcutil;hp;
StartupNotify=true
StartupWMClass=display-brightness-manager
EOF

chmod +x "$DESKTOP_DIR/$APP_NAME.desktop"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR" >/dev/null 2>&1 || true
fi

echo "✅ $APP_NAME installed successfully!"
echo "🚀 You can now find 'Display Brightness Manager' in your Start Menu or run '$APP_NAME' in terminal."
