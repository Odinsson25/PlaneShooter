WIN_SCORE = [
    700,
    1200,
    1500,
    2100,
    2500,
    2800,
    3000,
    3500,
    4200,
    4700,
    5000
] 
""" 
    Laatste in de array is "final score", hierna stopt het spel.
    Bij de andere score's komen er meer enemies & gaan ze sneller (aanpasbaar met enemy_speed_mp) 
""" 

ADDED_SCORE: int = 100 # Score die word toegevoegd na het doden van een enemy
enemy_speed_mp: int = 1.35 # Hoeveel sneller de enemy gaat na een "Level Up"
enemy_speed: int = 2  # Startsnelheid van enemy


# Hier niet aanzitten, tenzij je weet wat je doet ;)
SCREEN_WIDTH: int = 480
SCREEN_HEIGHT: int = 800
