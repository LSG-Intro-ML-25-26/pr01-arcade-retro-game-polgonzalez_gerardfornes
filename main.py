@namespace
class SpriteKind:
    Obstacle = SpriteKind.create()
# Variables Globales

def on_right_pressed():
    animation.run_image_animation(nena,
        assets.animation("""
            maduro-right0
            """),
        200,
        True)
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def on_left_pressed():
    animation.run_image_animation(nena,
        assets.animation("""
            maduro-left
            """),
        200,
        True)
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

def on_a_pressed():
    # Solo salta si está tocando el suelo
    if nena.is_hitting_tile(CollisionDirection.BOTTOM):
        nena.vy = -155

def on_on_overlap(sprite, otherSprite):
    game.over(False)
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap)

bot_mirando_derecha = False
velocidad3 = 0
distancia3 = 0
nena: Sprite = None
# Cargar Mapa
tiles.set_current_tilemap(tilemap("""
    prova
    """))
helicopter = sprites.create(assets.image("""
        helicoptero
        """),
    SpriteKind.Obstacle)
tanque = sprites.create(assets.image("""
    tanque
    """), SpriteKind.Obstacle)
minita = sprites.create(assets.image("""
    minita
    """), SpriteKind.enemy)
# Crear Bot (Soldado)
bot = sprites.create(assets.image("""
    soldado0
    """), SpriteKind.enemy)
# Crear Jugador (Maduro)
nena = sprites.create(assets.image("""
    maduro
    """), SpriteKind.player)
# Posicionar personajes
tiles.place_on_tile(tanque, tiles.get_tile_location(33, 10))
# Posicionar personajes
tiles.place_on_tile(helicopter, tiles.get_tile_location(60, 10))
# Posicionar personajes
tiles.place_on_tile(minita, tiles.get_tile_location(15, 11))
# Posicionar personajes
tiles.place_on_tile(nena, tiles.get_tile_location(6, 9))
tiles.place_on_tile(bot, tiles.get_tile_location(1, 7))
# Físicas
nena.ay = 350
bot.ay = 350
controller.move_sprite(nena, 100, 0)
nena.set_stay_in_screen(True)
scene.camera_follow_sprite(nena)
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def on_on_update():
    global distancia3, velocidad3, bot_mirando_derecha
    # Calcular distancia entre Jugador y Bot
    distancia3 = abs(nena.x - bot.x)
    # Ajustar velocidad según distancia (Efecto Goma Elástica)
    if distancia3 > 120:
        # Muy rápido si está lejos
        velocidad3 = 300
    elif distancia3 > 60:
        # Rápido
        velocidad3 = 170
    else:
        # Normal
        velocidad3 = 95
    # Movimiento y Animación del Bot
    if nena.x < bot.x:
        # Ir a la IZQUIERDA
        bot.vx = 0 - velocidad3
        if bot_mirando_derecha == True:
            animation.run_image_animation(bot,
                assets.animation("""
                    soldado-left
                    """),
                200,
                True)
            bot_mirando_derecha = False
    else:
        # Ir a la DERECHA
        bot.vx = velocidad3
        if bot_mirando_derecha == False:
            animation.run_image_animation(bot,
                assets.animation("""
                    soldado-right0
                    """),
                200,
                True)
            bot_mirando_derecha = True
    # Salto automático de obstáculos del Bot
    if bot.is_hitting_tile(CollisionDirection.LEFT) or bot.is_hitting_tile(CollisionDirection.RIGHT):
        if bot.is_hitting_tile(CollisionDirection.BOTTOM):
            bot.vy = -155
game.on_update(on_on_update)
