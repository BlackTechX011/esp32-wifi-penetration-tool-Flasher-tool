import os
import subprocess
import serial.tools.list_ports
import time


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def list_serial_ports():
    # List available serial ports
    ports = [port.device for port in serial.tools.list_ports.comports()]
    return ports

def flash_firmware(port):
    # Path to esptool.py in the esptool-master folder
    esptool_path = os.path.join("esptool-master", "esptool.py")
    
    # Flash firmware using esptool.py
    try:
        command = f'python "{esptool_path}" -p {port} -b 115200 --after hard_reset write_flash --flash_mode dio --flash_freq 40m --flash_size detect 0x8000 build/partition_table/partition-table.bin 0x1000 build/bootloader/bootloader.bin 0x10000 build/esp32-wifi-penetration-tool.bin'
        subprocess.run(command, shell=True, check=True)
        print("Firmware flashed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error flashing firmware: {e}")


def main():
    clear_screen()
    print("Flasher tool for ESP32")
    print("")
    # List available serial ports
    ports = list_serial_ports()
    if not ports:
        print("No serial ports found.")
        print("> Connect your ESP32 device")
        time.sleep(4)
        clear_screen()
        print("Exiting...")
        return
    
    # Display available ports
    print("Available serial ports:")
    print("")
    for i, port in enumerate(ports):
        print(f"{i+1}. {port}")
    
    # Prompt user to select a port
    selected_port = None
    while selected_port is None:
        try:
            print("")
            port_input = input("Select the port to which ESP32 is connected (1, 2, ..., COMx): ")
            print("")
            if port_input.isdigit():
                port_index = int(port_input)
                if 1 <= port_index <= len(ports):
                    selected_port = ports[port_index - 1]
                else:
                    print("Invalid port index. Please select a valid port.")
            elif port_input.upper() in ports:
                selected_port = port_input.upper()
            else:
                print("Invalid port selection. Please enter a valid port index or port name.")
        except ValueError:
            print("Invalid input. Please enter a valid port index or port name.")
    
    # Flash firmware
    flash_firmware(selected_port)

if __name__ == "__main__":
    main()
