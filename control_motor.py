import pygame
import RPi.GPIO as GPIO
import time

# Configuration des broches GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # IN1
GPIO.setup(27, GPIO.OUT)  # IN2
GPIO.setup(22, GPIO.OUT)  # IN3
GPIO.setup(23, GPIO.OUT)  # IN4

# Initialiser la bibliothèque pygame pour lire la manette
pygame.init()
pygame.joystick.init()

# Ouvrir la manette
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Fonction pour contrôler les moteurs
def control_motor(x_axis, y_axis):
    # X-axis et Y-axis peuvent être utilisés pour le contrôle de direction et de vitesse
    if y_axis < -0.1:  # Joystick poussé vers l'avant
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(23, GPIO.LOW)
    elif y_axis > 0.1:  # Joystick poussé vers l'arrière
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.HIGH)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(23, GPIO.HIGH)
    else:  # Stopper les moteurs
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(23, GPIO.LOW)

try:
    while True:
        pygame.event.pump()  # Nécessaire pour lire les événements pygame
        # Lire les valeurs des axes du joystick
        x_axis = joystick.get_axis(0)  # Axe horizontal (gauche/droite)
        y_axis = joystick.get_axis(1)  # Axe vertical (haut/bas)

        # Contrôler les moteurs en fonction des valeurs des axes
        control_motor(x_axis, y_axis)

        # Attendre un court instant pour ne pas surcharger le processeur
        time.sleep(0.1)

except KeyboardInterrupt:
    # Nettoyage des broches GPIO
    GPIO.cleanup()
    pygame.quit()