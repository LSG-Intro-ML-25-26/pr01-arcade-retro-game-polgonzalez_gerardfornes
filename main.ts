namespace SpriteKind {
    export const Obstacle = SpriteKind.create()
    export const Trampolin = SpriteKind.create()
    export const IconoNivel = SpriteKind.create()
    export const Cursor = SpriteKind.create()
    export const UI = SpriteKind.create()
    export const Fondo = SpriteKind.create()
}

//  --- 1. VARIABLES GLOBALES ---
let bot_mirando_derecha = false
let velocidad3 = 0
let distancia3 = 0
let juego_empezado = false
let tiempo_inicio = 0
//  Variable para guardar cuándo empezamos
//  Personajes y objetos
let nena : Sprite = null
let bot : Sprite = null
let tanque : Sprite = null
let tanque02 : Sprite = null
//  Variables para los iconos
let icono1 : Sprite = null
let icono2 : Sprite = null
let icono3 : Sprite = null
//  ---------------------------------------------------------
//  FASE 1: MENÚ INICIAL
//  ---------------------------------------------------------
function menu_inicial() {
    let boton_play: Sprite;
    if (assets.image`escape-to-usa2`) {
        scene.setBackgroundImage(assets.image`escape-to-usa2`)
    }
    
    if (assets.image`bigButtonPressed2`) {
        boton_play = sprites.create(assets.image`bigButtonPressed2`, SpriteKind.UI)
        boton_play.setPosition(80, 110)
        pause(500)
        while (!controller.A.isPressed()) {
            if (game.runtime() % 800 < 400) {
                boton_play.sayText("PLAY", 500, false)
            } else {
                boton_play.sayText("")
            }
            
            pause(20)
        }
        boton_play.destroy()
    } else {
        while (!controller.A.isPressed()) {
            pause(100)
        }
    }
    
    cinematica_lore()
}

//  ---------------------------------------------------------
//  FASE 2: CINEMÁTICA
//  ---------------------------------------------------------
function cinematica_lore() {
    //  IMAGEN 1
    if (assets.image`mapausa`) {
        scene.setBackgroundImage(assets.image`mapausa`)
    } else {
        scene.setBackgroundColor(15)
    }
    
    game.showLongText("El mundo pensaba que lo había visto todo, hasta que el 'Caudillo de Wall Street' decidió que la diplomacia era demasiado lenta y aburrida.", DialogLayout.Bottom)
    //  IMAGEN 2
    if (assets.image`trumpworld`) {
        scene.setBackgroundImage(assets.image`trumpworld`)
    }
    
    game.showLongText("En un movimiento que nadie vio venir —principalmente porque no tiene sentido legal—, el rubio más famoso de Florida ha 'adquirido' un activo internacional de gran tamaño.", DialogLayout.Bottom)
    //  IMAGEN 3
    if (assets.image`maduropurple`) {
        scene.setBackgroundImage(assets.image`maduropurple`)
    }
    
    game.showLongText("Sí... Maduro ha sido secuestrado. Narcolás Maduro AKA 'El Exiliado del Caribe', ahora es propiedad privada.", DialogLayout.Bottom)
    //  IMAGEN 4
    if (assets.image`madurobros`) {
        scene.setBackgroundImage(assets.image`madurobros`)
    }
    
    game.showLongText("La situación es insostenible. El Servicio Secreto está confundido, el SEBIN está en pánico y Twitter... bueno, X... como quieran llamarle, sigue igual de tóxico que siempre.", DialogLayout.Bottom)
    //  IMAGEN 5
    if (assets.image`cara feliz`) {
        scene.setBackgroundImage(assets.image`cara feliz`)
    }
    
    game.showLongText("Tu trabajo no es juzgar la legalidad de esta locura, ni velar por los intereses de ningún país en concreto.", DialogLayout.Bottom)
    game.showLongText("Tu misión es intervenir antes de que 'Tu Patito Favorito' A.K.A YFD (Your Favorite Duck) aplique su política de America First convirtiendo a Maduro en el primer souvenir humano de su nueva franquicia.", DialogLayout.Bottom)
    game.showLongText("Prepárate para la extracción más políticamente incorrecta de la historia. Inserte moneda para evitar la Tercera Guerra Mundial.", DialogLayout.Bottom)
    //  IMAGEN 6
    if (assets.image`pokemon`) {
        scene.setBackgroundImage(assets.image`pokemon`)
        pause(2000)
        game.showLongText("¡EMPIEZA LA MISIÓN!", DialogLayout.Center)
    }
    
    selector_de_mapa()
}

//  ---------------------------------------------------------
//  FASE 3: SELECTOR DE MAPA
//  ---------------------------------------------------------
function selector_de_mapa() {
    let mapa_visual: Sprite;
    
    juego_empezado = false
    nena = null
    bot = null
    //  Ocultamos la puntuación (que usamos como cronómetro) al volver al mapa
    info.setScore(0)
    info.showScore(false)
    scene.setBackgroundImage(null)
    scene.setBackgroundColor(9)
    sprites.destroyAllSpritesOfKind(SpriteKind.Player)
    sprites.destroyAllSpritesOfKind(SpriteKind.Enemy)
    sprites.destroyAllSpritesOfKind(SpriteKind.Obstacle)
    sprites.destroyAllSpritesOfKind(SpriteKind.Trampolin)
    sprites.destroyAllSpritesOfKind(SpriteKind.UI)
    pause(500)
    //  1. TILEMAP
    if (assets.tile`mundo_grande`) {
        tiles.setCurrentTilemap(tilemap`mundo_grande`)
    } else {
        tiles.setCurrentTilemap(tilemap`level1`)
    }
    
    //  2. FONDO GIGANTE
    if (assets.image`mapamundi2`) {
        mapa_visual = sprites.create(assets.image`mapamundi2`, SpriteKind.Fondo)
        mapa_visual.z = -100
        mapa_visual.setFlag(SpriteFlag.Ghost, true)
        mapa_visual.setPosition(400, 400)
    }
    
    //  3. CURSOR
    let cursor = sprites.create(assets.image`maduro`, SpriteKind.Cursor)
    tiles.placeOnTile(cursor, tiles.getTileLocation(10, 26))
    controller.moveSprite(cursor, 150, 150)
    scene.cameraFollowSprite(cursor)
    cursor.setStayInScreen(true)
    //  --- PUNTOS DE NIVEL ---
    if (assets.image`venezuela0`) {
        icono1 = sprites.create(assets.image`venezuela0`, SpriteKind.IconoNivel)
        tiles.placeOnTile(icono1, tiles.getTileLocation(12, 26))
        icono1.sayText("1", 50000, false)
    }
    
    if (assets.image`barco venezuela`) {
        icono2 = sprites.create(assets.image`barco venezuela`, SpriteKind.IconoNivel)
        tiles.placeOnTile(icono2, tiles.getTileLocation(16, 18))
        icono2.sayText("2", 50000, false)
    }
    
    if (assets.image`comunista`) {
        icono3 = sprites.create(assets.image`comunista`, SpriteKind.IconoNivel)
        tiles.placeOnTile(icono3, tiles.getTileLocation(37, 9))
        icono3.sayText("3", 50000, false)
    }
    
    game.splash("Elige un nivel")
}

//  --- LÓGICA DE CHOQUE ---
sprites.onOverlap(SpriteKind.Cursor, SpriteKind.IconoNivel, function on_mapa_overlap(sprite: Sprite, otherSprite: Sprite) {
    if (controller.A.isPressed()) {
        if (otherSprite == icono1) {
            iniciar_nivel_1()
        } else if (otherSprite == icono2) {
            game.splash("Nivel 2", "¡Próximamente!")
            pause(500)
        } else if (otherSprite == icono3) {
            game.splash("Nivel 3", "¡En construcción!")
            pause(500)
        }
        
    }
    
})
//  ---------------------------------------------------------
//  FASE 4: EL JUEGO REAL (NIVEL 1)
//  ---------------------------------------------------------
function iniciar_nivel_1() {
    let lugar: tiles.Location;
    let nueva_minita: Sprite;
    let tipo_actual: Image;
    let lista_lugares_toldo: tiles.Location[];
    let k: number;
    let lugar_t: tiles.Location;
    let nuevo_toldo: Sprite;
    let numero: number;
    
    sprites.destroyAllSpritesOfKind(SpriteKind.Fondo)
    sprites.destroyAllSpritesOfKind(SpriteKind.Cursor)
    sprites.destroyAllSpritesOfKind(SpriteKind.IconoNivel)
    scene.setBackgroundImage(null)
    //  --- CRONÓMETRO (Setup) ---
    //  Mostramos la puntuación, pero la usaremos para mostrar SEGUNDOS
    info.showScore(true)
    info.setScore(0)
    //  Guardamos el tiempo actual (en milisegundos)
    tiempo_inicio = game.runtime()
    tiles.setCurrentTilemap(tilemap`prova`)
    tanque = sprites.create(assets.image`tanque`, SpriteKind.Obstacle)
    tiles.placeOnTile(tanque, tiles.getTileLocation(116, 10))
    tanque02 = sprites.create(assets.image`tanque`, SpriteKind.Obstacle)
    tiles.placeOnTile(tanque02, tiles.getTileLocation(146, 10))
    let mySpriteBarco = sprites.create(assets.image`barco venezuela`, SpriteKind.Player)
    tiles.placeOnTile(mySpriteBarco, tiles.getTileLocation(245, 10))
    bot = sprites.create(assets.image`soldado0`, SpriteKind.Enemy)
    tiles.placeOnTile(bot, tiles.getTileLocation(1, 7))
    bot.ay = 350
    nena = sprites.create(assets.image`maduro`, SpriteKind.Player)
    tiles.placeOnTile(nena, tiles.getTileLocation(6, 9))
    nena.ay = 350
    nena.setStayInScreen(true)
    scene.cameraFollowSprite(nena)
    let lista_minas = tiles.getTilesByType(assets.tile`interrogacion`)
    let i = 0
    while (i < lista_minas.length) {
        lugar = lista_minas[i]
        nueva_minita = sprites.create(assets.image`minita3`, SpriteKind.Enemy)
        tiles.placeOnTile(nueva_minita, lugar)
        i += 1
    }
    let partes_toldo = [assets.tile`toldo01`, assets.tile`toldo02`, assets.tile`toldo03`, assets.tile`toldo04`]
    let t = 0
    while (t < partes_toldo.length) {
        tipo_actual = partes_toldo[t]
        lista_lugares_toldo = tiles.getTilesByType(tipo_actual)
        k = 0
        while (k < lista_lugares_toldo.length) {
            lugar_t = lista_lugares_toldo[k]
            nuevo_toldo = sprites.create(tipo_actual, SpriteKind.Trampolin)
            tiles.placeOnTile(nuevo_toldo, lugar_t)
            tiles.setTileAt(lugar_t, assets.tile`transparency16`)
            k += 1
        }
        t += 1
    }
    controller.moveSprite(nena, 0, 0)
    k = 0
    while (k < 3) {
        numero = 3 - k
        if (nena) {
            nena.sayText("" + numero, 1000, true)
        }
        
        pause(1000)
        k += 1
    }
    if (nena) {
        nena.sayText("¡CORRE!", 500, true)
    }
    
    juego_empezado = true
    controller.moveSprite(nena, 100, 0)
    if (controller.right.isPressed()) {
        animation.runImageAnimation(nena, assets.animation`maduro-right0`, 200, true)
    } else if (controller.left.isPressed()) {
        animation.runImageAnimation(nena, assets.animation`maduro-left`, 200, true)
    }
    
}

//  ---------------------------------------------------------
//  EVENTOS Y FÍSICAS
//  ---------------------------------------------------------
function game_over_personalizado() {
    
    juego_empezado = false
    game.splash("¡HAS MUERTO!", "Volviendo al mapa...")
    selector_de_mapa()
}

sprites.onOverlap(SpriteKind.Player, SpriteKind.Trampolin, function on_on_overlap(sprite: Sprite, otherSprite: Sprite) {
    if (nena) {
        nena.vy = -250
        if (nena.vx > 0) {
            nena.vx = 250
        } else {
            nena.vx = -250
        }
        
    }
    
})
controller.right.onEvent(ControllerButtonEvent.Pressed, function on_right_pressed() {
    if (nena) {
        animation.runImageAnimation(nena, assets.animation`maduro-right0`, 200, true)
    }
    
})
controller.left.onEvent(ControllerButtonEvent.Pressed, function on_left_pressed() {
    if (nena) {
        animation.runImageAnimation(nena, assets.animation`maduro-left`, 200, true)
    }
    
})
function on_a_pressed() {
    if (nena && nena.isHittingTile(CollisionDirection.Bottom)) {
        nena.vy = -155
    }
    
}

controller.A.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
controller.up.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function on_on_overlap2(sprite2: Sprite, otherSprite2: Sprite) {
    game_over_personalizado()
})
//  LÓGICA PRINCIPAL (UPDATE)
let tiles_petroleo = [assets.tile`petroleo0`, assets.tile`petroleo02`, assets.tile`petroleo1`]
let tile_mina = assets.tile`interrogacion`
game.onUpdate(function on_on_update() {
    let tiempo_actual: number;
    let segundos: number;
    let loc_actual: tiles.Location;
    let columna: number;
    let fila_abajo: number;
    let ubicacion_suelo: tiles.Location;
    let imagen_suelo: Image;
    let estoy_en_petroleo: boolean;
    
    //  --- LÓGICA DEL CRONÓMETRO ---
    //  Si estamos jugando, actualizamos el "Score" con los segundos pasados
    if (juego_empezado) {
        tiempo_actual = game.runtime()
        //  Calculamos segundos: (Tiempo actual - Tiempo inicio) / 1000
        segundos = Math.trunc((tiempo_actual - tiempo_inicio) / 1000)
        info.setScore(segundos)
    }
    
    if (!nena || !bot) {
        return
    }
    
    if (juego_empezado) {
        loc_actual = nena.tilemapLocation()
        columna = loc_actual.column
        fila_abajo = loc_actual.row + 1
        ubicacion_suelo = tiles.getTileLocation(columna, fila_abajo)
        imagen_suelo = tiles.tileImageAtLocation(ubicacion_suelo)
        if (imagen_suelo == tile_mina) {
            game_over_personalizado()
            return
        }
        
        estoy_en_petroleo = false
        for (let aceite of tiles_petroleo) {
            if (imagen_suelo == aceite) {
                estoy_en_petroleo = true
                break
            }
            
        }
        if (nena.isHittingTile(CollisionDirection.Bottom)) {
            if (estoy_en_petroleo) {
                controller.moveSprite(nena, 20, 0)
            } else {
                controller.moveSprite(nena, 100, 0)
            }
            
        }
        
        //  IA DEL BOT
        distancia3 = Math.abs(nena.x - bot.x)
        if (distancia3 > 90) {
            velocidad3 = 320
        } else if (distancia3 > 30) {
            velocidad3 = 190
        } else {
            velocidad3 = 95
        }
        
        if (nena.x < bot.x) {
            bot.vx = 0 - velocidad3
            if (bot_mirando_derecha == true) {
                animation.runImageAnimation(bot, assets.animation`soldado-left0`, 500, true)
                bot_mirando_derecha = false
            }
            
        } else {
            bot.vx = velocidad3
            if (bot_mirando_derecha == false) {
                animation.runImageAnimation(bot, assets.animation`soldado-right0`, 200, true)
                bot_mirando_derecha = true
            }
            
        }
        
        if (bot.isHittingTile(CollisionDirection.Left) || bot.isHittingTile(CollisionDirection.Right)) {
            if (bot.isHittingTile(CollisionDirection.Bottom)) {
                bot.vy = -155
            }
            
        }
        
    }
    
})
//  --- CHIVATO DE COORDENADAS ---
game.onUpdate(function debug_coordenadas_mapa() {
    let mi_cursor: Sprite;
    let col: any;
    let fila: any;
    let lista_cursores = sprites.allOfKind(SpriteKind.Cursor)
    if (lista_cursores.length > 0) {
        mi_cursor = lista_cursores[0]
        col = Math.trunc(mi_cursor.x / 16)
        fila = Math.trunc(mi_cursor.y / 16)
        mi_cursor.sayText("" + col + ", " + ("" + fila))
    }
    
})
//  --- INICIO DEL JUEGO ---
menu_inicial()
