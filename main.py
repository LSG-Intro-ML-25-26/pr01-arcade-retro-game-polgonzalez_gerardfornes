@namespace
class SpriteKind:
    Obstacle = SpriteKind.create()
    Trampolin = SpriteKind.create()

def on_on_overlap(sprite, otherSprite):
    if nena:
        nena.vy = -250
        if nena.vx > 0:
            nena.vx = 250
        else:
            nena.vx = -250
sprites.on_overlap(SpriteKind.player, SpriteKind.Trampolin, on_on_overlap)

# CONTROLES

def on_right_pressed():
    if nena:
        animation.run_image_animation(nena,
            assets.animation("""
                maduro-right0
                """),
            200,
            True)
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def on_left_pressed():
    if nena:
        animation.run_image_animation(nena,
            assets.animation("""
                maduro-left
                """),
            200,
            True)
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

# COLISIONES

def on_on_overlap2(sprite2, otherSprite2):
    game.over(False)
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap2)

def on_a_pressed():
    if nena and nena.is_hitting_tile(CollisionDirection.BOTTOM):
        nena.vy = -155
bot_mirando_derecha = False
velocidad3 = 0
distancia3 = 0
t = 0
i = 0
nena: Sprite = None
tiles.set_current_tilemap(tilemap("""
    prova
    """))
# OBJETOS FIJOS
tanque = sprites.create(assets.image("""
    tanque
    """), SpriteKind.Obstacle)
tiles.place_on_tile(tanque, tiles.get_tile_location(116, 10))
tanque02 = sprites.create(assets.image("""
    tanque
    """), SpriteKind.Obstacle)
tiles.place_on_tile(tanque02, tiles.get_tile_location(146, 10))
# PERSONAJES
bot = sprites.create(assets.image("""
    soldado0
    """), SpriteKind.enemy)
tiles.place_on_tile(bot, tiles.get_tile_location(1, 7))
bot.ay = 350
nena = sprites.create(assets.image("""
    maduro
    """), SpriteKind.player)
tiles.place_on_tile(nena, tiles.get_tile_location(6, 9))
nena.ay = 350
nena.set_stay_in_screen(True)
scene.camera_follow_sprite(nena)
# GENERADOR DE MINAS
lista_minas = tiles.get_tiles_by_type(assets.tile("""
    interrogacion
    """))
while i < len(lista_minas):
    lugar = lista_minas[i]
    nueva_minita = sprites.create(assets.image("""
        minita3
        """), SpriteKind.enemy)
    tiles.place_on_tile(nueva_minita, lugar)
    i += 1
# GENERADOR DE TOLDOS
partes_toldo = [assets.tile("""
        toldo01
        """),
    assets.tile("""
        toldo02
        """),
    assets.tile("""
        toldo03
        """),
    assets.tile("""
        toldo04
        """)]
while t < len(partes_toldo):
    tipo_actual = partes_toldo[t]
    lista_lugares_toldo = tiles.get_tiles_by_type(tipo_actual)
    k = 0
    while k < len(lista_lugares_toldo):
        lugar_t = lista_lugares_toldo[k]
        nuevo_toldo = sprites.create(tipo_actual, SpriteKind.Trampolin)
        tiles.place_on_tile(nuevo_toldo, lugar_t)
        tiles.set_tile_at(lugar_t, assets.tile("""
            transparency16
            """))
        k += 1
    t += 1
# CUENTA REGRESIVA
controller.move_sprite(nena, 0, 0)
k = 0
while k < 3:
    numero = 3 - k
    if nena:
        nena.say_text("" + str(numero), 1000, True)
    pause(1000)
    k += 1
if nena:
    nena.say_text("¡CORRE!", 500, True)
juego_empezado = True
controller.move_sprite(nena, 100, 0)
if controller.right.is_pressed():
    animation.run_image_animation(nena,
        assets.animation("""
            maduro-right0
            """),
        200,
        True)
elif controller.left.is_pressed():
    animation.run_image_animation(nena,
        assets.animation("""
            maduro-left
            """),
        200,
        True)
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)
# LÓGICA IA + SUELOS
tiles_petroleo = [assets.tile("""
        petroleo0
        """),
    assets.tile("""
        petroleo02
        """),
    assets.tile("""
        petroleo1
        """)]
tile_mina = assets.tile("""
    interrogacion
    """)

def on_on_update():
    global distancia3, velocidad3, bot_mirando_derecha
    if not (nena) or not (bot):
        return
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
    if bot.is_hitting_tile(CollisionDirection.LEFT) or bot.is_hitting_tile(CollisionDirection.RIGHT):
        if bot.is_hitting_tile(CollisionDirection.BOTTOM):
            bot.vy = -155
game.on_update(on_on_update)

mySprite20260124T233407695Z = sprites.create(img("""
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff9888fffffffff89fffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff9bfffffffffffff6bb66b66b1ffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff4555555555444ffffffffff8fffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff4555555555555fffccccfff9fffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff555555555555554455554ff1fffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff455555555555555455554ff9fffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff444444444444444455555ff9fffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffccccccccccccc44555555ff1fffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff8888888b6688ceeeeeeeeff9fffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff888888b1dd8bd88888888ff8fffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffcf88888bbcc888686b88888ff9fffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffcccccdbcccccc86d88888ff9fffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffcefffffffffffffffffffffffffffffffff8fe22222222222ec8888888ff1fffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffcefffffffffffffffffffffffffffffffffcfe222222222222ccccccccff1fffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffcefffffffffffffffffffffffffffffffff8fe222222222222eee2222eff1fffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffcefffffffffffffffffffffffffffffffff8fe222222222222eee2222eff1fffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffceffc6fffffffffffffffffffffffffffffcfceeeeeeeeeeeeeee2222eff1fffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffceffcbfffffffffffffffffffffffffffffcffffffffffffffeee2222eff1fffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffceffbccccffffffffffffffffffffffffff8fcccccccccccccffffffffff1fffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffceffdcccccccfffffffffffffffffffffffcfffffffffffff6ffffffffff9fffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffff9cfceffffffccccdb1ffffffffffffffffffffcfcffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffccfceffffffcccccccdfffffffffffffffffffcfcffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffccfcefffffffffcccccccccfffffffffffffff8fcffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffccfcefffffffffcccccccccfffffffffffffff8fcffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffccfceffffffffffffccccccccccccccffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffccfcefffffffffffff1111cccccccccffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffccfceffcccccffffffffffcccccccccccccccffefffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffccccfceffeeeeffffffcffcfffffffffcccccccfcefffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffcccffceffffffceeeefffffffffffffffffffffffefffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffcccffcefccccccfffccccccffffffffffffffffffefffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffcccffcefcbbbbcffffeeeeefffffdb99fffffffffefffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffffcccffcefcbbbbbbbbbcffffeeeeefffffffffffffefffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffcccccffcefcbbbbddbbbcccccccccccccccffffffffefffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffccc9fffcefcbdddddbbbbbbbbfffffeeeeeffffffffefffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffccc9fffcefcbbdddddddddbbbbbbbbfffffeeeecfffefffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffccc9fffcefcbbbddddddddbbbbbbbbccccccccccfffefffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffccc9fffcefcbbbdddddddddddddbbbbbbbcffffceffefffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffccc9fffcefcbdddddddddddddddddddbbbbcccccfffeffccfffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffccccffffcefcbddbddddddddddddddddbbbbbbbbcfffefcbcfffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffccccffffcefcbddbddddddddddddddddbbbbdddbbbffefcbcfffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffcccfffffcefcbdddddddddddddddddddbbbdddddbbffefcbcfffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffcccfffffcefcbbbdbbddddddddddddddbbbdddddddffefcbcfffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffcccccfffffcefcbbbddddddddddddddddbbbddddddddffefcbcfffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffcccfffffffcefcbbbdddbbdddddddddddbbbddddddddffefcbcfffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffcccfffffffcefcbbbddddddddddddddddbbbddddddddffefcbcfffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffcccfffffffcefcbbbddddddddddddddddbbbddddddddffefcbcfffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffff9cccfffffffcefcbbbddddddddddddddddbbbddddddddffefcbcfc9ffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffccfffffffffcefcbbbddddddddddddddddbbbddddddddffefcbbbff9fffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffffccfffffffffcefcbbbddddddddddddddddbddddddddddffefcdbbff9fffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffff1ccfffffffffcefcbbbbdddddddddddddddbddddddddddffefcdbbff9fffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffccbcfffffffffcefcbbbbdddddddddddddddbddddddddddffefcdbbff9fffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffccbffffffffffcefcbbbbddddddddddddddddddddddddddffefcdbbff9fffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffffffccbffffffffffcefcbbbbdddddddddddddbddddddddddddffefcdbbff8fffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffff9ccc6ffffffffffcefcbbbbddddddddddddddddddddddddddffefcdbbccfcffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffff9ccffffffffffffcefcbbbbddddddddddddddddddddddddddffefcddbbcffffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffff9ccffffffffffffcefcbbbbddddddddddddddddddddddddddffefcdddbcffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffccccffffffffffffcefcbbbbddddddddddddddddddddddddddffefcdddbcffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffcc9fffffffffffffcefcbbbbddddddddddddddddddddddddddffefcdddbcffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffccdfffffffffffffcefcbbbbddddddddddddddddddddddddddffefcdddbbbcffffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffffccc9fffffffffffffcefcbbbbddddddddddddddddddddddddddffefcdddbbbcffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffcccdffffffffffffffcefcbbbbddddddddddddddddddddddddddffefcbddddbcffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffcccfffffffffffffffcefcbbbbddddddddddddddddddddddddddffefcbddddbcffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffff6ccfffffffffffffffcefcbbbbddddddddddddddddddddddddddffefcbddddbcf1ffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffffccfffffffffffffffffcefcbbbbddddddddddbdddddddddddddddffefcbddddbbbfffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffccccfffffffffffffffffcefcbbbbddddddddddddddddddddddddddffefcbdddddbbfffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffcccffffffffffffffffffcefcbbbbdddddddddbddddddddddddddddffefcbddddddbfffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffffcccffffffffffffffffffcefcbbbbdddddddbddddddddddddddddddffefcbbdddddbfffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffcccccffffffffffffffffffcefcbbbbdddddddbddddddddddddddddddffefcbbddddbbfcf1fffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffccc1fffffffffffffffffffcefcbbbddddddbbdddddddddddddddddddffefcbbddddbbbcfdfffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffffccc1fffffffffffffffffffcefcbbbdddddbdddddddddddddddddddddffefcbbbdddddbbbffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffcccc1fffffffffffffffffffcefcbbbdddddbdddddddddddddddddddddffefcbbbdddddbbbffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffff1ccccffffffffffffffffffffcefcbbbdddbbbdddddddddddddddddddddffefcbbbdddbbbbbffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffcccccfffffffffffffffffffffcefcbbbdddbbddddddddddddddddddddddffefcbbbdddbbcccffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffcccfffffffffffffffffffffffcefcbbbdbbbbdddddddddddddddddddddbffeffbbbbbbbbfffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffcffffffffffffcccfffffffffffffffffffffffcefcbbbdbbddddddddbbbbbbbbbbbbbbbbfceffccccccccccceeeccfffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffcfffffbbffffbcccfffffffffffffffffffffffcefcbbbbbbddddddddbbbbbbbbbbbbbbbbffeffffffffffeeeeeeeefffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffcfed44ffffffccfffffffffffffffffffffffffcefcbbbbbbbbbbbbbbffffffffffffffffffeffeeeeeeeefffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffe544ffffccccfffffffffffffffffffffffffcefcbbbccccccccccccccccccccccccccfffeffcffffcccfffffffffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffe544ffffcccffffffffffffffffffffffffffcefcbbbfffffffffffeeeeeeeeeeeeeeeeffeffffffffffffffffccfffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffe544deffffcffffffffffffffffffffffffffcefffffeeeeeeeeeeeffffffffffffffffffeff1911191dffffffccfffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffe5455eeeeecffffffffffffffffffffffffffcefffffcccccccccccffffffffffffffffffeffffffffffffffffccfffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffe54554555dffffffb111bffffffffffffffffceffeecfffffffffffffffffffffffffffffeffffffffffffffffcc11fffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffcfe544555555dddddffffffffffffffffffffffceffffffffffffffffffffffffffffffffffeffffffffffffffffccccfffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffe5445555555555deccccccfffffffffffffffceffffffffffffffffffffffffffffffffffefffffffffffffffffcccfffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffe54455555555555555555efffffffffffffffceffffffffffffffffffffffffffffffffffefffffffffffffffffcccfffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffe545555555555555555554bbbbbefffffffffceffffffffffffffffffffffffffffffffffefffffffffffffffffcccccfffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffe545555555555555555555555557ffffffcfffcffffcfffffffffffffffffffffffffffffeffffffffffffffffff1ccccffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffcfe55545555555555555555555555547747dcffffffffffffffffffffffffffffffffffffffefffffffffffffffffffcccc1fffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffcfcbeee45555555555555555555555555555eeeeeeeeeefffffffffffffffffffffffffffffeffffffffffffffffffffccc1fffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffff88fe55555555555555555555555555555555555557fffffffffffffffffffffffffffffeffffffffffffffffffffccc1fffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffff888cccccce555555555555555555555555555555547bbbbbbbbefffffffffffffffffffeffffffffffffffffffffcccccffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffff888888888c44444455555555555555555555555555555555555effffffffffffffffcffcffccccccccccccccffffffcccbfffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffff888888888888888845555555555555555555555555555555555555d55555555555deffffffffffffffffffffcfffffffccfffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffff8888888888888888ceeeee4555555555555555555555555555555555555555555554eeeeeeeeeeeeeeeeeeeefffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffff8888888888888888888888c44444445455555555555555555555555555555555555555555555555555555555fffffffffffffffffffffffffffffffffffffffffffff
        ffffffffffffffffffffffffff8888888888888888888888888888888c455555555555555555555555555555555555555555555555555555555dddddddddddddddddddddddddfffffffffffffffffff
        ffffffffffffffffffffffffffc8888888888888888888888888888888ceeeeeee55555555555555555555555555555555555555555555555555555555555555555554444444fffffffffffffffffff
        ffffffffffffffffffffffffffff8888888888888888888888888888888888888845555555555555555555555555555555555555555555555555555555555555555555444444fffffffffffffffffff
        ffffffffffffffffffffffffffff88888888888888888888888888888888888888cccccccccc55555555555555555555555555555555555555555555555555555555554444cffffffffffffffffffff
        ffffffffffffffffffffffffffffcccccc88888888888888888888888888888888888888888c44444444444444445555555555555555555555555555555555555555554444fffffffffffffffffffff
        ffffffffffffffffffffffffffffe22eeec88888888888888888888888888888888888888888888888888888888c5555555555555555555555555555555555555555444444ff9ffffffffffffffffff
        fffffffffffffffffffffffffffffe2e22eeeeeec888888888888888888888888888888888888888888888888888ccccccccccccccccccccccccccccccccccccccccccccccff9ffffffffffffffffff
        fffffffffffffffffffffffffffcfe2ee2222222e8888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888ff9ffffffffffffffffff
        fffffffffffffffffffffffffffcfe2ee22222222eeeeeeeeeee88888888888888888888888888888888888888888888888888888888888888888888888888888888888888ff9ffffffffffffffffff
        fffffffffffffffffffffffffffcfceee222222222222222222ecccccccccccccc88888888888888888888888888888888888888888888888888888888888888888888888fff9ffffffffffffffffff
        ffffffffffffffffffffffffffff8ffeee2222222222222222222222222222222ec888888888888888888888888888888888888888888888888888888888888888888888fffffffffffffffffffffff
        fffffffffffffffffffffffffffffffeee222ee222222222222222222222222222eeeeeeeeeeeeeeeeeeeeeec88888888888888888888888888888888888888888888888fffffffffffffffffffffff
        fffffffffffffffffffffffffffffffeeeeeeeee222222222222222222222222222222222222222222222222eccccccccccccccccccccccccccccccccccccccffcccccfffffffffffffffffffffffff
        ffffffffffffffffffffffffffffff9ff2eeeeeeeeeee22222222222222222222222222222222222222222222eeeeeeeeeeeeeeeeeeeee22eeeeeee22222eeeeeeeeeeeff8fffffffffffffffffffff
        ffffffffffffffffffffffffffffffffcceeeeeeeeeeeee2eeeeeee2e22222222222222222222222222222222222222222222222222222222222eeee2e22eeeeeeeeeeeffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffeeeeeeeeeeeeeeeeeeeeeeee2222222222222222222222222222222222222222222222222222222eeeeeeeeeeeeeeeeeeeeeeffffffffffffffffffffffff
        ffffffffffffffffffffffffffffffff96ff2eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffcfffffffffffffffffffffff
        ffffffffffffffffffffffffffffffffffffee2eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeefffff8fffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeefffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffff88cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccfff8fffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
        """),
    SpriteKind.player)