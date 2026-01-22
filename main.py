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

# Boton saltar + gravetat
def on_a_pressed():
    if nena.is_hitting_tile(CollisionDirection.BOTTOM):
        nena.vy = -150
bot_mirando_derecha = False
velocidad3 = 0
distancia3 = 0
nena: Sprite = None
velocidad2 = 0
distancia2 = 0
distancia = 0
velocidad = 0
tiles.set_current_tilemap(tilemap("""
    prova
    """))
bot = sprites.create(assets.image("""
    soldado
    """), SpriteKind.enemy)
nena = sprites.create(assets.image("""
    maduro
    """), SpriteKind.player)
tiles.place_on_tile(nena, tiles.get_tile_location(6, 14))
tiles.place_on_tile(bot, tiles.get_tile_location(1, 10))
nena.ay = 350
controller.move_sprite(nena, 100, 0)
nena.set_stay_in_screen(True)
bot.ay = 350
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)
scene.camera_follow_sprite(nena)

def on_on_update():
    global distancia3, velocidad3, bot_mirando_derecha
    distancia3 = abs(nena.x - bot.x)
    if distancia3 > 120:
        velocidad3 = 300
    elif distancia3 > 60:
        velocidad3 = 170
    else:
        velocidad3 = 95
    if nena.x < bot.x:
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
        bot.vx = velocidad3
        if bot_mirando_derecha == False:
            animation.run_image_animation(bot,
                assets.animation("""
                    soldado-right
                    """),
                200,
                True)
            bot_mirando_derecha = True
    if bot.is_hitting_tile(CollisionDirection.LEFT) or bot.is_hitting_tile(CollisionDirection.RIGHT):
        if bot.is_hitting_tile(CollisionDirection.BOTTOM):
            bot.vy = -150
game.on_update(on_on_update)

def on_overlap(sprite, otherSprite):
    game.over(False)

sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_overlap)