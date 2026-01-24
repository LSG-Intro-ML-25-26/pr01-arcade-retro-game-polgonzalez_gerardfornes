@namespace
class SpriteKind:
    Obstacle = SpriteKind.create()
    Trampolin = SpriteKind.create()

tiles.set_current_tilemap(tilemap("""prova"""))

# Variables Globales
bot_mirando_derecha = False
velocidad3 = 0
distancia3 = 0
nena: Sprite = None

# Tanques
tanque = sprites.create(assets.image("""tanque"""), SpriteKind.Obstacle)
tiles.place_on_tile(tanque, tiles.get_tile_location(116, 10))

tanque02 = sprites.create(assets.image("""tanque"""), SpriteKind.Obstacle)
tiles.place_on_tile(tanque02, tiles.get_tile_location(146, 10))

# Bot
bot = sprites.create(assets.image("""soldado0"""), SpriteKind.enemy)
tiles.place_on_tile(bot, tiles.get_tile_location(1, 7))
bot.ay = 350

# Maduro
nena = sprites.create(assets.image("""maduro"""), SpriteKind.player)
tiles.place_on_tile(nena, tiles.get_tile_location(6, 9))
nena.ay = 350
nena.set_stay_in_screen(True)
scene.camera_follow_sprite(nena)


# Minas
lista_minas = tiles.get_tiles_by_type(assets.tile("""interrogacion"""))
for i in range(len(lista_minas)):
    lugar = lista_minas[i]
    nueva_minita = sprites.create(assets.image("""minita3"""), SpriteKind.enemy)
    tiles.place_on_tile(nueva_minita, lugar)
    tiles.set_tile_at(lugar, assets.tile("""transparency16"""))

#Salto Toldos
partes_toldo = [
    assets.tile("""toldo01"""),
    assets.tile("""toldo02"""),
    assets.tile("""toldo03"""),
    assets.tile("""toldo04""")
]

for t in range(len(partes_toldo)):
    tipo_actual = partes_toldo[t]
    
    lista_lugares_toldo = tiles.get_tiles_by_type(tipo_actual)
    
    for k in range(len(lista_lugares_toldo)):
        lugar_t = lista_lugares_toldo[k]
        
        nuevo_toldo = sprites.create(tipo_actual, SpriteKind.Trampolin)
        tiles.place_on_tile(nuevo_toldo, lugar_t)
        
        tiles.set_tile_at(lugar_t, assets.tile("""transparency16"""))


# CUENTA REGRESIVA
for k in range(3):
    numero = 3 - k
    if nena:
        nena.say_text("" + str(numero), 1000, True)
    pause(1000)

if nena:
    nena.say_text("¡CORRE!", 500, True)

controller.move_sprite(nena, 100, 0)


def on_right_pressed():
    if nena:
        animation.run_image_animation(nena, assets.animation("""maduro-right0"""), 200, True)
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def on_left_pressed():
    if nena:
        animation.run_image_animation(nena, assets.animation("""maduro-left"""), 200, True)
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

def on_a_pressed():
    if nena and nena.is_hitting_tile(CollisionDirection.BOTTOM):
        nena.vy = -155
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def on_on_update():
    global distancia3, velocidad3, bot_mirando_derecha
    if not nena or not bot: return

    distancia3 = abs(nena.x - bot.x)
    if distancia3 > 90:
        velocidad3 = 320
    elif distancia3 > 30:
        velocidad3 = 190
    else:
        velocidad3 = 95
        
    if nena.x < bot.x:
        bot.vx = 0 - velocidad3
        if bot_mirando_derecha == True:
            animation.run_image_animation(bot, assets.animation("""soldado-left0"""), 500, True)
            bot_mirando_derecha = False
    else:
        bot.vx = velocidad3
        if bot_mirando_derecha == False:
            animation.run_image_animation(bot, assets.animation("""soldado-right0"""), 200, True)
            bot_mirando_derecha = True
            
    if bot.is_hitting_tile(CollisionDirection.LEFT) or bot.is_hitting_tile(CollisionDirection.RIGHT):
        if bot.is_hitting_tile(CollisionDirection.BOTTOM):
            bot.vy = -155
game.on_update(on_on_update)

def on_enemy_overlap(sprite, otherSprite):
    game.over(False)
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_enemy_overlap)

def on_toldo_overlap(sprite, otherSprite):
    if nena:
        nena.vy = -250
        
        if nena.vx > 0:
            nena.vx = 250
        else:
            nena.vx = -250
            
sprites.on_overlap(SpriteKind.player, SpriteKind.Trampolin, on_toldo_overlap)