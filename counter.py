import os
import time
import re
import sys
from collections import Counter
from pathlib import Path


try:
    from rich.console import Console
except ImportError:
    print("Error: 'rich' library not found.")
    print("Please install it using: pip install rich")
    sys.exit(1)



try:
    import tkinter as tk
    from tkinter import filedialog
    tkinter_available = True
except ImportError:
    tkinter_available = False
    
    tkinter_needed = False 

# --- Globals ---
console = Console()
MIN_COUNT = 1000  
REPORT1_TOP_N = 25 
REPORT2_TOP_N = 50 
MIN_WORD_LENGTH = 5 

# --- Helper Functions ---

def clear_console():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_rich_text(text):
    """Formats text with [[number]] tags into a Rich markup string."""
    segments = re.split(r'(\[\[\d+\]\])', text)
    current_style = "white"  
    output_string = ""
    for segment in segments:
        if re.match(r'\[\[\d+\]\]', segment):
            color_code = segment.strip('[]')
            
            try:
               color_num = int(color_code)
               if 0 <= color_num <= 255:
                   current_style = f"color({color_num})"
               else: 
                   current_style = "white"
            except ValueError:
                 current_style = "white" 
        elif segment:
             
             escaped_segment = segment.replace('[', r'\[').replace(']', r'\]')
             output_string += f"[{current_style}]{escaped_segment}[/]"
    return output_string

def rich_print(text, end="\n"):
    """Prints text using Rich, processing [[number]] tags."""
    formatted_text = format_rich_text(text)
    console.print(formatted_text, end=end)

# --- Art Definition ---
MR_PROGRAMM_ART = [
    "[[47]]▓▓    ▓▓  ▓▓▓▓        ▓▓▓▓    ▓▓▓▓      ▓▓▓    ▓▓▓▓   ▓▓▓▓      ▓▓▓    ▓▓    ▓▓  ▓▓    ▓▓",
    "[[47]]▓▓▓  ▓▓▓  ▓▓  ▓▓      ▓▓  ▓▓  ▓▓  ▓    ▓   ▓  ▓▓      ▓▓  ▓    ▓▓ ▓▓   ▓▓▓  ▓▓▓  ▓▓▓  ▓▓▓",
    "[[47]]▓  ▓▓  ▓  ▓▓▓▓    ▓▓  ▓▓▓▓    ▓▓▓▓    ▓     ▓ ▓  ▓▓▓  ▓▓▓▓    ▓▓▓▓▓▓▓  ▓  ▓▓  ▓  ▓  ▓▓  ▓",
    "[[47]]▓      ▓  ▓   ▓       ▓       ▓   ▓    ▓   ▓  ▓▓   ▓  ▓   ▓   ▓     ▓  ▓      ▓  ▓      ▓", 
    "[[47]]▓▓    ▓▓  ▓    ▓      ▓       ▓    ▓    ▓▓▓    ▓▓▓▓   ▓    ▓  ▓     ▓  ▓▓    ▓▓  ▓▓    ▓▓" 
]

def strip_tags_for_len(text):
    return re.sub(r'\[\[\d+\]\]', '', text)


try:
    ART_MAX_WIDTH = max(len(strip_tags_for_len(line)) for line in MR_PROGRAMM_ART)
except ValueError: 
    ART_MAX_WIDTH = 0

def generate_ascii_art():
    """Prints the predefined MR_PROGRAMM_ART, centered."""
    terminal_width = console.width
    
    padding = " " * max(0, (terminal_width - ART_MAX_WIDTH) // 2)

    for line in MR_PROGRAMM_ART:
        
        rich_print(padding + line)

def get_folder_path():
    """Gets the folder path from the user using one of two methods."""
    global tkinter_needed 
    while True:
        clear_console()
        display_title()

        rich_print("\n\n")
        rich_print("[[180]]SELECT [[15]]an [[9]]OPTION [[15]]of how to choose the [[49]]FOLDER [[15]]you would like to  [[130]]ANALYZE[[15]].")
        rich_print("[[11]]-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        rich_print("[[67]]([[85]]1[[67]]) [[14]]Manually select your [[156]]FOLDER [[14]] from a [[156]]WINDOW[[15]].")
        rich_print("[[9]]OR")
        rich_print("[[67]]([[85]]2[[67]]) [[133]]PASTE [[14]]your [[156]]FOLDER [[14]]location in console[[15]].")
        rich_print("\n\n")

        time.sleep(1)
        
        prompt_text = "[[15]]Please [[180]]SELECT [[85]]1[[15]], [[14]]or [[85]]2[[15]]:[[85]]    "
        choice = console.input(format_rich_text(prompt_text))

        if choice == '1':
            tkinter_needed = True 
            if not tkinter_available:
                
                console.print("\n\nError: Tkinter library needed for folder selection window but not found.")
                console.print("Please ensure Tkinter is installed for your Python environment,")
                console.print("or choose Option 2 to paste the path.")
                time.sleep(4)
                continue 

            rich_print("\n\n") 
            rich_print("[[82]]Please select the [[200]]FOLDER [[82]]you want to [[198]]ANALYZE[[15]].")
            time.sleep(2.75)
            
            root = tk.Tk()
            root.withdraw()
            
            root.attributes('-topmost', True)
            folder_path = filedialog.askdirectory(title="Select Folder to Analyze")
            root.destroy() 

            if folder_path: 
                return Path(folder_path)
            else: 
                rich_print("[[1]]Operation cancelled by user.[[15]]")
                time.sleep(2)
                continue 

        elif choice == '2':
            rich_print("\n")
            rich_print("[[82]]Please [[133]]PASTE [[82]]your [[200]]FOLDER'S [[82]]location in which you would like to [[198]]ANALYZE[[15]].")
            time.sleep(1.2)
             
            prompt_text = "[[121]]Location[[15]]:    "
            path_str = console.input(format_rich_text(prompt_text))
            folder_path = Path(path_str.strip().strip('"\'')) 

            if folder_path.is_dir():
                return folder_path
            else:
                
                rich_print(f"\n[[1]]Error: [[15]]The path '[[14]]{folder_path}[[15]]' is not a valid directory.")
                time.sleep(3)
                continue 
        else:
            rich_print("\n[[1]]Invalid choice. Please enter 1 or 2.[[15]]")
            time.sleep(2)
            

def display_title():
    """Displays the program title and header."""
    border = "                 [[215]].o0o..o0o..o0o..o0o..o0o..o0o..o0o..o0o..o0o..o0o..o0o..o0o..o0o..o0o..o0o..o0o."
    rich_print(border)
    rich_print("")
    generate_ascii_art()
    rich_print("")
    rich_print("                                 [[45]]COMMON PASSWORDS [[87]]USED [[217]]COUNTER    [[15]]version [[1]]( [[9]]1.0 [[1]]) ")
    rich_print("                                           [[7]]mr-programm1@proton.me   [[142]]https://github.com/Mr-Programm   ")                                                          
    rich_print(border)

def analyze_files(folder_path):
    """Reads files, extracts passwords, counts them and words (>=MIN_WORD_LENGTH chars) within them."""
    password_counter = Counter()
    word_counter = Counter()
    all_passwords = [] 

    rich_print(f"\n[[15]]Analyzing files in folder: [[117]]{folder_path}[[15]]...")
    found_files = False
    processed_lines = 0

    try:
        txt_files = list(folder_path.glob('*.txt'))
        if not txt_files:
             rich_print(f"\n[[3]]Warning: [[15]]No '[[14]].txt[[15]]' files found in the selected folder.")
             return None, None, None 

        found_files = True
        total_files = len(txt_files)
        rich_print(f"[[15]]Found [[6]]{total_files}[[15]] '.txt' file(s). Starting analysis...")

        for i, file_path in enumerate(txt_files):
            
            print(f"  Processing file {i+1}/{total_files}: '{file_path.name}'...", end="\r")
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        processed_lines += 1
                        
                        parts = line.strip().rsplit(':', 1)
                        if len(parts) == 2:
                            password = parts[1].strip()
                            if password: 
                                password_counter[password] += 1
                                all_passwords.append(password) 
            except Exception as e:
                 
                rich_print(f"\n[[1]]Error reading file [[14]]{file_path.name}[[15]]: {e}")
                time.sleep(1) 

        print(" " * console.width, end="\r") 
        rich_print(f"[[15]]Analysis complete. Processed [[6]]{processed_lines}[[15]] lines across [[6]]{total_files}[[15]] files.")

        if not password_counter:
             rich_print(f"\n[[3]]Warning: [[15]]No passwords found (lines with ':password') in the processed files.")
             return None, None, None 

        # --- Word Analysis (with length filter) ---
        rich_print(f"[[15]]Analyzing words (min length {MIN_WORD_LENGTH}) within passwords...") 
        for password in all_passwords:
            password_lower = password.lower()
            
            words_in_pass = re.findall(r'[a-z]+', password_lower)
            
            unique_words_in_pass = set(words_in_pass)

            
            valid_words = {word for word in unique_words_in_pass if len(word) >= MIN_WORD_LENGTH}

            
            if valid_words: 
                word_counter.update(valid_words)

        rich_print("[[15]]Word analysis complete.") 

        
        filtered_passwords = {pw: count for pw, count in password_counter.items() if count >= MIN_COUNT}
        
        filtered_words = {word: count for word, count in word_counter.items() if count >= MIN_COUNT}

        
        sorted_passwords = sorted(filtered_passwords.items(), key=lambda item: item[1], reverse=True)
        sorted_words = sorted(filtered_words.items(), key=lambda item: item[1], reverse=True)

        return sorted_passwords, sorted_words, all_passwords

    except Exception as e:
         
        rich_print(f"\n[[1]]An unexpected error occurred during analysis: {e}")
        return None, None, None


def display_report(report_data, title, header, top_n, type_label):
    """Displays a formatted report in the console using rich_print."""
    clear_console()
    rich_print(title)
    rich_print(header)
    
    line_format_template = "[[15]]{index}. [[14]]{item:<{width}} [[10]]COUNT[[15]]: [[6]]{count}"

    if not report_data:
        rich_print(f"\n[[3]]No {type_label} found with a minimum count of {MIN_COUNT}.")
        return False 

    
    item_width = 30

    count_displayed = 0
    for i, (item, count) in enumerate(report_data):
        if i < top_n:
            
            line_to_print = line_format_template.format(index=i + 1, item=item, width=item_width, count=count)
            rich_print(line_to_print)
            count_displayed += 1
        else:
            break 

    if len(report_data) > top_n:
         
         rich_print(f"\n[[1]]MORE THAN [[9]]{top_n} [[1]]COMMON [[9]]{type_label.upper()} [[1]]FOUND[[15]]!!!")

    if count_displayed == 0:
         
         min_req_text = f"minimum count of {MIN_COUNT}"
         if type_label == "words":
             min_req_text += f" and minimum length of {MIN_WORD_LENGTH}"
         rich_print(f"\n[[3]]No {type_label} found meeting requirements ({min_req_text}).[[15]]")
         return False 

    return True 

def save_report(report_data, filename, folder_path, title, header, type_label):
    """Saves the full report data to a text file, removing color tags and ensuring alignment."""
    if not report_data:
        return # Don't save empty reports

    save_path = folder_path / filename
    # The format string for the lines in the file
    line_format = "{index}. {item:<{width}} COUNT: {count}"
    # Initial item width - will be adjusted below
    item_width = 30

    # Function to remove color tags (only needed for title/header here)
    def strip_color_tags(text):
        return re.sub(r'\[\[\d+\]\]', '', text)

    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            # Remove color tags before writing title and header
            clean_title = strip_color_tags(title).strip()
            clean_header = strip_color_tags(header).strip()

            f.write(f"{clean_title}\n")
            f.write(f"{clean_header}\n")
            f.write(f"{'-'* (len(clean_header) if clean_header else 40)}\n") # Separator

            if not report_data:
                 min_req_text = f"minimum count of {MIN_COUNT}"
                 if type_label == "words":
                    min_req_text += f" and minimum length of {MIN_WORD_LENGTH}"
                 f.write(f"\nNo {type_label} found meeting requirements ({min_req_text}).\n")
            else:
                 # --- Start of Width Calculation Change ---
                 # Determine width for alignment based on actual data
                 try:
                    # Find max length of the actual items (password/word strings)
                    # Ensure items are strings for len()
                    max_item_len = max(len(str(item[0])) for item in report_data) if report_data else 0

                    # Set a generous fixed minimum width OR the max length + padding, whichever is larger.
                    # This ensures space for the item AND the count part on the same line.
                    # Let's use a minimum of 40 characters for the item field.
                    item_width = max(40, max_item_len + 5) # Increased minimum width and padding

                 except Exception as e: # Handle potential errors during calculation
                    # Use console.print for plain error message to console if needed
                    # console.print(f"Debug: Error calculating max_item_len: {e}")
                    item_width = 50 # Fallback to a reasonably large width
                 # --- End of Width Calculation Change ---

                 for i, (item, count) in enumerate(report_data):
                     # Optional: Sanitize item just in case it contains newlines (unlikely)
                     safe_item = str(item).replace('\n', '').replace('\r', '')

                     # Write the line using the calculated width
                     # The f-string now correctly allocates enough space via item_width
                     f.write(line_format.format(index=i + 1, item=safe_item, width=item_width, count=count) + "\n")

    except Exception as e:
        # Use rich_print for console error message which might have tags
        rich_print(f"\n[[1]]Error saving report to [[14]]{save_path}[[15]]: {e}")
# --- Main Program Flow ---

def main():
    while True: 
        clear_console()
        display_title()
        time.sleep(1.5)

        folder_path = get_folder_path()
        if not folder_path:
            continue 

        sorted_passwords, sorted_words, _ = analyze_files(folder_path)

        if sorted_passwords is None and sorted_words is None:
            
            rich_print("\n[[15]]Returning to the main menu...") 
            time.sleep(4)
            continue 

        # --- Display Report 1 ---
        report1_title = "[[11]]REPORT [[15]]# [[51]]1"
        report1_header = "[[15]]TOP [[11]]PASSWORDS [[9]]FOUND\n[[11]]-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-"
        report1_shown = display_report(sorted_passwords, report1_title, report1_header, REPORT1_TOP_N, "passwords")

        if report1_shown: 
            time.sleep(2)
            
            prompt_text = "\n[[7]]Please press [[10]]ENTER [[7]]to continue to the next [[11]]REPORT[[15]]..."
            console.input(format_rich_text(prompt_text))
        else:
             time.sleep(3) 


        # --- Display Report 2 ---
        report2_title = "[[11]]REPORT [[15]]# [[81]]2"
        report2_header = f"[[15]]TOP [[1]]COMMON [[141]]WORDS [[9]](LEN>={MIN_WORD_LENGTH}) [[9]]FOUND [[15]]IN [[11]]PASSWORDS\n[[11]]-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=-=-"
        report2_shown = display_report(sorted_words, report2_title, report2_header, REPORT2_TOP_N, "words")

        if report2_shown: 
            time.sleep(2)
            
            prompt_text = "\n[[7]]Please press [[10]]ENTER [[7]]to continue to the for the option to [[3]]SAVE [[7]]the [[11]]REPORTS[[15]]..."
            console.input(format_rich_text(prompt_text))
        else:
             time.sleep(3) 

        clear_console()
        time.sleep(1)
        rich_print("\n\n\n") 

        prompt_text = (
            "[[7]]Do you want to [[6]]SAVE [[7]]the [[215]]REPORTS [[7]]to [[163]]TEXT [[7]]"
            " documents in that same [[200]]FOLDER[[15]]? \n"
            "[[161]]Yes[[9]](Y)[[15]], [[7]]or [[197]]No[[9]](N) [[15]]: "
        )
        save_choice = console.input(format_rich_text(prompt_text)).strip().lower()

        if save_choice in ['yes', 'y']:
            rich_print("\n[[15]]Saving reports...") 
            save_report(sorted_passwords, 'COMMON_PASSWORDS.txt', folder_path,
                        report1_title, report1_header, "passwords")
            save_report(sorted_words, 'COMMON_WORDS.txt', folder_path,
                        report2_title, report2_header, "words")
            rich_print("\n\n") 
            rich_print(f"[[3]]DOCUMENTS [[7]]saved as [[14]]COMMON_PASSWORDS.txt [[7]]and [[14]]COMMON_WORDS.txt [[7]]in [[200]]{folder_path}[[15]].") 
            time.sleep(4)
        else:
            rich_print("\n[[7]]Reports not saved.[[15]]") 
            time.sleep(2)

        rich_print("\n[[15]]Returning to the main menu...") 
        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
         
        print("\n\nExiting program. Goodbye!")
    except Exception as e:
        
        console.print_exception(show_locals=False)
         
        print(f"\n\nAn unexpected critical error occurred: {e}")
        print("Exiting.")