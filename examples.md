# Package manager style
npm = PackageManagerSpinner('npm', 'installing dependencies')
npm.start()
# ... do work ...
npm.stop()

# Glow text
glow = GlowText("CYBER PUNK", glow_color='cyan', intensity=5)
glow.start()

# System update
manager = LoadingManager()
manager.system_update(['kernel', 'drivers', 'apps'])

# Matrix effect
matrix = MatrixCode(char_set='katakana', density=0.2)
matrix.start()
