import socket
import keyboard
import cv2
import threading


def watch_video_stream(command_socket, command_addr):
    command_socket.sendto(b"streamon", command_addr) 
    print("\n   video streaming started!")
    cap = cv2.VideoCapture('udp://192.168.10.1:11111')
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Tello Video Stream', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # 'Esc' key
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()


def configure_wifi(command_socket, command_addr):

    ssid = input("\n   Enter new wifi SSID: ")
    print("   Done!")


def main():
    print("   Connect to Tello wifi and press <<Shift>>")
    while not keyboard.is_pressed("Shift"):
        pass
    print("   Starting")
    command_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    command_addr = ('192.168.10.1', 8889)
    command_socket.bind(('', 8889))
    command_socket.sendto(b"command", command_addr)
    command_socket.recvfrom(1024)
    print("   Control has taken successfully!")
    video_thread = threading.Thread(target=watch_video_stream, args=(command_socket, command_addr))
    video_thread.daemon = True
    keyboard.on_press_key("1", lambda _: command_socket.sendto(b"emergency", command_addr))
    keyboard.on_press_key("2", lambda _: video_thread.start())
    keyboard.on_press_key("3", lambda _: command_socket.sendto(b"land", command_addr))
    keyboard.on_press_key("4", lambda _: configure_wifi(command_socket, command_addr))

    print("""
   press key for each function:
      1) Emergency - stop motors immediately
       2) Watch Video Stream
        3) Land
       4) Configure Wifi Password- lock the drone
      5) Exit
        """)
    while not keyboard.is_pressed("5"):
        pass


if __name__ == "__main__":
    main()
