@namespace
class SpriteKind:
    Obstacle = SpriteKind.create()
    Trampolin = SpriteKind.create()
    IconoNivel = SpriteKind.create()
    Cursor = SpriteKind.create()
    UI = SpriteKind.create()
    Fondo = SpriteKind.create()
    Meta = SpriteKind.create()

bot_mirando_derecha = False
velocidad3 = 0
distancia3 = 0
juego_empezado = False
tiempo_inicio = 0

nivel_desbloqueado = 1
nivel_actual = 0

nena: Sprite = None
bot: Sprite = None
tanque: Sprite = None
tanque02: Sprite = None

icono1: Sprite = None
icono2: Sprite = None
icono3: Sprite = None

def menu_inicial():
    if assets.image("escape-to-usa2"):
        scene.set_background_image(assets.image("escape-to-usa2"))
    
    if assets.image("bigButtonPressed2"):
        boton_play = sprites.create(assets.image("bigButtonPressed2"), SpriteKind.UI)
        boton_play.set_position(80, 110)
        pause(500)
        while not controller.A.is_pressed():
            if (game.runtime() % 800) < 400:
                boton_play.say_text("PLAY", 500, False)
            else:
                boton_play.say_text("")
            pause(20)
        boton_play.destroy()
    else:
        while not controller.A.is_pressed():
            pause(100)
            
    cinematica_lore()

def cinematica_lore():
    if assets.image("mapausa"):
        scene.set_background_image(assets.image("mapausa"))
    else:
        scene.set_background_color(15)
    game.show_long_text("El mundo pensaba que lo había visto todo, hasta que el 'Caudillo de Wall Street' decidió que la diplomacia era demasiado lenta y aburrida.", DialogLayout.BOTTOM)

    if assets.image("trumpworld"):
        scene.set_background_image(assets.image("trumpworld"))
    game.show_long_text("En un movimiento que nadie vio venir —principalmente porque no tiene sentido legal—, el rubio más famoso de Florida ha 'adquirido' un activo internacional de gran tamaño.", DialogLayout.BOTTOM)

    if assets.image("maduropurple"):
        scene.set_background_image(assets.image("maduropurple"))
    game.show_long_text("Sí... Maduro ha sido secuestrado. Narcolás Maduro AKA 'El Exiliado del Caribe', ahora es propiedad privada.", DialogLayout.BOTTOM)

    if assets.image("madurobros"):
        scene.set_background_image(assets.image("madurobros"))
    game.show_long_text("La situación es insostenible. El Servicio Secreto está confundido, el SEBIN está en pánico y Twitter... bueno, X... como quieran llamarle, sigue igual de tóxico que siempre.", DialogLayout.BOTTOM)

    if assets.image("cara feliz"):
        scene.set_background_image(assets.image("cara feliz"))
    
    game.show_long_text("Tu trabajo no es juzgar la legalidad de esta locura, ni velar por los intereses de ningún país en concreto.", DialogLayout.BOTTOM)
    game.show_long_text("Tu misión es intervenir antes de que 'Tu Patito Favorito' A.K.A YFD (Your Favorite Duck) aplique su política de America First convirtiendo a Maduro en el primer souvenir humano de su nueva franquicia.", DialogLayout.BOTTOM)
    game.show_long_text("Prepárate para la extracción más políticamente incorrecta de la historia. Inserte moneda para evitar la Tercera Guerra Mundial.", DialogLayout.BOTTOM)

    if assets.image("pokemon"):
        scene.set_background_image(assets.image("pokemon"))
        pause(2000)
        game.show_long_text("¡EMPIEZA LA MISIÓN!", DialogLayout.CENTER)

    selector_de_mapa()

def selector_de_mapa():
    global juego_empezado, nena, bot, icono1, icono2, icono3
    
    juego_empezado = False
    nena = None
    bot = None
    
    info.set_score(0)
    info.show_score(False)
    
    scene.set_background_image(None)
    scene.set_background_color(9)
    
    sprites.destroy_all_sprites_of_kind(SpriteKind.player)
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Obstacle)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Trampolin)
    sprites.destroy_all_sprites_of_kind(SpriteKind.UI)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Meta)
    
    pause(500)
    
    if assets.tile("mundo_grande"):
        tiles.set_current_tilemap(tilemap("mundo_grande"))
    else:
        tiles.set_current_tilemap(tilemap("level1"))

    if assets.image("mapamundi2"):
        mapa_visual = sprites.create(assets.image("mapamundi2"), SpriteKind.Fondo)
        mapa_visual.z = -100
        mapa_visual.set_flag(SpriteFlag.GHOST, True)
        mapa_visual.set_position(400, 400)
    
    cursor = sprites.create(assets.image("maduro"), SpriteKind.Cursor)
    tiles.place_on_tile(cursor, tiles.get_tile_location(10, 26))
    
    controller.move_sprite(cursor, 150, 150)
    scene.camera_follow_sprite(cursor)
    cursor.set_stay_in_screen(True)
    
    if assets.image("venezuela0"):
        icono1 = sprites.create(assets.image("venezuela0"), SpriteKind.IconoNivel)
        tiles.place_on_tile(icono1, tiles.get_tile_location(12, 26))
        if nivel_desbloqueado > 1:
            icono1.say_text("OK", 50000, False)
        else:
            icono1.say_text("1", 50000, False)

    if assets.image("barco venezuela"):
        icono2 = sprites.create(assets.image("barco venezuela"), SpriteKind.IconoNivel)
        tiles.place_on_tile(icono2, tiles.get_tile_location(16, 18))
        
        if nivel_desbloqueado >= 2:
            icono2.say_text("2", 50000, False)
        else:
            icono2.say_text("X", 50000, False)

    if assets.image("comunista"):
        icono3 = sprites.create(assets.image("comunista"), SpriteKind.IconoNivel)
        tiles.place_on_tile(icono3, tiles.get_tile_location(37, 9))
        icono3.say_text("3", 50000, False)
    
    game.splash("Elige un nivel")

def on_mapa_overlap(sprite, otherSprite):
    if controller.A.is_pressed():
        
        if otherSprite == icono1:
            iniciar_nivel_1()
            
        elif otherSprite == icono2:
            if nivel_desbloqueado >= 2:
                game.splash("Nivel 2", "¡Huye del ejército!")
                iniciar_nivel_2()
            else:
                game.splash("BLOQUEADO", "Completa el Nivel 1 primero")
            pause(500)
            
        elif otherSprite == icono3:
            if nivel_desbloqueado >= 3:
                game.splash("Nivel 3", "¡Próximamente!")
            else:
                game.splash("BLOQUEADO", "Completa el Nivel 2 primero")
            pause(500)

sprites.on_overlap(SpriteKind.Cursor, SpriteKind.IconoNivel, on_mapa_overlap)

def iniciar_nivel_1():
    global tanque, tanque02, bot, nena, juego_empezado, tiempo_inicio, nivel_actual
    
    nivel_actual = 1
    
    sprites.destroy_all_sprites_of_kind(SpriteKind.Fondo)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Cursor)
    sprites.destroy_all_sprites_of_kind(SpriteKind.IconoNivel)
    scene.set_background_image(None)
    
    info.show_score(True)
    info.set_score(0)
    tiempo_inicio = game.runtime()
    
    tiles.set_current_tilemap(tilemap("prova"))
    
    tanque = sprites.create(assets.image("tanque"), SpriteKind.Obstacle)
    tiles.place_on_tile(tanque, tiles.get_tile_location(116, 10))
    tanque02 = sprites.create(assets.image("tanque"), SpriteKind.Obstacle)
    tiles.place_on_tile(tanque02, tiles.get_tile_location(146, 10))
    
    mySpriteBarco = sprites.create(assets.image("barco venezuela"), SpriteKind.Meta)
    tiles.place_on_tile(mySpriteBarco, tiles.get_tile_location(245, 10))
    
    bot = sprites.create(assets.image("soldado0"), SpriteKind.enemy)
    tiles.place_on_tile(bot, tiles.get_tile_location(1, 7))
    bot.ay = 350
    
    nena = sprites.create(assets.image("maduro"), SpriteKind.player)
    tiles.place_on_tile(nena, tiles.get_tile_location(6, 9))
    nena.ay = 350
    nena.set_stay_in_screen(True)
    scene.camera_follow_sprite(nena)
    
    lista_minas = tiles.get_tiles_by_type(assets.tile("interrogacion"))
    i = 0
    while i < len(lista_minas):
        lugar = lista_minas[i]
        nueva_minita = sprites.create(assets.image("minita3"), SpriteKind.enemy)
        tiles.place_on_tile(nueva_minita, lugar)
        i += 1
        
    partes_toldo = [
        assets.tile("toldo01"), assets.tile("toldo02"),
        assets.tile("toldo03"), assets.tile("toldo04")
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
            tiles.set_tile_at(lugar_t, assets.tile("transparency16"))
            k += 1
        t += 1
        
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
        animation.run_image_animation(nena, assets.animation("maduro-right0"), 200, True)
    elif controller.left.is_pressed():
        animation.run_image_animation(nena, assets.animation("maduro-left"), 200, True)

def iniciar_nivel_2():
    global bot, nena, juego_empezado, tiempo_inicio, nivel_actual
    
    nivel_actual = 2
    
    sprites.destroy_all_sprites_of_kind(SpriteKind.Fondo)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Cursor)
    sprites.destroy_all_sprites_of_kind(SpriteKind.IconoNivel)
    scene.set_background_image(None)
    
    info.show_score(True)
    info.set_score(0)
    tiempo_inicio = game.runtime()
    
    tiles.set_current_tilemap(tilemap("nivel02"))
    
    nena = sprites.create(assets.image("maduro"), SpriteKind.player)
    tiles.place_on_tile(nena, tiles.get_tile_location(7, 10))
    nena.ay = 350
    nena.set_stay_in_screen(True)
    scene.camera_follow_sprite(nena)
    
    bot = sprites.create(assets.image("usarmy"), SpriteKind.enemy)
    tiles.place_on_tile(bot, tiles.get_tile_location(4, 10))
    bot.ay = 350
    bot.set_bounce_on_wall(True)
    
    mySpriteBarco = sprites.create(assets.image("barco venezuela"), SpriteKind.Meta)
    tiles.place_on_tile(mySpriteBarco, tiles.get_tile_location(50, 10))
    
    juego_empezado = True
    controller.move_sprite(nena, 100, 0)

def game_over_personalizado():
    global juego_empezado
    juego_empezado = False
    game.splash("¡HAS MUERTO!", "Volviendo al mapa...")
    selector_de_mapa()

def on_nivel_completado(sprite, otherSprite):
    global nivel_desbloqueado
    
    tiempo_final = info.score()
    
    if nivel_actual == 1:
        game.splash("¡NIVEL 1 SUPERADO!", "Tiempo: " + str(tiempo_final) + "s")
        if nivel_desbloqueado < 2:
            nivel_desbloqueado = 2
            game.splash("¡NIVEL 2 DESBLOQUEADO!")
            
    elif nivel_actual == 2:
        game.splash("¡NIVEL 2 SUPERADO!", "Tiempo: " + str(tiempo_final) + "s")
        if nivel_desbloqueado < 3:
            nivel_desbloqueado = 3
            game.splash("¡NIVEL 3 DESBLOQUEADO!")
    
    selector_de_mapa()

sprites.on_overlap(SpriteKind.player, SpriteKind.Meta, on_nivel_completado)

def on_on_overlap(sprite, otherSprite):
    if nena:
        nena.vy = -250
        if nena.vx > 0:
            nena.vx = 250
        else:
            nena.vx = -250
sprites.on_overlap(SpriteKind.player, SpriteKind.Trampolin, on_on_overlap)

def on_right_pressed():
    if nena:
        animation.run_image_animation(nena, assets.animation("maduro-right0"), 200, True)
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def on_left_pressed():
    if nena:
        animation.run_image_animation(nena, assets.animation("maduro-left"), 200, True)
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

def on_a_pressed():
    if nena and nena.is_hitting_tile(CollisionDirection.BOTTOM):
        nena.vy = -155
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def on_on_overlap2(sprite2, otherSprite2):
    game_over_personalizado()
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap2)

tiles_petroleo = [
    assets.tile("petroleo0"), assets.tile("petroleo02"), assets.tile("petroleo1")
]
tile_mina = assets.tile("interrogacion")

def on_on_update():
    global distancia3, velocidad3, bot_mirando_derecha
    
    if juego_empezado:
        tiempo_actual = game.runtime()
        segundos = int((tiempo_actual - tiempo_inicio) / 1000)
        info.set_score(segundos)
    
    if not nena or not bot:
        return

    if juego_empezado:
        loc_actual = nena.tilemap_location()
        columna = loc_actual.column
        fila_abajo = loc_actual.row + 1
        ubicacion_suelo = tiles.get_tile_location(columna, fila_abajo)
        imagen_suelo = tiles.tile_image_at_location(ubicacion_suelo)
        
        if imagen_suelo == tile_mina:
            game_over_personalizado()
            return
            
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

        distancia3 = abs(nena.x - bot.x)
        
        if nivel_actual == 1:
            if distancia3 > 90:
                velocidad3 = 320
            elif distancia3 > 30:
                velocidad3 = 190
            else:
                velocidad3 = 95
        
        elif nivel_actual == 2:
            if distancia3 > 80:
                velocidad3 = 70
            else:
                velocidad3 = 40
                
        if nena.x < bot.x:
            bot.vx = 0 - velocidad3
            if nivel_actual == 1:
                if bot_mirando_derecha == True:
                    animation.run_image_animation(bot, assets.animation("soldado-left0"), 500, True)
                    bot_mirando_derecha = False
        else:
            bot.vx = velocidad3
            if nivel_actual == 1:
                if bot_mirando_derecha == False:
                    animation.run_image_animation(bot, assets.animation("soldado-right0"), 200, True)
                    bot_mirando_derecha = True
                
        if bot.is_hitting_tile(CollisionDirection.LEFT) or bot.is_hitting_tile(CollisionDirection.RIGHT):
            if bot.is_hitting_tile(CollisionDirection.BOTTOM):
                bot.vy = -155
game.on_update(on_on_update)

menu_inicial()