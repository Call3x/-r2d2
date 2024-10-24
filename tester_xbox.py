import pygame

pygame.init()
pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
print(f"Number of joysticks: {joystick_count}")

if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick name: {joystick.get_name()}")
    print(f"Number of axes: {joystick.get_numaxes()}")
else:
    print("No joystick detected")
