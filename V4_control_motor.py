import pygame
import RPi.GPIO as GPIO
import time

# Configuration des broches GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # IN1 (Motor 1 Forward)
GPIO.setup(27, GPIO.OUT)  # IN2 (Motor 1 Backward)
GPIO.setup(22, GPIO.OUT)  # IN3 (Motor 2 Forward)
GPIO.setup(23, GPIO.OUT)  # IN4 (Motor 2 Backward)

# Initialiser la bibliothèque pygame pour lire la manette
pygame.init()
pygame.joystick.init()

# Ouvrir la manette
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Créer des objets PWM pour les moteurs
pwm_motor1_forward = GPIO.PWM(17, 100)  # Fréquence de 100 Hz
pwm_motor1_backward = GPIO.PWM(27, 100)  # Fréquence de 100 Hz
pwm_motor2_forward = GPIO.PWM(22, 100)  # Fréquence de 100 Hz
pwm_motor2_backward = GPIO.PWM(23, 100)  # Fréquence de 100 Hz

# Démarrer les PWM avec une valeur de 0
pwm_motor1_forward.start(0)
pwm_motor1_backward.start(0)
pwm_motor2_forward.start(0)
pwm_motor2_backward.start(0)

# Variable pour le mode pause
pause_mode = False

# Fonction pour contrôler les moteurs
def control_motor(x_axis, y_axis):
    global pause_mode
    if pause_mode:
        # Si en pause, arrêter les moteurs
        pwm_motor1_forward.ChangeDutyCycle(0)
        pwm_motor1_backward.ChangeDutyCycle(0)
        pwm_motor2_forward.ChangeDutyCycle(0)
        pwm_motor2_backward.ChangeDutyCycle(0)
        return

    # X-axis pour tourner, Y-axis pour avancer/reculer
    if y_axis < -0.1:  # Joystick poussé vers l'avant
        pwm_motor1_forward.ChangeDutyCycle(int(abs(y_axis) * 100))  # Vitesse proportionnelle
        pwm_motor1_backward.ChangeDutyCycle(0)
        pwm_motor2_forward.ChangeDutyCycle(int(abs(y_axis) * 100))  # Vitesse proportionnelle
        pwm_motor2_backward.ChangeDutyCycle(0)
    elif y_axis > 0.1:  # Joystick poussé vers l'arrière
        pwm_motor1_forward.ChangeDutyCycle(0)
        pwm_motor1_backward.ChangeDutyCycle(int(abs(y_axis) * 100))  # Vitesse proportionnelle
        pwm_motor2_forward.ChangeDutyCycle(0)
        pwm_motor2_backward.ChangeDutyCycle(int(abs(y_axis) * 100))  # Vitesse proportionnelle
    else:  # Stopper les moteurs si le joystick est au centre
        pwm_motor1_forward.ChangeDutyCycle(0)
        pwm_motor1_backward.ChangeDutyCycle(0)
        pwm_motor2_forward.ChangeDutyCycle(0)
        pwm_motor2_backward.ChangeDutyCycle(0)

    # Contrôle de direction (gauche/droite) avec le joystick
    if x_axis > -0.1:  # Joystick déplacé à gauche
        pwm_motor1_forward.ChangeDutyCycle(int(abs(x_axis) * 100))  # Vitesse proportionnelle
        pwm_motor1_backward.ChangeDutyCycle(0)
        pwm_motor2_forward.ChangeDutyCycle(0)
        pwm_motor2_backward.ChangeDutyCycle(0)
    elif x_axis < 0.1:  # Joystick déplacé à droite
        pwm_motor1_forward.ChangeDutyCycle(0)
        pwm_motor1_backward.ChangeDutyCycle(0)
        pwm_motor2_forward.ChangeDutyCycle(int(abs(x_axis) * 100))  # Vitesse proportionnelle
        pwm_motor2_backward.ChangeDutyCycle(0)

# Boucle principale
try:
    while True:
        pygame.event.pump()  # Nécessaire pour lire les événements pygame
        # Lire les valeurs des axes du joystick
        x_axis = joystick.get_axis(0)  # Axe horizontal (gauche/droite)
        y_axis = joystick.get_axis(1)  # Axe vertical (haut/bas)

        # Vérifier si le bouton "Start" est pressé pour basculer le mode pause
        start_button = joystick.get_button(7)  # Index pour le bouton "Start" sur Xbox
        if start_button:
            pause_mode = not pause_mode  # Toggle pause mode
        time.sleep(0.5)  # Anti -bounce delay

        control_motor(x_axis, y_axis)
        
except KeyboardInterrupt:
    # Arrêter les PWM et fermer les GPIO
    pwm_motor1_forward.stop()
    pwm_motor1_backward.stop()
    pwm_motor2_forward.stop()
    pwm_motor2_backward.stop()
    GPIO.cleanup()