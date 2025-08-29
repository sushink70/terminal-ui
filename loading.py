#!/usr/bin/env python3
"""
Terminal Loading Animations Collection
A comprehensive library of terminal animations for loading states, progress bars, and transitions.
Features customizable colors, speeds, and styles.
"""

import time
import sys
import threading
import random
import itertools
from typing import Optional, List, Callable, Any
import os

class Colors:
    """ANSI color codes for terminal output"""
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

class TerminalAnimator:
    """Base class for all terminal animations"""
    
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
        print(f"\r{' ' * 80}\r", end='', flush=True)

class SpinnerAnimation(TerminalAnimator):
    """Various spinning animations"""
    
    SPINNERS = {
        'classic': ['|', '/', '-', '\\'],
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'braille': ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷'],
        'blocks': ['▉', '▊', '▋', '▌', '▍', '▎', '▏', '▎', '▍', '▌', '▋', '▊', '▉'],
        'arrows': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'bounce': ['⠁', '⠂', '⠄', '⠂'],
        'pulse': ['●', '◐', '◑', '◒', '◓', '◔', '◕', '◖', '◗'],
        'wave': ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█', '▇', '▆', '▅', '▄', '▃', '▂'],
        'star': ['✶', '✸', '✹', '✺', '✹', '✷'],
        'clock': ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛'],
        'moon': ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘'],
        'earth': ['🌍', '🌎', '🌏'],
        'weather': ['☀️', '🌤️', '⛅', '🌦️', '🌧️', '⛈️', '🌩️', '☀️']
    }
    
    def __init__(self, spinner_type: str = 'classic', message: str = 'Loading', **kwargs):
        super().__init__(**kwargs)
        self.spinner = self.SPINNERS.get(spinner_type, self.SPINNERS['classic'])
        self.message = message
        
    def _animate(self):
        spinner_cycle = itertools.cycle(self.spinner)
        while self.running:
            char = next(spinner_cycle)
            print(f"\r{self.color}{char} {self.message}...{Colors.RESET}", end='', flush=True)
            time.sleep(self.speed)

class ProgressBar(TerminalAnimator):
    """Advanced progress bar with various styles"""
    
    def __init__(self, total: int = 100, width: int = 50, 
                 fill_char: str = '█', empty_char: str = '░',
                 show_percentage: bool = True, show_eta: bool = False,
                 **kwargs):
        super().__init__(**kwargs)
        self.total = total
        self.width = width
        self.fill_char = fill_char
        self.empty_char = empty_char
        self.show_percentage = show_percentage
        self.show_eta = show_eta
        self.current = 0
        self.start_time = None
        
    def update(self, value: int):
        """Update progress bar to specific value"""
        self.current = min(value, self.total)
        self._draw()
        
    def increment(self, amount: int = 1):
        """Increment progress by amount"""
        self.update(self.current + amount)
        
    def _draw(self):
        if self.start_time is None:
            self.start_time = time.time()
            
        percentage = (self.current / self.total) * 100
        filled = int((self.current / self.total) * self.width)
        
        bar = self.fill_char * filled + self.empty_char * (self.width - filled)
        
        output = f"\r{self.color}[{bar}]{Colors.RESET}"
        
        if self.show_percentage:
            output += f" {percentage:.1f}%"
            
        if self.show_eta and self.current > 0:
            elapsed = time.time() - self.start_time
            eta = (elapsed / self.current) * (self.total - self.current)
            output += f" ETA: {eta:.1f}s"
            
        output += f" ({self.current}/{self.total})"
        
        print(output, end='', flush=True)
        
        if self.current >= self.total:
            print()  # New line when complete

class AnimatedText(TerminalAnimator):
    """Animated text effects"""
    
    def __init__(self, text: str, effect: str = 'typewriter', **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.effect = effect
        
    def _animate(self):
        if self.effect == 'typewriter':
            self._typewriter_effect()
        elif self.effect == 'wave':
            self._wave_effect()
        elif self.effect == 'rainbow':
            self._rainbow_effect()
        elif self.effect == 'glitch':
            self._glitch_effect()
            
    def _typewriter_effect(self):
        print(self.color, end='', flush=True)
        for char in self.text:
            if not self.running:
                break
            print(char, end='', flush=True)
            time.sleep(self.speed)
        print(Colors.RESET)
        
    def _wave_effect(self):
        colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
        while self.running:
            for i in range(len(colors)):
                if not self.running:
                    break
                colored_text = ""
                for j, char in enumerate(self.text):
                    color_index = (i + j) % len(colors)
                    colored_text += f"{colors[color_index]}{char}"
                print(f"\r{colored_text}{Colors.RESET}", end='', flush=True)
                time.sleep(self.speed)
                
    def _rainbow_effect(self):
        colors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
        colored_text = ""
        for i, char in enumerate(self.text):
            color = colors[i % len(colors)]
            colored_text += f"{color}{char}"
        print(f"{colored_text}{Colors.RESET}")
        
    def _glitch_effect(self):
        chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        original = self.text
        while self.running:
            glitched = ""
            for char in original:
                if random.random() < 0.1:  # 10% chance to glitch
                    glitched += random.choice(chars)
                else:
                    glitched += char
            print(f"\r{self.color}{glitched}{Colors.RESET}", end='', flush=True)
            time.sleep(self.speed)
            
            # Occasionally show original text
            if random.random() < 0.3:
                print(f"\r{self.color}{original}{Colors.RESET}", end='', flush=True)
                time.sleep(self.speed * 2)

class MatrixRain(TerminalAnimator):
    """Matrix-style digital rain effect"""
    
    def __init__(self, width: int = 80, height: int = 24, 
                 characters: str = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン",
                 **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.height = height
        self.characters = characters
        self.drops = [0] * width
        
    def _animate(self):
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        while self.running:
            # Clear screen
            print("\033[2J\033[H", end='')
            
            for x in range(self.width):
                for y in range(self.height):
                    if y == self.drops[x]:
                        print(f"{Colors.BRIGHT_GREEN}{random.choice(self.characters)}{Colors.RESET}", end='')
                    elif y < self.drops[x] and y > self.drops[x] - 10:
                        print(f"{Colors.GREEN}{random.choice(self.characters)}{Colors.RESET}", end='')
                    elif y < self.drops[x] and y > self.drops[x] - 15:
                        print(f"{Colors.DIM}{random.choice(self.characters)}{Colors.RESET}", end='')
                    else:
                        print(" ", end='')
                print()
                
            # Update drops
            for i in range(len(self.drops)):
                if self.drops[i] > self.height and random.random() > 0.975:
                    self.drops[i] = 0
                self.drops[i] += 1
                
            time.sleep(self.speed)

class LoadingManager:
    """Manager class to handle multiple animations and background tasks"""
    
    def __init__(self):
        self.current_animation = None
        
    def run_with_spinner(self, func: Callable, *args, spinner_type: str = 'dots', 
                        message: str = 'Processing', color: str = Colors.CYAN, **kwargs):
        """Run a function with a spinner animation"""
        spinner = SpinnerAnimation(spinner_type, message, color=color, **kwargs)
        spinner.start()
        
        try:
            result = func(*args)
            return result
        finally:
            spinner.stop()
            
    def run_with_progress(self, func: Callable, total_steps: int, *args, **kwargs):
        """Run a function with a progress bar (requires the function to yield progress)"""
        progress = ProgressBar(total=total_steps, **kwargs)
        
        try:
            for step in func(*args):
                progress.update(step)
                time.sleep(0.01)  # Small delay for smooth animation
            return True
        finally:
            progress.stop()

# Example usage functions
def simulate_work(duration: float = 3):
    """Simulate work being done"""
    time.sleep(duration)
    return "Work completed!"

def simulate_progress_work(steps: int = 50):
    """Simulate work that reports progress"""
    for i in range(steps + 1):
        time.sleep(0.1)
        yield i

# Demo functions
def demo_spinners():
    """Demonstrate all spinner types"""
    print(f"{Colors.BOLD}Spinner Animations Demo{Colors.RESET}\n")
    
    for spinner_type in SpinnerAnimation.SPINNERS.keys():
        print(f"Testing {spinner_type} spinner:")
        spinner = SpinnerAnimation(spinner_type, f"Loading with {spinner_type}", 
                                 color=random.choice([Colors.RED, Colors.GREEN, Colors.BLUE, Colors.YELLOW, Colors.MAGENTA]))
        spinner.start()
        time.sleep(2)
        spinner.stop()
        print(" ✓ Complete\n")

def demo_progress_bars():
    """Demonstrate progress bar variations"""
    print(f"{Colors.BOLD}Progress Bar Demo{Colors.RESET}\n")
    
    # Standard progress bar
    print("Standard progress bar:")
    progress = ProgressBar(total=100, color=Colors.GREEN, show_eta=True)
    for i in range(101):
        progress.update(i)
        time.sleep(0.05)
    print()
    
    # Custom styled progress bar
    print("Custom styled progress bar:")
    progress = ProgressBar(total=50, fill_char='▓', empty_char='░', 
                          color=Colors.BLUE, width=30)
    for i in range(51):
        progress.update(i)
        time.sleep(0.1)
    print()

def demo_text_animations():
    """Demonstrate text animation effects"""
    print(f"{Colors.BOLD}Text Animation Demo{Colors.RESET}\n")
    
    # Typewriter effect
    print("Typewriter effect:")
    typewriter = AnimatedText("Hello, World! This is a typewriter effect.", 
                            effect='typewriter', color=Colors.GREEN, speed=0.05)
    typewriter.start()
    time.sleep(3)
    typewriter.stop()
    
    # Rainbow effect
    print("\nRainbow effect:")
    rainbow = AnimatedText("🌈 Rainbow Text Effect! 🌈", effect='rainbow')
    rainbow.start()
    time.sleep(1)
    rainbow.stop()
    
    # Wave effect
    print("Wave effect (5 seconds):")
    wave = AnimatedText("WAVE EFFECT", effect='wave', speed=0.1)
    wave.start()
    time.sleep(5)
    wave.stop()

def demo_loading_manager():
    """Demonstrate the loading manager"""
    print(f"{Colors.BOLD}Loading Manager Demo{Colors.RESET}\n")
    
    manager = LoadingManager()
    
    # Run work with spinner
    print("Running work with spinner:")
    result = manager.run_with_spinner(simulate_work, 2, 
                                    spinner_type='braille', 
                                    message='Processing data',
                                    color=Colors.YELLOW)
    print(f"Result: {result}\n")
    
    # Run work with progress bar
    print("Running work with progress bar:")
    manager.run_with_progress(simulate_progress_work, 30, 
                            color=Colors.MAGENTA, 
                            show_eta=True)
    print("Progress work completed!\n")

if __name__ == "__main__":
    print(f"{Colors.BOLD}{Colors.CYAN}Terminal Animation Library Demo{Colors.RESET}")
    print("=" * 50)
    
    try:
        # Demo all features
        demo_spinners()
        time.sleep(1)
        
        demo_progress_bars()
        time.sleep(1)
        
        demo_text_animations()
        time.sleep(1)
        
        demo_loading_manager()
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}Demo completed!{Colors.RESET}")
        print("\nTo use these animations in your code:")
        print("1. Import the classes you need")
        print("2. Create an instance with your preferred settings")
        print("3. Call start() to begin animation")
        print("4. Call stop() when your work is done")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Demo interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error during demo: {e}{Colors.RESET}")
