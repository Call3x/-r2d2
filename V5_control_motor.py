import pygame
import RPi.GPIO as GPIO
import time

# Configuration des broches GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # IN1 (Motor 1 Forward)
GPIO.setup(22, GPIO.OUT)  # IN3 (Motor 2 Forward)

# Initialiser la bibliothèque pygame pour lire la manette
pygame.init()
pygame.joystick.init()

# Ouvrir la manette
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Créer des objets PWM pour les moteurs
pwm_motor1_forward = GPIO.PWM(17, 100)  # Fréquence de 100 Hz
pwm_motor2_forward = GPIO.PWM(22, 100)  # Fréquence de 100 Hz

# Démarrer les PWM avec une valeur de 0
pwm_motor1_forward.start(0)
pwm_motor2_forward.start(0)

# Variable pour contrôler l'état des moteurs
motors_enabled = True  # Par défaut, les moteurs sont activés

# Fonction pour contrôler les moteurs
def control_motor(x_axis, y_axis):
    if not motors_enabled:
        # Si les moteurs ne sont pas activés, ne rien faire
        pwm_motor1_forward.ChangeDutyCycle(0)
        pwm_motor2_forward.ChangeDutyCycle(0)
        return

    # Y-axis pour avancer
    if y_axis < -0.1:  # Joystick poussé vers l'avant
        pwm_motor1_forward.ChangeDutyCycle(int(abs(y_axis) * 100))  # Vitesse proportionnelle
        pwm_motor2_forward.ChangeDutyCycle(int(abs(y_axis) * 100))  # Vitesse proportionnelle
    else:  # Stopper les moteurs si le joystick est au centre ou en arrière
        pwm_motor1_forward.ChangeDutyCycle(0)
        pwm_motor2_forward.ChangeDutyCycle(0)

    # Contrôle de direction (gauche/droite) avec le joystick
    if x_axis > -0.1:  # Joystick déplacé à gauche
        pwm_motor1_forward.ChangeDutyCycle(int(abs(x_axis) * 100))  # Vitesse proportionnelle
        pwm_motor2_forward.ChangeDutyCycle(0)
    elif x_axis < 0.1:  # Joystick déplacé à droite
        pwm_motor1_forward.ChangeDutyCycle(0)
        pwm_motor2_forward.ChangeDutyCycle(int(abs(x_axis) * 100))  # Vitesse proportionnelle

def toggle_motors():
    global motors_enabled
    motors_enabled = not motors_enabled  # Inverser l'état des moteurs

try:
    while True:
        pygame.event.pump()  # Nécessaire pour lire les événements pygame
        
        # Lire les valeurs des axes du joystick
        x_axis = joystick.get_axis(0)  # Axe horizontal (gauche/droite)
        y_axis = joystick.get_axis(1)  # Axe vertical (haut/bas)

        # Vérifier si le bouton start (généralement le bouton 7 sur un contrôleur Xbox) est pressé
        if joystick.get_button(7):  # Remplacez 7 par le bon index de bouton si nécessaire
            toggle_motors()
            time.sleep(0.5)  # Anti-rebond pour éviter de basculer trop rapidement

        # Contrôler les moteurs en fonction des valeurs des axes
        control_motor(x_axis, y_axis)

        # Attendre un court instant pour ne pas surcharger le processeur
        time.sleep(0.1)

except KeyboardInterrupt:
    # Nettoyage des broches GPIO
    pwm_motor1_forward.stop()
    pwm_motor2_forward.stop()
    GPIO.cleanup()
    pygame.quit()