import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import threading
import time
from datetime import datetime

class SatiricalNewsGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_data()
        self.setup_variables()
        self.create_widgets()
        self.headline_count = 0
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("🎭 Satirical News Headlines Generator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Modern color scheme
        self.colors = {
            'bg': "#f0e2e2",
            'secondary_bg': "#e8ecef", 
            'accent': "#9A1111",
            'accent_hover': "#033C17",
            'success': '#27ae60',
            'text': "#A80B0B",
            'text_secondary': '#b0b0b0',
            'warning': '#f39c12'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Configure ttk style for modern look
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
    def setup_data(self):
        """Initialize all data lists"""
        self.celebrities = [
            "Shahrukh Khan", "Virat Kohli", "Nirmala Sitharaman", "Amitabh Bachchan",
            "Priyanka Chopra", "MS Dhoni", "Akshay Kumar", "Deepika Padukone",
            "Salman Khan", "Aamir Khan", "Kareena Kapoor", "Ranveer Singh"
        ]
        
        self.fictional_characters = [
            "A Mumbai Cat", "Delhi Metro Announcer", "Chaiwala from Corner Shop",
            "Autorickshaw Driver", "Bollywood Villain", "Street Food Vendor",
            "Local Barber", "Newspaper Delivery Boy", "Traffic Police Uncle"
        ]
        
        self.abstract_concepts = [
            "Astrobiology", "Ancient Civilizations", "Quantum Computing", "Mythology & Folklore",
            "Artificial Intelligence Ethics", "Marine Biology", "Forensic Psychology", "Space Exploration",
            "Cryptography", "Environmental Sustainability", "Genetic Engineering", "Philosophy of Mind",
            "Nanotechnology", "Virtual Reality", "Cultural Anthropology", "Renewable Energy",
            "Linguistics", "Robotics", "History of Art", "Cybersecurity", "Climate Change"
        ]
        
        self.actions = [
            "launches startup for", "declares love for", "writes poetry about", "creates memes featuring",
            "organizes flash mob at", "establishes diplomatic relations with", "builds replica of",
            "starts online petition against", "composes symphony inspired by", "invents new sport involving",
            "opens theme park dedicated to", "creates NFT collection of", "starts YouTube channel about",
            "launches cryptocurrency based on", "designs fashion line inspired by", "creates documentary about",
            "invents app for", "starts meditation retreat near", "organizes marathon around"
        ]
        
        self.places = [
            "Taj Mahal", "Qutub Minar", "Red Fort", "India Gate", "Gateway of India",
            "Charminar", "Hawa Mahal", "Lotus Temple", "Golden Temple", "Meenakshi Temple",
            "Dal Lake", "Pangong Lake", "Thar Desert", "Sundarbans", "Cyber City Gurgaon",
            "Bandra-Worli Sea Link", "Bangalore IT Corridor", "Mumbai Local Train", "Delhi Metro"
        ]
        
        self.headline_formats = [
            "🚨 SATIRICAL NEWS: {} {} {}!",
            "📰 PARODY ALERT: Local Sources Report {} {} {}",
            "🎭 COMEDY NEWS: In Shocking Turn, {} {} {}",
            "😂 FAKE BULLETIN: {} Reportedly {} {}",
            "🎪 SATIRICAL SCOOP: {} {} {} - Netizens React!"
        ]
        
    def setup_variables(self):
        """Initialize tkinter variables"""
        self.auto_generate_var = tk.BooleanVar(value=False)
        self.auto_interval_var = tk.DoubleVar(value=2.0)
        self.current_headline_var = tk.StringVar()
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        self.create_header()
        self.create_main_content()
        self.create_controls()
        self.create_history_section()
        self.create_footer()
        
    def create_header(self):
        """Create the header section"""
        header_frame = tk.Frame(self.root, bg=self.colors['secondary_bg'], height=100)
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame, 
            text="🎭 Satirical News Headlines Generator",
            font=('Arial', 24, 'bold'),
            bg=self.colors['secondary_bg'],
            fg=self.colors['accent']
        )
        title_label.pack(pady=15)
        
        # Disclaimer
        disclaimer_label = tk.Label(
            header_frame,
            text="⚠️ DISCLAIMER: All headlines are FICTIONAL and for ENTERTAINMENT only!",
            font=('Arial', 10, 'italic'),
            bg=self.colors['secondary_bg'],
            fg=self.colors['warning']
        )
        disclaimer_label.pack()
        
    def create_main_content(self):
        """Create the main headline display area"""
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Current headline display
        headline_frame = tk.Frame(main_frame, bg=self.colors['secondary_bg'], relief='raised', bd=2)
        headline_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(
            headline_frame,
            text="Latest Satirical Headline:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['secondary_bg'],
            fg=self.colors['text']
        ).pack(anchor='w', padx=10, pady=(10, 5))
        
        self.headline_display = tk.Label(
            headline_frame,
            textvariable=self.current_headline_var,
            font=('Arial', 14),
            bg=self.colors['secondary_bg'],
            fg=self.colors['accent'],
            wraplength=800,
            justify='left'
        )
        self.headline_display.pack(padx=10, pady=(0, 10), fill='x')
        
        # Set initial headline
        self.current_headline_var.set("Click 'Generate Headline' to create your first satirical news!")
        
    def create_controls(self):
        """Create control buttons and options"""
        controls_frame = tk.Frame(self.root, bg=self.colors['bg'])
        controls_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        # Buttons frame
        buttons_frame = tk.Frame(controls_frame, bg=self.colors['bg'])
        buttons_frame.pack(fill='x', pady=(0, 10))
        
        # Generate button
        self.generate_btn = tk.Button(
            buttons_frame,
            text="🎲 Generate Headline",
            font=('Arial', 12, 'bold'),
            bg=self.colors['accent'],
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.generate_headline,
            cursor='hand2'
        )
        self.generate_btn.pack(side='left', padx=(0, 10))
        
        # Clear history button
        clear_btn = tk.Button(
            buttons_frame,
            text="🗑️ Clear History",
            font=('Arial', 10),
            bg=self.colors['warning'],
            fg='white',
            relief='flat',
            padx=15,
            pady=10,
            command=self.clear_history,
            cursor='hand2'
        )
        clear_btn.pack(side='left', padx=(0, 10))
        
        # Auto-generate controls
        auto_frame = tk.Frame(buttons_frame, bg=self.colors['bg'])
        auto_frame.pack(side='right')
        
        self.auto_checkbox = tk.Checkbutton(
            auto_frame,
            text="Auto Generate",
            variable=self.auto_generate_var,
            command=self.toggle_auto_generate,
            bg=self.colors['bg'],
            fg=self.colors['text'],
            selectcolor=self.colors['secondary_bg'],
            activebackground=self.colors['bg'],
            font=('Arial', 10)
        )
        self.auto_checkbox.pack(side='left', padx=(0, 10))
        
        tk.Label(
            auto_frame,
            text="Interval:",
            bg=self.colors['bg'],
            fg=self.colors['text'],
            font=('Arial', 10)
        ).pack(side='left')
        
        self.interval_spinbox = tk.Spinbox(
            auto_frame,
            from_=1.0,
            to=10.0,
            increment=0.5,
            textvariable=self.auto_interval_var,
            width=5,
            font=('Arial', 10)
        )
        self.interval_spinbox.pack(side='left', padx=(5, 0))
        
        tk.Label(
            auto_frame,
            text="sec",
            bg=self.colors['bg'],
            fg=self.colors['text'],
            font=('Arial', 10)
        ).pack(side='left', padx=(5, 0))
        
    def create_history_section(self):
        """Create the headlines history section"""
        history_frame = tk.Frame(self.root, bg=self.colors['bg'])
        history_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # History label
        tk.Label(
            history_frame,
            text="📜 Headlines History:",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 5))
        
        # Scrollable text area for history
        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            height=8,
            font=('Arial', 10),
            bg=self.colors['secondary_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            relief='sunken',
            bd=2
        )
        self.history_text.pack(fill='both', expand=True)
        
    def create_footer(self):
        """Create the footer with statistics"""
        footer_frame = tk.Frame(self.root, bg=self.colors['secondary_bg'], height=40)
        footer_frame.pack(fill='x', padx=10, pady=(0, 10))
        footer_frame.pack_propagate(False)
        
        self.stats_label = tk.Label(
            footer_frame,
            text="Headlines Generated: 0 | Session Started: " + datetime.now().strftime("%Y-%m-%d %H:%M"),
            font=('Arial', 10),
            bg=self.colors['secondary_bg'],
            fg=self.colors['text_secondary']
        )
        self.stats_label.pack(side='left', padx=10, pady=10)
        
        # Exit button
        exit_btn = tk.Button(
            footer_frame,
            text="❌ Exit",
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            command=self.exit_application,
            cursor='hand2'
        )
        exit_btn.pack(side='right', padx=10, pady=5)
        
    def get_random_subject(self):
        """Get random subject from different categories"""
        category = random.choice(['celebrity', 'fictional', 'abstract'])
        if category == 'celebrity':
            return random.choice(self.celebrities)
        elif category == 'fictional':
            return random.choice(self.fictional_characters)
        else:
            return random.choice(self.abstract_concepts)
            
    def generate_headline(self):
        """Generate and display a new satirical headline"""
        subject = self.get_random_subject()
        action = random.choice(self.actions)
        place = random.choice(self.places)
        format_template = random.choice(self.headline_formats)
        
        headline = format_template.format(subject, action, place)
        self.current_headline_var.set(headline)
        
        # Add to history
        self.headline_count += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_entry = f"[{timestamp}] {headline}\n"
        
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)
        
        # Update statistics
        self.update_stats()
        
        # Visual feedback
        self.animate_button()
        
    def animate_button(self):
        """Add visual feedback to generate button"""
        original_bg = self.generate_btn['bg']
        self.generate_btn.configure(bg=self.colors['success'])
        self.root.after(200, lambda: self.generate_btn.configure(bg=original_bg))
        
    def toggle_auto_generate(self):
        """Toggle auto-generation mode"""
        if self.auto_generate_var.get():
            self.start_auto_generate()
        else:
            self.stop_auto_generate()
            
    def start_auto_generate(self):
        """Start automatic headline generation"""
        self.generate_btn.configure(state='disabled')
        self.auto_generate_thread()
        
    def auto_generate_thread(self):
        """Thread function for auto generation"""
        def auto_loop():
            while self.auto_generate_var.get():
                self.root.after(0, self.generate_headline)
                time.sleep(self.auto_interval_var.get())
                
        self.auto_thread = threading.Thread(target=auto_loop, daemon=True)
        self.auto_thread.start()
        
    def stop_auto_generate(self):
        """Stop automatic headline generation"""
        self.generate_btn.configure(state='normal')
        
    def clear_history(self):
        """Clear the headlines history"""
        result = messagebox.askyesno("Clear History", "Are you sure you want to clear all headlines history?")
        if result:
            self.history_text.delete(1.0, tk.END)
            
    def update_stats(self):
        """Update footer statistics"""
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        stats_text = f"Headlines Generated: {self.headline_count} | Session Started: {start_time}"
        self.stats_label.configure(text=stats_text)
        
    def exit_application(self):
        """Exit the application with confirmation"""
        if self.headline_count > 0:
            result = messagebox.askyesnocancel(
                "Exit Application", 
                f"You've generated {self.headline_count} headlines!\n\nAre you sure you want to exit?"
            )
            if result:
                self.root.quit()
        else:
            self.root.quit()

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = SatiricalNewsGUI(root)
    
    # Center the window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()