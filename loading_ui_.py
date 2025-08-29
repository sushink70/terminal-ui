#!/usr/bin/env python3
"""
Advanced Terminal Animation Library
Comprehensive collection of terminal animations including package manager styles,
text effects (glow, fade, wave), loading indicators, and system update animations.
Features 256-color support, RGB colors, and advanced ANSI escape sequences.
"""

import time
import sys
import threading
import random
import itertools
import math
import os
import shutil
from typing import Optional, List, Callable, Any, Dict, Tuple
from dataclasses import dataclass

class Colors:
    """Extended ANSI color codes including 256-color and RGB support"""
    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Styles
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    STRIKETHROUGH = '\033[9m'
    
    @staticmethod
    def rgb(r: int, g: int, b: int) -> str:
        """Create RGB color escape sequence"""
        return f'\033[38;2;{r};{g};{b}m'
    
    @staticmethod
    def bg_rgb(r: int, g: int, b: int) -> str:
        """Create RGB background color escape sequence"""
        return f'\033[48;2;{r};{g};{b}m'
    
    @staticmethod
    def color_256(n: int) -> str:
        """Use 256-color palette"""
        return f'\033[38;5;{n}m'
    
    @staticmethod
    def bg_color_256(n: int) -> str:
        """Use 256-color palette for background"""
        return f'\033[48;5;{n}m'

class TerminalUtils:
    """Utility functions for terminal control"""
    
    @staticmethod
    def clear_screen():
        """Clear the entire screen"""
        print('\033[2J\033[H', end='')
    
    @staticmethod
    def clear_line():
        """Clear current line"""
        print('\033[2K', end='')
    
    @staticmethod
    def move_cursor(x: int, y: int):
        """Move cursor to position"""
        print(f'\033[{y};{x}H', end='')
    
    @staticmethod
    def move_cursor_up(n: int = 1):
        """Move cursor up n lines"""
        print(f'\033[{n}A', end='')
    
    @staticmethod
    def move_cursor_down(n: int = 1):
        """Move cursor down n lines"""
        print(f'\033[{n}B', end='')
    
    @staticmethod
    def hide_cursor():
        """Hide cursor"""
        print('\033[?25l', end='')
    
    @staticmethod
    def show_cursor():
        """Show cursor"""
        print('\033[?25h', end='')
    
    @staticmethod
    def get_terminal_size() -> Tuple[int, int]:
        """Get terminal width and height"""
        return shutil.get_terminal_size()

class TerminalAnimator:
    """Enhanced base class for all terminal animations"""
    
    def __init__(self, color: str = Colors.CYAN, speed: float = 0.1):
        self.color = color
        self.speed = speed
        self.running = False
        self.thread = None
        
    def start(self):
        """Start the animation in a separate thread"""
        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop the animation"""
        self.running = False
        if self.thread:
            self.thread.join()
        self._cleanup()
        
    def _animate(self):
        """Override this method in subclasses"""
        pass
        
    def _cleanup(self):
        """Clean up after animation stops"""
        TerminalUtils.clear_line()
        print('\r', end='', flush=True)

class PackageManagerSpinner(TerminalAnimator):
    """Package manager style loading animations"""
    
    PACKAGE_MANAGERS = {
        'npm': {
            'spinner': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
            'color': Colors.RED,
            'prefix': 'npm',
            'messages': ['Installing dependencies', 'Resolving packages', 'Building project']
        },
        'yarn': {
            'spinner': ['◐', '◓', '◑', '◒'],
            'color': Colors.BLUE,
            'prefix': 'yarn',
            'messages': ['Installing packages', 'Resolving dependencies', 'Building bundles']
        },
        'pnpm': {
            'spinner': ['●', '○', '◉', '○'],
            'color': Colors.YELLOW,
            'prefix': 'pnpm',
            'messages': ['Installing from store', 'Linking dependencies', 'Running scripts']
        },
        'bun': {
            'spinner': ['🌕', '🌖', '🌗', '🌘', '🌑', '🌒', '🌓', '🌔'],
            'color': Colors.MAGENTA,
            'prefix': 'bun',
            'messages': ['Installing at light speed', 'Bundling assets', 'Optimizing build']
        },
        'cargo': {
            'spinner': ['▱▱▱', '▰▱▱', '▰▰▱', '▰▰▰', '▱▰▰', '▱▱▰', '▱▱▱'],
            'color': Colors.rgb(222, 165, 132),
            'prefix': 'cargo',
            'messages': ['Compiling crates', 'Building dependencies', 'Linking binaries']
        },
        'apt': {
            'spinner': ['[    ]', '[=   ]', '[==  ]', '[=== ]', '[====]', '[ ===]', '[  ==]', '[   =]'],
            'color': Colors.GREEN,
            'prefix': 'apt',
            'messages': ['Updating package lists', 'Installing packages', 'Configuring system']
        },
        'snap': {
            'spinner': ['◜', '◠', '◝', '◞', '◡', '◟'],
            'color': Colors.rgb(0, 179, 152),
            'prefix': 'snap',
            'messages': ['Downloading snap', 'Mounting snap', 'Installing snap']
        },
        'pip': {
            'spinner': ['-', '\\', '|', '/'],
            'color': Colors.GREEN,
            'prefix': 'pip',
            'messages': ['Installing packages', 'Resolving dependencies', 'Downloading wheels']
        },
        'brew': {
            'spinner': ['🍺', '🍻', '🥂', '🍷'],
            'color': Colors.YELLOW,
            'prefix': 'brew',
            'messages': ['Brewing formulas', 'Pouring bottles', 'Updating taps']
        },
        'pacman': {
            'spinner': ['<', '=', '>'],
            'color': Colors.CYAN,
            'prefix': 'pacman',
            'messages': ['Syncing databases', 'Installing packages', 'Resolving conflicts']
        }
    }
    
    def __init__(self, pm_type: str = 'npm', custom_message: str = None, **kwargs):
        pm_config = self.PACKAGE_MANAGERS.get(pm_type, self.PACKAGE_MANAGERS['npm'])
        super().__init__(color=pm_config['color'], **kwargs)
        self.spinner = pm_config['spinner']
        self.prefix = pm_config['prefix']
        self.messages = pm_config['messages']
        self.current_message = custom_message or random.choice(self.messages)
        
    def _animate(self):
        spinner_cycle = itertools.cycle(self.spinner)
        message_timer = 0
        
        while self.running:
            char = next(spinner_cycle)
            
            # Change message occasionally
            message_timer += 1
            if message_timer > 50:  # Change every ~5 seconds
                self.current_message = random.choice(self.messages)
                message_timer = 0
            
            print(f"\r{self.color}{char} {self.prefix}: {self.current_message}...{Colors.RESET}", 
                  end='', flush=True)
            time.sleep(self.speed)

class GlowText(TerminalAnimator):
    """Text with glow effect using color gradients"""
    
    def __init__(self, text: str, glow_color: str = 'cyan', intensity: int = 3, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.glow_color = glow_color
        self.intensity = intensity
        self.glow_colors = self._generate_glow_gradient()
        
    def _generate_glow_gradient(self) -> List[str]:
        """Generate gradient colors for glow effect"""
        if self.glow_color == 'cyan':
            return [Colors.color_256(51), Colors.color_256(45), Colors.color_256(39), 
                   Colors.color_256(33), Colors.color_256(27)]
        elif self.glow_color == 'red':
            return [Colors.color_256(196), Colors.color_256(160), Colors.color_256(124), 
                   Colors.color_256(88), Colors.color_256(52)]
        elif self.glow_color == 'green':
            return [Colors.color_256(46), Colors.color_256(40), Colors.color_256(34), 
                   Colors.color_256(28), Colors.color_256(22)]
        elif self.glow_color == 'purple':
            return [Colors.color_256(129), Colors.color_256(93), Colors.color_256(57), 
                   Colors.color_256(21), Colors.color_256(19)]
        else:
            return [Colors.BRIGHT_WHITE, Colors.WHITE, Colors.DIM]
    
    def _animate(self):
        pulse_cycle = 0
        while self.running:
            intensity_factor = (math.sin(pulse_cycle) + 1) / 2  # 0 to 1
            color_index = int(intensity_factor * (len(self.glow_colors) - 1))
            
            glow_color = self.glow_colors[color_index]
            
            # Create glow effect with spaces
            glow_text = f"  {glow_color}{Colors.BOLD}{self.text}{Colors.RESET}  "
            print(f"\r{glow_text}", end='', flush=True)
            
            pulse_cycle += 0.2
            time.sleep(self.speed)

class FadeText(TerminalAnimator):
    """Text with fade in/out effect"""
    
    def __init__(self, text: str, fade_type: str = 'in_out', **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.fade_type = fade_type
        
    def _animate(self):
        fade_levels = [
            Colors.color_256(235),  # Very dark
            Colors.color_256(237),
            Colors.color_256(239),
            Colors.color_256(241),
            Colors.color_256(243),
            Colors.color_256(245),
            Colors.color_256(247),
            Colors.color_256(249),
            Colors.color_256(251),
            Colors.BRIGHT_WHITE     # Brightest
        ]
        
        while self.running:
            # Fade in
            for level in fade_levels:
                if not self.running:
                    break
                print(f"\r{level}{self.text}{Colors.RESET}", end='', flush=True)
                time.sleep(self.speed)
            
            if self.fade_type == 'in_out':
                # Fade out
                for level in reversed(fade_levels):
                    if not self.running:
                        break
                    print(f"\r{level}{self.text}{Colors.RESET}", end='', flush=True)
                    time.sleep(self.speed)

class WaveText(TerminalAnimator):
    """Text with wave animation effect"""
    
    def __init__(self, text: str, wave_colors: List[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.wave_colors = wave_colors or [
            Colors.rgb(255, 0, 127),   # Pink
            Colors.rgb(255, 127, 0),   # Orange  
            Colors.rgb(255, 255, 0),   # Yellow
            Colors.rgb(127, 255, 0),   # Light green
            Colors.rgb(0, 255, 127),   # Cyan-green
            Colors.rgb(0, 127, 255),   # Light blue
            Colors.rgb(127, 0, 255),   # Purple
        ]
        
    def _animate(self):
        wave_offset = 0
        while self.running:
            colored_text = ""
            for i, char in enumerate(self.text):
                if char == ' ':
                    colored_text += char
                    continue
                    
                # Calculate wave position
                wave_pos = (i + wave_offset) % len(self.wave_colors)
                color = self.wave_colors[wave_pos]
                colored_text += f"{color}{char}"
            
            print(f"\r{colored_text}{Colors.RESET}", end='', flush=True)
            wave_offset += 1
            time.sleep(self.speed)

class FireText(TerminalAnimator):
    """Text with fire effect using red/orange/yellow colors"""
    
    def __init__(self, text: str, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.fire_chars = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█', '▇', '▆', '▅', '▄', '▃', '▂']
        self.fire_colors = [
            Colors.rgb(255, 0, 0),     # Red
            Colors.rgb(255, 69, 0),    # Red-orange
            Colors.rgb(255, 140, 0),   # Dark orange
            Colors.rgb(255, 165, 0),   # Orange
            Colors.rgb(255, 215, 0),   # Gold
            Colors.rgb(255, 255, 0),   # Yellow
        ]
        
    def _animate(self):
        while self.running:
            fire_text = ""
            for i, char in enumerate(self.text):
                if char == ' ':
                    fire_text += char
                    continue
                    
                # Random fire effect
                fire_char = random.choice(self.fire_chars)
                fire_color = random.choice(self.fire_colors)
                fire_text += f"{fire_color}{fire_char}"
            
            print(f"\r{fire_text}{Colors.RESET}", end='', flush=True)
            time.sleep(self.speed)

class NeonText(TerminalAnimator):
    """Neon sign effect with flickering"""
    
    def __init__(self, text: str, neon_color: str = 'cyan', **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.neon_color = neon_color
        
    def _animate(self):
        while self.running:
            # Bright neon
            if self.neon_color == 'cyan':
                bright = Colors.rgb(0, 255, 255)
                dim = Colors.rgb(0, 128, 128)
            elif self.neon_color == 'pink':
                bright = Colors.rgb(255, 0, 255)
                dim = Colors.rgb(128, 0, 128)
            elif self.neon_color == 'green':
                bright = Colors.rgb(0, 255, 0)
                dim = Colors.rgb(0, 128, 0)
            else:
                bright = Colors.BRIGHT_WHITE
                dim = Colors.WHITE
            
            # Occasional flicker
            if random.random() < 0.1:
                color = dim if random.random() < 0.5 else Colors.DIM
                flicker_text = f"{color}{self.text}{Colors.RESET}"
            else:
                flicker_text = f"{bright}{Colors.BOLD}{self.text}{Colors.RESET}"
            
            print(f"\r{flicker_text}", end='', flush=True)
            time.sleep(self.speed)

class TypewriterEffect(TerminalAnimator):
    """Enhanced typewriter with cursor and realistic timing"""
    
    def __init__(self, text: str, cursor_char: str = '|', realistic_timing: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.cursor_char = cursor_char
        self.realistic_timing = realistic_timing
        
    def _animate(self):
        current_text = ""
        cursor_visible = True
        
        for char in self.text:
            if not self.running:
                break
                
            current_text += char
            
            # Show current text with cursor
            display_text = current_text
            if cursor_visible:
                display_text += f"{Colors.BLINK}{self.cursor_char}{Colors.RESET}"
            
            print(f"\r{self.color}{display_text}{Colors.RESET}", end='', flush=True)
            
            # Realistic typing delays
            if self.realistic_timing:
                if char == ' ':
                    delay = self.speed * 0.5
                elif char in '.,!?':
                    delay = self.speed * 3
                elif char in '\n':
                    delay = self.speed * 5
                else:
                    delay = self.speed + random.uniform(-0.02, 0.05)
            else:
                delay = self.speed
                
            time.sleep(max(0.01, delay))
        
        # Final display without cursor
        print(f"\r{self.color}{current_text}{Colors.RESET}")

class SystemUpdateAnimation(TerminalAnimator):
    """Linux system update style animation"""
    
    def __init__(self, packages: List[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.packages = packages or [
            'linux-headers', 'gcc', 'python3', 'nodejs', 'git', 'vim', 
            'curl', 'wget', 'htop', 'neofetch', 'docker', 'nginx'
        ]
        self.current_package = 0
        self.progress = 0
        
    def _animate(self):
        total_packages = len(self.packages)
        
        while self.running and self.current_package < total_packages:
            package = self.packages[self.current_package]
            
            # Show current package being processed
            print(f"\r{Colors.GREEN}[{self.current_package + 1}/{total_packages}]"
                  f"{Colors.RESET} Processing {Colors.BOLD}{package}{Colors.RESET}...", 
                  end='', flush=True)
            
            # Simulate processing time
            time.sleep(random.uniform(0.5, 2.0))
            
            # Show completion
            print(f"\r{Colors.GREEN}[{self.current_package + 1}/{total_packages}]"
                  f"{Colors.RESET} ✓ {Colors.BOLD}{package}{Colors.RESET} installed")
            
            self.current_package += 1
            
        if self.running:
            print(f"{Colors.BRIGHT_GREEN}✓ All packages updated successfully!{Colors.RESET}")

class ProgressIndicator(TerminalAnimator):
    """Advanced progress indicator with ETA and speed"""
    
    def __init__(self, total: int = 100, width: int = 40, 
                 style: str = 'blocks', show_speed: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.total = total
        self.width = width
        self.style = style
        self.show_speed = show_speed
        self.current = 0
        self.start_time = None
        self.last_update_time = None
        self.speeds = []
        
        self.styles = {
            'blocks': {'fill': '█', 'empty': '░'},
            'arrows': {'fill': '▶', 'empty': '▷'},
            'dots': {'fill': '●', 'empty': '○'},
            'lines': {'fill': '═', 'empty': '─'},
            'gradient': {'fill': ['▏', '▎', '▍', '▌', '▋', '▊', '▉', '█'], 'empty': ' '}
        }
        
    def update(self, value: int):
        """Update progress"""
        if self.start_time is None:
            self.start_time = time.time()
            
        current_time = time.time()
        
        # Calculate speed
        if self.last_update_time and value > self.current:
            time_diff = current_time - self.last_update_time
            items_diff = value - self.current
            speed = items_diff / time_diff if time_diff > 0 else 0
            self.speeds.append(speed)
            if len(self.speeds) > 10:  # Keep last 10 measurements
                self.speeds.pop(0)
                
        self.current = min(value, self.total)
        self.last_update_time = current_time
        self._draw()
        
    def _draw(self):
        percentage = (self.current / self.total) * 100
        filled_width = int((self.current / self.total) * self.width)
        
        style_config = self.styles.get(self.style, self.styles['blocks'])
        
        if self.style == 'gradient' and isinstance(style_config['fill'], list):
            # Gradient style
            bar = '█' * filled_width + ' ' * (self.width - filled_width)
        else:
            bar = style_config['fill'] * filled_width + style_config['empty'] * (self.width - filled_width)
        
        output = f"\r{self.color}[{bar}]{Colors.RESET} {percentage:5.1f}%"
        
        # Add current/total
        output += f" ({self.current}/{self.total})"
        
        # Add speed if enabled
        if self.show_speed and self.speeds:
            avg_speed = sum(self.speeds) / len(self.speeds)
            output += f" Speed: {avg_speed:.1f}/s"
        
        # Add ETA
        if self.current > 0 and self.start_time:
            elapsed = time.time() - self.start_time
            if self.current < self.total:
                eta = (elapsed / self.current) * (self.total - self.current)
                output += f" ETA: {eta:.0f}s"
        
        print(output, end='', flush=True)

class MatrixCode(TerminalAnimator):
    """Enhanced Matrix digital rain with customization"""
    
    def __init__(self, width: int = None, height: int = None, 
                 char_set: str = 'matrix', density: float = 0.1, **kwargs):
        super().__init__(**kwargs)
        terminal_width, terminal_height = TerminalUtils.get_terminal_size()
        self.width = width or terminal_width
        self.height = height or terminal_height - 2
        
        self.char_sets = {
            'matrix': '0123456789ABCDEF',
            'binary': '01',
            'katakana': 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン',
            'hex': '0123456789ABCDEF',
            'symbols': '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }
        
        self.characters = self.char_sets.get(char_set, char_set)
        self.density = density
        self.drops = [0] * self.width
        self.lengths = [random.randint(5, 15) for _ in range(self.width)]
        
    def _animate(self):
        TerminalUtils.hide_cursor()
        TerminalUtils.clear_screen()
        
        try:
            while self.running:
                TerminalUtils.move_cursor(1, 1)
                
                # Create matrix effect
                for y in range(self.height):
                    line = ""
                    for x in range(self.width):
                        if y == self.drops[x]:
                            # Bright leading character
                            line += f"{Colors.BRIGHT_WHITE}{random.choice(self.characters)}"
                        elif y < self.drops[x] and y > self.drops[x] - self.lengths[x]:
                            # Fading trail
                            trail_pos = self.drops[x] - y
                            if trail_pos < 3:
                                line += f"{Colors.BRIGHT_GREEN}{random.choice(self.characters)}"
                            elif trail_pos < 6:
                                line += f"{Colors.GREEN}{random.choice(self.characters)}"
                            else:
                                line += f"{Colors.DIM}{Colors.GREEN}{random.choice(self.characters)}"
                        else:
                            line += " "
                    print(f"{line}{Colors.RESET}")
                
                # Update drops
                for i in range(len(self.drops)):
                    if self.drops[i] > self.height + self.lengths[i] and random.random() > (1 - self.density):
                        self.drops[i] = 0
                        self.lengths[i] = random.randint(5, 15)
                    else:
                        self.drops[i] += 1
                
                time.sleep(self.speed)
                
        finally:
            TerminalUtils.show_cursor()

class DecryptText(TerminalAnimator):
    """Text that decrypts from random characters"""
    
    def __init__(self, text: str, iterations: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.iterations = iterations
        self.chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()'
        
    def _animate(self):
        current = list(random.choice(self.chars) for _ in self.text)
        
        for _ in range(self.iterations):
            if not self.running:
                break
            for i in range(len(self.text)):
                if random.random() < 0.1:  # 10% chance to decrypt each char per iteration
                    current[i] = self.text[i]
            print(f"\r{self.color}{''.join(current)}{Colors.RESET}", end='', flush=True)
            time.sleep(self.speed)
        
        # Final text
        print(f"\r{self.color}{self.text}{Colors.RESET}")

class ScrollText(TerminalAnimator):
    """Text that scrolls left to right"""
    
    def __init__(self, text: str, width: int = 20, direction: str = 'left', **kwargs):
        super().__init__(**kwargs)
        self.text = text + ' ' * width  # Pad for scrolling
        self.width = width
        self.direction = direction
        self.offset = 0
        
    def _animate(self):
        while self.running:
            display = self.text[self.offset:self.offset + self.width]
            if len(display) < self.width:
                display += self.text[:self.width - len(display)]
            print(f"\r{self.color}{display}{Colors.RESET}", end='', flush=True)
            
            if self.direction == 'left':
                self.offset = (self.offset + 1) % len(self.text)
            else:
                self.offset = (self.offset - 1) % len(self.text)
            time.sleep(self.speed)

class BounceText(TerminalAnimator):
    """Text that bounces back and forth"""
    
    def __init__(self, text: str, width: int = 40, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.width = width - len(text)
        self.position = 0
        self.direction = 1
        
    def _animate(self):
        while self.running:
            padding_left = ' ' * self.position
            padding_right = ' ' * (self.width - self.position)
            print(f"\r{padding_left}{self.color}{self.text}{Colors.RESET}{padding_right}", end='', flush=True)
            
            self.position += self.direction
            if self.position >= self.width or self.position <= 0:
                self.direction *= -1
            time.sleep(self.speed)

class AsciiArtAnimator(TerminalAnimator):
    """Plays ASCII art animation frames"""
    
    def __init__(self, frames: List[str], **kwargs):
        super().__init__(**kwargs)
        self.frames = frames
        
    def _animate(self):
        cycle = itertools.cycle(self.frames)
        while self.running:
            frame = next(cycle)
            lines = frame.split('\n')
            TerminalUtils.clear_screen()
            for line in lines:
                print(f"{self.color}{line}{Colors.RESET}")
            time.sleep(self.speed)

class LoadingManager:
    """Enhanced loading manager with more package manager styles"""
    
    def __init__(self):
        self.current_animation = None
        
    def npm_install(self, packages: List[str], duration: float = 3):
        """Simulate npm install with realistic output"""
        spinner = PackageManagerSpinner('npm', f"installing {len(packages)} packages")
        spinner.start()
        time.sleep(duration)
        spinner.stop()
        
        print(f"{Colors.GREEN}✓{Colors.RESET} Installed {len(packages)} packages")
        return True
        
    def system_update(self, packages: List[str] = None):
        """Simulate Linux system update"""
        if packages is None:
            packages = ['linux-headers', 'gcc', 'python3', 'nodejs', 'git']
            
        updater = SystemUpdateAnimation(packages)
        updater.start()
        time.sleep(0.1)  # Let it start
        
        # Wait for completion
        while updater.running:
            time.sleep(0.1)
            
        return True
    
    def cargo_build(self, duration: float = 5):
        """Simulate Rust cargo build"""
        spinner = PackageManagerSpinner('cargo', 'Building release binary')
        spinner.start()
        time.sleep(duration)
        spinner.stop()
        
        print(f"{Colors.GREEN}✓{Colors.RESET} Build completed successfully")
        return True
    
    def pip_install(self, packages: List[str], duration: float = 3):
        """Simulate pip install"""
        spinner = PackageManagerSpinner('pip', f"installing {len(packages)} packages")
        spinner.start()
        time.sleep(duration)
        spinner.stop()
        
        print(f"{Colors.GREEN}✓{Colors.RESET} Installed {len(packages)} packages")
        return True
    
    def brew_install(self, packages: List[str], duration: float = 3):
        """Simulate brew install"""
        spinner = PackageManagerSpinner('brew', f"installing {len(packages)} formulas")
        spinner.start()
        time.sleep(duration)
        spinner.stop()
        
        print(f"{Colors.GREEN}✓{Colors.RESET} Brewed {len(packages)} formulas")
        return True

# Demo functions with all new effects
def demo_package_managers():
    """Demo all package manager animations"""
    print(f"{Colors.BOLD}Package Manager Animations{Colors.RESET}\n")
    
    managers = ['npm', 'yarn', 'pnpm', 'bun', 'cargo', 'apt', 'snap', 'pip', 'brew', 'pacman']
    
    for pm in managers:
        print(f"Testing {pm}:")
        spinner = PackageManagerSpinner(pm)
        spinner.start()
        time.sleep(2)
        spinner.stop()
        print(f" {Colors.GREEN}✓{Colors.RESET} Complete\n")

def demo_text_effects():
    """Demo advanced text effects"""
    print(f"{Colors.BOLD}Advanced Text Effects{Colors.RESET}\n")
    
    # Glow effect
    print("Glow Effect:")
    glow = GlowText("GLOWING TEXT", glow_color='cyan', speed=0.05)
    glow.start()
    time.sleep(3)
    glow.stop()
    print("\n")
    
    # Neon effect
    print("Neon Effect:")
    neon = NeonText("NEON SIGN", neon_color='pink', speed=0.1)
    neon.start()
    time.sleep(3)
    neon.stop()
    print("\n")
    
    # Fire effect
    print("Fire Effect:")
    fire = FireText("FIRE TEXT", speed=0.1)
    fire.start()
    time.sleep(3)
    fire.stop()
    print("\n")
    
    # Wave effect
    print("Wave Effect:")
    wave = WaveText("RAINBOW WAVE", speed=0.1)
    wave.start()
    time.sleep(3)
    wave.stop()
    print("\n")
    
    # Decrypt effect
    print("Decrypt Effect:")
    decrypt = DecryptText("SECRET MESSAGE", speed=0.05)
    decrypt.start()
    time.sleep(3)
    while decrypt.running:
        time.sleep(0.1)
    print("\n")
    
    # Scroll effect
    print("Scroll Effect:")
    scroll = ScrollText("SCROLLING TEXT MESSAGE", width=20, speed=0.1)
    scroll.start()
    time.sleep(3)
    scroll.stop()
    print("\n")
    
    # Bounce effect
    print("Bounce Effect:")
    bounce = BounceText("BOUNCING", width=30, speed=0.05)
    bounce.start()
    time.sleep(3)
    bounce.stop()
    print("\n")

def demo_enhanced_typewriter():
    """Demo enhanced typewriter effect"""
    print(f"{Colors.BOLD}Enhanced Typewriter Effect{Colors.RESET}\n")
    
    text = "This is a realistic typewriter effect with variable timing, punctuation pauses, and a blinking cursor."
    
    typewriter = TypewriterEffect(text, color=Colors.GREEN, speed=0.05, realistic_timing=True)
    typewriter.start()
    time.sleep(0.1)  # Let it start
    
    # Wait for completion
    while typewriter.running:
        time.sleep(0.1)
    
    print("\n")

def demo_system_operations():
    """Demo system operation animations"""
    print(f"{Colors.BOLD}System Operations{Colors.RESET}\n")
    
    # System update
    print("System Update:")
    manager = LoadingManager()
    manager.system_update()
    print("\n")
    
    # Progress indicator
    print("Progress Indicator:")
    progress = ProgressIndicator(total=100, style='blocks', speed=0.05)
    for i in range(0, 101, 5):
        progress.update(i)
        time.sleep(0.2)
    print("\n")
    
    # Matrix code
    print("Matrix Code:")
    matrix = MatrixCode(speed=0.05)
    matrix.start()
    time.sleep(3)
    matrix.stop()
    print("\n")

def demo_ascii_art():
    """Demo ASCII art animation"""
    print(f"{Colors.BOLD}ASCII Art Animation{Colors.RESET}\n")
    
    # Simple spinning line frames
    frames = [
        '-\n',
        '\\\n',
        '|\n',
        '/\n'
    ]
    
    ascii_anim = AsciiArtAnimator(frames, speed=0.2)
    ascii_anim.start()
    time.sleep(3)
    ascii_anim.stop()
    print("\n")

if __name__ == "__main__":
    # TerminalUtils.clear_screen()
    # demo_package_managers()
    # time.sleep(1)
    # demo_text_effects()
    # time.sleep(1)
    # demo_enhanced_typewriter()
    # time.sleep(1)
    # demo_system_operations()
    # time.sleep(1)
    demo_ascii_art()
