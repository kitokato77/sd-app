import os
import time
from datetime import datetime, timedelta

#deklarasi awal
def convert_to_seconds(hours=0, minutes=0, seconds=0):
    """
    Convert hours, minutes, and seconds to total seconds
    Supports decimal values for all units
    """
    return (float(hours) * 3600) + (float(minutes) * 60) + float(seconds)

#menu1
def get_power_option():
    """
    Get the desired power operation from user
    """
    print("╔════════════════════════════════════════╗")
    print("║           POWER OPTIONS                ║")
    print("╠════════════════════════════════════════╣")
    print("║ 1. Shutdown                            ║")
    print("║ 2. Restart                             ║")
    print("║ 3. Sleep                               ║")
    print("╚════════════════════════════════════════╝")
    
    try:
        choice = int(input("\nPilih opsi (1-3): "))
        if choice not in [1, 2, 3]:
            raise ValueError("Pilihan tidak valid!")
        return choice
    except ValueError as e:
        print(f"Error: {str(e)}")
        return None

#menu2
def get_time_input():
    """
    Get time input from user with flexible format options
    """
    print("╔════════════════════════════════════════╗")
    print("║           TIMER OPTIONS                ║")
    print("╠════════════════════════════════════════╣")
    print("║ 1. Masukkan waktu dalam jam            ║")
    print("║ 2. Masukkan waktu dalam menit          ║")
    print("║ 3. Masukkan waktu dalam detik          ║")
    print("║ 4. Masukkan kombinasi (jam:menit:detik)║")
    print("╚════════════════════════════════════════╝")
    
    try:
        choice = int(input("\nPilih opsi (1-4): "))
        
        if choice == 1:
            hours = float(input("Masukkan jam (bisa desimal, misal 3.5): "))
            return convert_to_seconds(hours=hours)
        elif choice == 2:
            minutes = float(input("Masukkan menit (bisa desimal, misal 4.5): "))
            return convert_to_seconds(minutes=minutes)
        elif choice == 3:
            seconds = float(input("Masukkan detik (bisa desimal, misal 90.5): "))
            return convert_to_seconds(seconds=seconds)
        elif choice == 4:
            print("\nFormat: jam:menit:detik")
            print("Contoh: 1:30:45 atau 0:45:30 atau 2:15:0")
            time_input = input("\nMasukkan waktu: ").split(':')
            if len(time_input) != 3:
                raise ValueError("Format waktu salah!")
            return convert_to_seconds(
                float(time_input[0]), 
                float(time_input[1]), 
                float(time_input[2])
            )
        else:
            raise ValueError("Pilihan tidak valid!")
    except ValueError as e:
        print(f"Error: {str(e)}")
        return None

#tombolmenu1
def execute_power_command(power_option):
    """
    Execute the selected power command based on OS
    """
    if os.name == 'nt':  # Windows
        if power_option == 1:  # Shutdown
            os.system('shutdown /s /t 1')
        elif power_option == 2:  # Restart
            os.system('shutdown /r /t 1')
        elif power_option == 3:  # Sleep
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
    else:  # Unix-based
        if power_option == 1:  # Shutdown
            os.system('shutdown -h now')
        elif power_option == 2:  # Restart
            os.system('shutdown -r now')
        elif power_option == 3:  # Sleep
            os.system('systemctl suspend')

def cancel_power_command(power_option):
    """
    Cancel the pending power command
    """
    if os.name == 'nt':  # Windows
        if power_option in [1, 2]:  # Shutdown or Restart
            os.system('shutdown /a')
    else:  # Unix-based
        if power_option in [1, 2]:  # Shutdown or Restart
            os.system('shutdown -c')

def get_power_action_name(power_option):
    """
    Get the name of the power action for display
    """
    if power_option == 1:
        return "SHUTDOWN"
    elif power_option == 2:
        return "RESTART"
    else:
        return "SLEEP"

def power_timer(total_seconds, power_option):
    """
    Timer function with countdown for various power options
    Parameters:
        total_seconds (float): Number of seconds until power action
        power_option (int): Selected power option (1=shutdown, 2=restart, 3=sleep)
    """
    action_name = get_power_action_name(power_option)
    box_width = 40  # Tetapkan lebar box yang konsisten
    
    try:
        while total_seconds > 0:
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Calculate remaining time
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            seconds = int(total_seconds % 60)
            
            # Calculate estimated action time
            action_time = datetime.now().replace(microsecond=0) + \
                         timedelta(seconds=total_seconds)
            
            # Format strings with fixed width
            title = f"{action_name} COUNTDOWN"
            time_remaining = f"Time remaining: {hours:02d}:{minutes:02d}:{seconds:02d}"
            shutdown_time = f"{action_name} at: {action_time.strftime('%H:%M:%S')}"
            
            # Center align text
            title = title.center(box_width - 4)  # -4 untuk kompensasi "║ " di kedua sisi
            time_remaining = time_remaining.ljust(box_width - 4)
            shutdown_time = shutdown_time.ljust(box_width - 4)
            
            # Display countdown dengan lebar tetap
            print("╔" + "═" * (box_width - 2) + "╗")
            print(f"║ {title} ║")
            print("╠" + "═" * (box_width - 2) + "╣")
            print(f"║ {time_remaining} ║")
            print(f"║ {shutdown_time} ║")
            print("╚" + "═" * (box_width - 2) + "╝")
            print("\nTekan Ctrl+C untuk membatalkan")
            
            time.sleep(1)
            total_seconds -= 1
            
        print(f"\nMemulai {action_name.lower()}...")
        execute_power_command(power_option)
            
    except KeyboardInterrupt:
        print(f"\n{action_name} timer dibatalkan!")
        cancel_power_command(power_option)

# Main program
if __name__ == "__main__":
    while True:
        power_option = get_power_option()
        if power_option is not None:
            seconds = get_time_input()
            if seconds is not None and seconds > 0:
                power_timer(seconds, power_option)
                break
        
        retry = input("\nIngin mencoba lagi? (y/n): ")
        if retry.lower() != 'y':
            break