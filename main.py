@namespace
class SpriteKind:
    Obstacle = SpriteKind.create()
    Trampolin = SpriteKind.create()
    IconoNivel = SpriteKind.create()
    Cursor = SpriteKind.create()
    UI = SpriteKind.create()
    Fondo = SpriteKind.create()
    Meta = SpriteKind.create()
    # Projectile existe por defecto

# --- 1. VARIABLES GLOBALES ---
bot_mirando_derecha = False
velocidad3 = 0
distancia3 = 0
juego_empezado = False
tiempo_inicio = 0
probabilidad_bomba = 100

# PROGRESO
nivel_desbloqueado = 1
nivel_actual = 0

# Personajes y objetos
nena: Sprite = None
bot: Sprite = None
tanque: Sprite = None
tanque02: Sprite = None
mySpriteBarco: Sprite = None
mySpriteBarco2: Sprite = None

# Variable cursor
cursor: Sprite = None

# Variables para los iconos
icono1: Sprite = None
icono2: Sprite = None
icono3: Sprite = None

# Listas y contadores
lista_cursores: List[Sprite] = []
l = 0
t = 0
partes_toldo: List[Image] = []
i = 0
lista_minas: List[tiles.Location] = []
tiempo_final = 0

# ---------------------------------------------------------
# FASE 1: MENÚ INICIAL
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# FASE 2: CINEMÁTICA
# ---------------------------------------------------------
def cinematica_lore():
    if assets.image("mapausa"):
        scene.set_background_image(assets.image("mapausa"))
    else:
        scene.set_background_color(15)
    game.show_long_text("El mundo pensaba que lo había visto todo...", DialogLayout.BOTTOM)
    selector_de_mapa()

# ---------------------------------------------------------
# FASE 3: SELECTOR DE MAPA
# ---------------------------------------------------------
def selector_de_mapa():
    global juego_empezado, nena, bot, icono1, icono2, icono3, cursor
    
    juego_empezado = False
    nena = None
    bot = None
    
    info.set_score(0)
    info.show_score(False)
    
    scene.set_background_image(None)
    scene.set_background_color(9)
    
    # Limpieza segura
    pause(100)
    sprites.destroy_all_sprites_of_kind(SpriteKind.player)
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Obstacle)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Trampolin)
    sprites.destroy_all_sprites_of_kind(SpriteKind.UI)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Meta)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Fondo)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Projectile)
    pause(200)
    
    # 1. TILEMAP
    if assets.tile("mundo_grande"):
        tiles.set_current_tilemap(tilemap("mundo_grande"))
    else:
        tiles.set_current_tilemap(tilemap("level1"))

    # 2. FONDO GIGANTE
    if assets.image("mapamundi2"):
        mapa_visual = sprites.create(assets.image("mapamundi2"), SpriteKind.Fondo)
        mapa_visual.z = -100
        mapa_visual.set_flag(SpriteFlag.GHOST, True)
        mapa_visual.set_position(400, 400)
    
    # 3. CURSOR
    cursor = sprites.create(assets.image("maduro"), SpriteKind.Cursor)
    tiles.place_on_tile(cursor, tiles.get_tile_location(10, 26))
    
    controller.move_sprite(cursor, 150, 150)
    scene.camera_follow_sprite(cursor)
    cursor.set_stay_in_screen(True)
    
    # --- PUNTOS DE NIVEL ---
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
        if nivel_desbloqueado >= 3:
            icono3.say_text("3", 50000, False)
        else:
            icono3.say_text("X", 50000, False)
    
    game.splash("Elige un nivel")

# --- LÓGICA DE CHOQUE EN EL MAPA ---
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
                game.splash("Nivel 3", "¡Guerra Aérea!")
                iniciar_nivel_3()
            else:
                game.splash("BLOQUEADO", "Completa el Nivel 2 primero")
            pause(500)

sprites.on_overlap(SpriteKind.Cursor, SpriteKind.IconoNivel, on_mapa_overlap)

# ---------------------------------------------------------
# FASE 4: JUEGO REAL (NIVEL 1)
# ---------------------------------------------------------
def iniciar_nivel_1():
    global tanque, tanque02, bot, nena, juego_empezado, tiempo_inicio, nivel_actual, mySpriteBarco, i, t, probabilidad_bomba
    
    nivel_actual = 1
    probabilidad_bomba = 100
    
    sprites.destroy_all_sprites_of_kind(SpriteKind.Fondo)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Cursor)
    sprites.destroy_all_sprites_of_kind(SpriteKind.IconoNivel)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Projectile)
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

# ---------------------------------------------------------
# FASE 5: JUEGO REAL (NIVEL 2)
# ---------------------------------------------------------
def iniciar_nivel_2():
    global nivel_actual, nena, bot, mySpriteBarco2, l, juego_empezado, tiempo_inicio, probabilidad_bomba
    
    nivel_actual = 2
    probabilidad_bomba = 100
    
    sprites.destroy_all_sprites_of_kind(SpriteKind.Fondo)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Cursor)
    sprites.destroy_all_sprites_of_kind(SpriteKind.IconoNivel)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Projectile)
    scene.set_background_image(None)
    
    info.show_score(True)
    info.set_score(0)
    
    tiles.set_current_tilemap(tilemap("nivel02"))

    img_ola = None
    if assets.image("ola"):
        img_ola = assets.image("ola")
    else:
        img_ola = img("""
            8 8 8 8 8 8 8 8
            8 8 8 8 8 8 8 8
            8 8 8 8 8 8 8 8
            8 8 8 8 8 8 8 8
        """)

    ola1 = sprites.create(img_ola, SpriteKind.Fondo)
    tiles.place_on_tile(ola1, tiles.get_tile_location(15, 12))
    ola1.z = 1
    ola1.ay = 0
    ola1.set_flag(SpriteFlag.GHOST, True)

    ola2 = sprites.create(img_ola, SpriteKind.Fondo)
    tiles.place_on_tile(ola2, tiles.get_tile_location(30, 13))
    ola2.z = 1
    ola2.ay = 0
    ola2.set_flag(SpriteFlag.GHOST, True)

    ola3 = sprites.create(img_ola, SpriteKind.Fondo)
    tiles.place_on_tile(ola3, tiles.get_tile_location(45, 12))
    ola3.z = 1
    ola3.ay = 0
    ola3.set_flag(SpriteFlag.GHOST, True)
    
    if assets.image("maduro-lancha-right"):
        nena = sprites.create(assets.image("maduro-lancha-right"), SpriteKind.player)
    else:
        nena = sprites.create(assets.image("maduro"), SpriteKind.player)
    
    nena.z = 2
    tiles.place_on_tile(nena, tiles.get_tile_location(11, 10))
    nena.ay = 350
    nena.set_stay_in_screen(True)
    scene.camera_follow_sprite(nena)
    
    bot = sprites.create(assets.image("usarmy"), SpriteKind.enemy)
    tiles.place_on_tile(bot, tiles.get_tile_location(4, 9))
    bot.ay = 350
    bot.set_bounce_on_wall(True)
    
    mySpriteBarco2 = sprites.create(assets.image("barco venezuela"), SpriteKind.Meta)
    tiles.place_on_tile(mySpriteBarco2, tiles.get_tile_location(240, 10))
    
    controller.move_sprite(nena, 0, 0)
    
    l = 0
    while l < 3:
        numero_cuenta = 3 - l
        if nena:
            nena.say_text(str(numero_cuenta), 1000, True)
        pause(1000)
        l += 1
        
    if nena:
        nena.say_text("¡YA!", 500, True)
    
    juego_empezado = True
    controller.move_sprite(nena, 100, 0)
    
    tiempo_inicio = game.runtime()

# ---------------------------------------------------------
# FASE 6: JUEGO REAL (NIVEL 3) - ¡AÉREO!
# ---------------------------------------------------------
def iniciar_nivel_3():
    global nivel_actual, nena, bot, juego_empezado, tiempo_inicio, probabilidad_bomba
    
    nivel_actual = 3
    
    # Limpieza
    sprites.destroy_all_sprites_of_kind(SpriteKind.Fondo)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Cursor)
    sprites.destroy_all_sprites_of_kind(SpriteKind.IconoNivel)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Projectile)
    sprites.destroy_all_sprites_of_kind(SpriteKind.enemy)
    sprites.destroy_all_sprites_of_kind(SpriteKind.Meta)
    scene.set_background_image(None)
    scene.set_background_color(9) # Cielo azul
    
    info.show_score(True)
    info.set_score(0)
    
    # Cargar Tilemap Nivel 3
    tiles.set_current_tilemap(tilemap("nivel03"))
    
    # --- JUGADOR (AVIÓN VENEZOLANO) ---
    img_avion = None
    if assets.image("maduro-avion-right"):
        img_avion = assets.image("maduro-avion-right")
    elif assets.image("avion_venezuela_pixelart"):
        img_avion = assets.image("avion_venezuela_pixelart")
    else:
        # Fallback
        img_avion = assets.image("maduro")
        
    nena = sprites.create(img_avion, SpriteKind.player)
    
    # Posición inicial
    tiles.place_on_tile(nena, tiles.get_tile_location(25, 10))
    
    # --- CONFIGURACIÓN DE VUELO (SIN GRAVEDAD) ---
    nena.ay = 0  # Gravedad CERO
    nena.set_stay_in_screen(True)
    scene.camera_follow_sprite(nena)
    
    # --- ENEMIGO (HELICÓPTERO) ---
    img_heli = None
    if assets.image("helicoptero"):
        img_heli = assets.image("helicoptero")
    else:
        # Fallback si no existe la imagen "helicoptero"
        img_heli = img("""
            . . . . . . . .
            . . . 2 2 2 . .
            . . 2 2 2 2 2 .
            . . . . . . . .
        """)
        
    bot = sprites.create(img_heli, SpriteKind.enemy)
    tiles.place_on_tile(bot, tiles.get_tile_location(5, 10)) # Empieza delante
    bot.ay = 0 # El enemigo también vuela
    bot.set_bounce_on_wall(True)

    # --- META AL FINAL DEL NIVEL ---
    meta_avion = sprites.create(assets.image("barco venezuela"), SpriteKind.Meta)
    tiles.place_on_tile(meta_avion, tiles.get_tile_location(200, 10))
    
    # --- INICIO ---
    juego_empezado = True
    
    # Movimiento en X e Y (vuelo libre)
    controller.move_sprite(nena, 100, 100)
    
    tiempo_inicio = game.runtime()
    nena.say_text("¡A VOLAR!", 1000, True)

# ---------------------------------------------------------
# EVENTOS Y FÍSICAS
# ---------------------------------------------------------

def game_over_personalizado():
    global juego_empezado
    juego_empezado = False
    game.splash("¡HAS MUERTO!", "Volviendo al mapa...")
    selector_de_mapa()

# --- GESTIÓN DE VICTORIAS ---
def on_nivel_completado(sprite, otherSprite):
    global nivel_desbloqueado, tiempo_final
    
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
            
    elif nivel_actual == 3:
        game.splash("¡NIVEL 3 SUPERADO!", "Tiempo: " + str(tiempo_final) + "s")
        game.splash("¡ERES EL LIBERTADOR DEL AIRE!")
    
    selector_de_mapa()

sprites.on_overlap(SpriteKind.player, SpriteKind.Meta, on_nivel_completado)

def on_on_overlap(sprite, otherSprite):
    if nena:
        if nivel_actual != 3: # Solo rebota en niveles con gravedad
            nena.vy = -250
            if nena.vx > 0:
                nena.vx = 250
            else:
                nena.vx = -250
sprites.on_overlap(SpriteKind.player, SpriteKind.Trampolin, on_on_overlap)

def on_right_pressed():
    if nena:
        if nivel_actual == 1:
            animation.run_image_animation(nena, assets.animation("maduro-right0"), 200, True)
        elif nivel_actual == 2:
            if assets.image("maduro-lancha-right"):
                nena.set_image(assets.image("maduro-lancha-right"))
        elif nivel_actual == 3:
            # Cambio de sprite en vuelo
            if assets.image("maduro-avion-right"):
                nena.set_image(assets.image("maduro-avion-right"))
            
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def on_left_pressed():
    if nena:
        if nivel_actual == 1:
            animation.run_image_animation(nena, assets.animation("maduro-left"), 200, True)
        elif nivel_actual == 2:
            if assets.image("maduro-lancha-left"):
                nena.set_image(assets.image("maduro-lancha-left"))
        elif nivel_actual == 3:
            # Cambio de sprite en vuelo
            if assets.image("maduro-avion-left"):
                nena.set_image(assets.image("maduro-avion-left"))
            
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

def on_a_pressed():
    # Salto solo si hay gravedad (Niveles 1 y 2)
    if nivel_actual != 3:
        if nena and nena.is_hitting_tile(CollisionDirection.BOTTOM):
            nena.vy = -155
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

def on_on_overlap2(sprite2, otherSprite2):
    game_over_personalizado()
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap2)

# ==========================================
#   SISTEMA DE LLUVIA DE BOMBAS
# ==========================================

def generar_bomba():
    # Solo caen si el juego ha empezado y NO estamos en el Nivel 3
    if juego_empezado and nivel_actual != 3 and randint(0, 100) < probabilidad_bomba:
        cam_x = scene.camera_property(CameraProperty.X)
        cam_top = scene.camera_property(CameraProperty.Top)
        
        img_bomba = None
        if assets.image("bomba"):
            img_bomba = assets.image("bomba")
        else:
            img_bomba = img("""
                2 2 2 2
                2 2 2 2
                2 2 2 2
                2 2 2 2
            """)
            
        bomba = sprites.create(img_bomba, SpriteKind.Projectile)
        bomba.set_position(randint(cam_x - 100, cam_x + 100), cam_top)
        bomba.vy = 100
        bomba.z = 100
        bomba.set_flag(SpriteFlag.AUTO_DESTROY, True)

game.on_update_interval(1000, generar_bomba)

# ==========================================
#   SISTEMA DE DISPARO DEL HELICÓPTERO (CORREGIDO FINAL)
# ==========================================

def disparar_helicoptero():
    # Dispara solo en nivel 3 y si el bot existe
    if juego_empezado and nivel_actual == 3 and bot:
        
        # Crear imagen de "bala" o "gota"
        img_bala = None
        if assets.image("misil"):
            img_bala = assets.image("misil")
        else:
            img_bala = img("""
                2 2
                2 2
            """)
            
        misil = sprites.create(img_bala, SpriteKind.Projectile)
        
        # --- AJUSTE DE POSICIÓN ---
        # Salida por el "morro" lateral
        offset_x = 0
        if nena.x < bot.x:
            offset_x = -70 # Izquierda
        else:
            offset_x = 70  # Derecha
            
        misil.set_position(bot.x + offset_x, bot.y + 5)
        
        # --- CÁLCULO DE DIRECCIÓN RECTA (LÁSER) ---
        dx = nena.x - misil.x
        dy = nena.y - misil.y
        
        angulo = Math.atan2(dy, dx)
        velocidad_disparo = 200
        
        misil.vx = Math.cos(angulo) * velocidad_disparo
        misil.vy = Math.sin(angulo) * velocidad_disparo
        
        misil.z = 95
        misil.lifespan = 3000

# Dispara cada 500ms (1.5s)
game.on_update_interval(2500, disparar_helicoptero)


def on_player_hit_bomb(player, bomb):
    bomb.destroy(effects.fire, 100)
    game_over_personalizado()

sprites.on_overlap(SpriteKind.player, SpriteKind.Projectile, on_player_hit_bomb)

def on_bomb_hit_wall(bomb2, location):
    global probabilidad_bomba
    bomb2.destroy(effects.disintegrate, 100)
    if probabilidad_bomba > 10:
        probabilidad_bomba -= 10

scene.on_hit_wall(SpriteKind.Projectile, on_bomb_hit_wall)

# --- CHOQUE CON NUBE EN NIVEL 3 ---
def on_nube_tocada(sprite, location):
    if nivel_actual == 3:
        game_over_personalizado()

if assets.tile("nube02"):
    scene.on_overlap_tile(SpriteKind.player, assets.tile("nube02"), on_nube_tocada)

# LÓGICA PRINCIPAL (UPDATE)
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
    
    if not nena:
        return

    # Lógica específica de suelo (Solo Niveles 1 y 2)
    if juego_empezado and nivel_actual != 3:
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

        # Lógica del Bot (Solo si existe)
        if bot:
            distancia3 = abs(nena.x - bot.x)
            
            if nivel_actual == 1:
                if distancia3 > 90:
                    velocidad3 = 320
                elif distancia3 > 30:
                    velocidad3 = 190
                else:
                    velocidad3 = 95
            elif nivel_actual == 2:
                if distancia3 > 120:
                    velocidad3 = 320
                else:
                    velocidad3 = 60
                    
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
                    
    # Lógica específica de vuelo (Nivel 3)
    elif juego_empezado and nivel_actual == 3:
        if bot:
            # === VELOCIDAD DINÁMICA AÉREA ===
            distancia3 = abs(nena.x - bot.x)
            
            if distancia3 > 120:
                velocidad3 = 200
            elif distancia3 > 30:
                velocidad3 = 60
            else:
                velocidad3 = 40
            
            # Perseguir en X
            if nena.x < bot.x:
                bot.vx = -velocidad3
            else:
                bot.vx = velocidad3
                
            # Perseguir en Y
            if nena.y < bot.y:
                bot.vy = -velocidad3
            else:
                bot.vy = velocidad3

            # Rebote en paredes
            if bot.is_hitting_tile(CollisionDirection.LEFT) or bot.is_hitting_tile(CollisionDirection.RIGHT):
                 bot.vx = -bot.vx

game.on_update(on_on_update)

# --- CHIVATO DE COORDENADAS ---
def debug_coordenadas_mapa():
    lista_cursores = sprites.all_of_kind(SpriteKind.Cursor)
    if len(lista_cursores) > 0:
        mi_cursor = lista_cursores[0]
        col = int(mi_cursor.x / 16)
        fila = int(mi_cursor.y / 16)
        mi_cursor.say_text(str(col) + ", " + str(fila))
game.on_update(debug_coordenadas_mapa)

# --- INICIO DEL JUEGO ---
iniciar_nivel_3() # Descomentar para probar directo Nivel 3
#selector_de_mapa()