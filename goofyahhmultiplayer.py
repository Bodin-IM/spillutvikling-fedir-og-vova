import pygame
import socket
import pickle
import sys


pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shooter Game - Client")


player_pos = [width // 2, height // 2]
player_color = (0, 255, 0)
bullets = []


server_ip = input("Enter the host's IP address: ")
server_port = 139

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try:
    client_socket.connect((server_ip, server_port))
    print("Connected to the lobby!")
except Exception as e:
    print(f"Connection failed: {e}")
    pygame.quit()
    sys.exit()  # Exit if the connection fails


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Player movement
    if keys[pygame.K_a]:  # Move left
        player_pos[0] -= 5
    if keys[pygame.K_d]:  # Move right
        player_pos[0] += 5
    if keys[pygame.K_w]:  # Move up
        player_pos[1] -= 5
    if keys[pygame.K_s]:  # Move down
        player_pos[1] += 5

    # Receive bullet positions from the server
    try:
        data = client_socket.recv(4096)
        if data:
            bullets = pickle.loads(data)
    except Exception as e:
        print(f"Error receiving data: {e}")
        running = False  # Stop the loop if there's an error

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw player
    pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], 50, 50))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 0, 0), (bullet[0], bullet[1], 5, 10))

    pygame.display.flip()


client_socket.close()  # Close the socket when done
pygame.quit()