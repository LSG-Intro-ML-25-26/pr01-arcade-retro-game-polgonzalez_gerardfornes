@namespace
class SpriteKind:
    Obstacle = SpriteKind.create()
    Trampolin = SpriteKind.create()

tiles.set_current_tilemap(tilemap("""prova"""))

bot_mirando_derecha = False
velocidad3 = 0
distancia3 = 0
nena: Sprite = None
juego_empezado = False

# OBJETOS FIJOS
tanque = sprites.create(assets.image("""tanque"""), SpriteKind.Obstacle)
tiles.place_on_tile(tanque, tiles.get_tile_location(116, 10))
tanque02 = sprites.create(assets.image("""tanque"""), SpriteKind.Obstacle)
tiles.place_on_tile(tanque02, tiles.get_tile_location(146, 10))

# PERSONAJES
bot = sprites.create(assets.image("""soldado0"""), SpriteKind.enemy)
tiles.place_on_tile(bot, tiles.get_tile_location(1, 7))
bot.ay = 350

nena = sprites.create(assets.image("""maduro"""), SpriteKind.player)
tiles.place_on_tile(nena, tiles.get_tile_location(6, 9))
nena.ay = 350
nena.set_stay_in_screen(True)
scene.camera_follow_sprite(nena)

# GENERADOR DE MINAS
lista_minas = tiles.get_tiles_by_type(assets.tile("""interrogacion"""))
i = 0
while i < len(lista_minas):
    lugar = lista_minas[i]
    nueva_minita = sprites.create(assets.image("""minita3"""), SpriteKind.enemy)
    tiles.place_on_tile(nueva_minita, lugar)
    i += 1

# GENERADOR DE TOLDOS
partes_toldo = [
    assets.tile("""toldo01"""),
    assets.tile("""toldo02"""),
    assets.tile("""toldo03"""),
    assets.tile("""toldo04""")
]

t = 0
while t < len(partes_toldo):
    tipo_actual = partes_toldo[t]
    lista_lugares_toldo = tiles.get_tiles_by_type(tipo_actual)
    k = 0
    while k < len(lista_lugares_toldo):
        lugar_t = lista_lugares_toldo[k]
        nuevo_toldo = sprites.create(tipo_actual, SpriteKind.Trampolin)
        tiles.place_on_tile(nuevo_toldo, lugar_t)
        tiles.set_tile_at(lugar_t, assets.tile("""transparency16"""))
        k += 1
    t += 1

# CUENTA REGRESIVA
controller.move_sprite(nena, 0, 0)

k = 0
while k < 3:
    numero = 3 - k
    if nena:
        nena.say_text(str(numero), 1000, True)
    pause(1000)
    k += 1

if nena:
    nena.say_text("¡CORRE!", 500, True)

juego_empezado = True
controller.move_sprite(nena, 100, 0)

if controller.right.is_pressed():
    animation.run_image_animation(nena, assets.animation("""maduro-right0"""), 200, True)
elif controller.left.is_pressed():
    animation.run_image_animation(nena, assets.animation("""maduro-left"""), 200, True)


# CONTROLES
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


# LÓGICA IA + SUELOS

tiles_petroleo = [
    assets.tile("""petroleo0"""),
    assets.tile("""petroleo02"""),
    assets.tile("""petroleo1""")
]
tile_mina = assets.tile("""interrogacion""")

def on_on_update():
    global distancia3, velocidad3, bot_mirando_derecha
    if not nena or not bot: return

    if juego_empezado:
        loc_actual = nena.tilemap_location()
        columna = loc_actual.column
        fila_abajo = loc_actual.row + 1
        ubicacion_suelo = tiles.get_tile_location(columna, fila_abajo)
        
        imagen_suelo = tiles.tile_image_at_location(ubicacion_suelo)
        
        # 1. MINAS
        if imagen_suelo == tile_mina:
            game.over(False)
            return

        # 2. PETRÓLEO
        estoy_en_petroleo = False
        for aceite in tiles_petroleo:
            if imagen_suelo == aceite:
                estoy_en_petroleo = True
                break
        
        if nena.is_hitting_tile(CollisionDirection.BOTTOM):
            if estoy_en_petroleo:
                controller.move_sprite(nena, 20, 0)
            else:
                controller.move_sprite(nena, 100, 0)

    # IA DEL BOT
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

# COLISIONES

def on_enemy_overlap(sprite2, otherSprite2):
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