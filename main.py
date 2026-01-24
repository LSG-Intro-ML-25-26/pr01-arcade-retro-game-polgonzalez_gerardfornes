@namespace
class SpriteKind:
    Obstacle = SpriteKind.create()

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
    if nena.is_hitting_tile(CollisionDirection.BOTTOM):
        nena.vy = -155

def on_on_overlap(sprite, otherSprite):
    game.over(False)
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap)

bot_mirando_derecha = False
velocidad3 = 0
distancia3 = 0
nena: Sprite = None
tiles.set_current_tilemap(tilemap("""
    prova
    """))
helicopter = sprites.create(assets.image("""
        helicoptero
        """),
    SpriteKind.Obstacle)
tiles.place_on_tile(helicopter, tiles.get_tile_location(60, 10))
tanque = sprites.create(assets.image("""
    tanque
    """), SpriteKind.Obstacle)
tiles.place_on_tile(tanque, tiles.get_tile_location(66, 10))

bot = sprites.create(assets.image("""
    soldado0
    """), SpriteKind.enemy)
tiles.place_on_tile(bot, tiles.get_tile_location(1, 7))
nena = sprites.create(assets.image("""
    maduro
    """), SpriteKind.player)
tiles.place_on_tile(nena, tiles.get_tile_location(6, 9))
# Crear Minas
lista_lugares = tiles.get_tiles_by_type(assets.tile("""
    interrogacion
    """))
for lugar in lista_lugares:
    nueva_minita = sprites.create(assets.image("""
        minita3
        """), SpriteKind.enemy)
    tiles.place_on_tile(nueva_minita, lugar)
    tiles.set_tile_at(lugar, assets.tile("""
        transparency16
        """))
nena.ay = 350
bot.ay = 350
nena.set_stay_in_screen(True)
scene.camera_follow_sprite(nena)
#CUENTA REGRESIVA
controller.move_sprite(nena, 0, 0)
for i in range(3):
    numero = 3 - i
    nena.say_text("" + str(numero), 1000, True)
    pause(1000)
nena.say_text("¡CORRE!", 500, True)
controller.move_sprite(nena, 100, 0)
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def on_on_update():
    global distancia3, velocidad3, bot_mirando_derecha
    distancia3 = abs(nena.x - bot.x)
    if distancia3 > 90:
        velocidad3 = 320
    elif distancia3 > 30:
        velocidad3 = 190
    else:
        velocidad3 = 95
    # Movimiento Bot
    if nena.x < bot.x:
        bot.vx = 0 - velocidad3
        if bot_mirando_derecha == True:
            animation.run_image_animation(bot,
                assets.animation("""
                    soldado-left0
                    """),
                500,
                True)
            bot_mirando_derecha = False
    else:
        bot.vx = velocidad3
        if bot_mirando_derecha == False:
            animation.run_image_animation(bot,
                assets.animation("""
                    soldado-right0
                    """),
                200,
                True)
            bot_mirando_derecha = True
    # Salto Bot
    if bot.is_hitting_tile(CollisionDirection.LEFT) or bot.is_hitting_tile(CollisionDirection.RIGHT):
        if bot.is_hitting_tile(CollisionDirection.BOTTOM):
            bot.vy = -155
game.on_update(on_on_update)
