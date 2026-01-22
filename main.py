def on_right_pressed():
    animation.run_image_animation(nena,
        assets.animation("""
            maduro-right0
            """),
        500,
        True)
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def on_left_pressed():
    animation.run_image_animation(nena,
        assets.animation("""
            maduro-left
            """),
        500,
        True)
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

# Boton saltar + gravetat
def on_a_pressed():
    if nena.is_hitting_tile(CollisionDirection.BOTTOM):
        nena.vy = -150
velocidad2 = 0
distancia2 = 0
nena: Sprite = None
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
nena.ay = 350
controller.move_sprite(nena, 100, 0)
nena.set_stay_in_screen(True)
bot.ay = 350
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)
scene.camera_follow_sprite(nena)

bot_mirando_derecha = False

def on_update():
    global bot_mirando_derecha
    
    distancia = abs(nena.x - bot.x)
    velocidad = 0
    if distancia > 120:
        velocidad = 300
    elif distancia > 60:
        velocidad = 170
    else:
        velocidad = 95

    if nena.x < bot.x:
        bot.vx = -velocidad
        
        if bot_mirando_derecha == True:
            animation.run_image_animation(bot, assets.animation("""soldado-left"""), 200, True)
            bot_mirando_derecha = False

    else:
        bot.vx = velocidad
        
        if bot_mirando_derecha == False:
            animation.run_image_animation(bot, assets.animation("""soldado-right"""), 200, True)
            bot_mirando_derecha = True

    if bot.is_hitting_tile(CollisionDirection.LEFT) or bot.is_hitting_tile(CollisionDirection.RIGHT):
        if bot.is_hitting_tile(CollisionDirection.BOTTOM):
            bot.vy = -150

game.on_update(on_update)