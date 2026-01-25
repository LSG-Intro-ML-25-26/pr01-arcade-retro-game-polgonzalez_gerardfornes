namespace SpriteKind {
    export const Obstacle = SpriteKind.create()
    export const Trampolin = SpriteKind.create()
    export const IconoNivel = SpriteKind.create()
    export const Cursor = SpriteKind.create()
    export const UI = SpriteKind.create()
    export const Fondo = SpriteKind.create()
    export const Meta = SpriteKind.create()
}

let bot_mirando_derecha = false
let velocidad3 = 0
let distancia3 = 0
let juego_empezado = false
let tiempo_inicio = 0
let probabilidad_bomba = 100
let nivel_desbloqueado = 1
let nivel_actual = 0
let nena : Sprite = null
let bot : Sprite = null
let tanque : Sprite = null
let tanque02 : Sprite = null
let mySpriteBarco : Sprite = null
let mySpriteBarco2 : Sprite = null
let cursor : Sprite = null
let icono1 : Sprite = null
let icono2 : Sprite = null
let icono3 : Sprite = null
let lista_cursores : Sprite[] = []
let l = 0
let t = 0
let partes_toldo : Image[] = []
let i = 0
let lista_minas : tiles.Location[] = []
let tiempo_final = 0
function menu_inicial() {
    let boton_play: Sprite;
    
    juego_empezado = false
    info.showScore(false)
    if (assets.image`
        escapefromusa
        `) {
        scene.setBackgroundImage(assets.image`
            escapefromusa
            `)
    }
    
    if (assets.image`
        bigButtonPressed2
        `) {
        boton_play = sprites.create(assets.image`
                bigButtonPressed2
                `, SpriteKind.UI)
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

function cinematica_lore() {
    if (assets.image`
        mapausa
        `) {
        scene.setBackgroundImage(assets.image`
            mapausa
            `)
    } else {
        scene.setBackgroundColor(15)
    }
    
    game.showLongText("El mundo pensaba que lo había visto todo...", DialogLayout.Bottom)
    if (assets.image`
        trumpworld
        `) {
        scene.setBackgroundImage(assets.image`
            trumpworld
            `)
    }
    
    game.showLongText("En un movimiento que nadie vio venir...", DialogLayout.Bottom)
    if (assets.image`
        maduropurple
        `) {
        scene.setBackgroundImage(assets.image`
            maduropurple
            `)
    }
    
    game.showLongText("Sí... Maduro ha sido secuestrado...", DialogLayout.Bottom)
    if (assets.image`
        madurobros
        `) {
        scene.setBackgroundImage(assets.image`
            madurobros
            `)
    }
    
    game.showLongText("La situación es insostenible...", DialogLayout.Bottom)
    if (assets.image`
        cara feliz
        `) {
        scene.setBackgroundImage(assets.image`
            cara feliz
            `)
    }
    
    game.showLongText("Tu trabajo no es juzgar...", DialogLayout.Bottom)
    game.showLongText("Tu misión es intervenir...", DialogLayout.Bottom)
    game.showLongText("Prepárate para la extracción...", DialogLayout.Bottom)
    if (assets.image`
        pokemon
        `) {
        scene.setBackgroundImage(assets.image`
            pokemon
            `)
        pause(2000)
        game.showLongText("¡EMPIEZA LA MISIÓN!", DialogLayout.Center)
    }
    
    selector_de_mapa()
}

function selector_de_mapa() {
    let mapa_visual: Sprite;
    
    juego_empezado = false
    nena = null
    bot = null
    info.setScore(0)
    info.showScore(false)
    scene.setBackgroundImage(null)
    scene.setBackgroundColor(9)
    pause(100)
    sprites.destroyAllSpritesOfKind(SpriteKind.Player)
    sprites.destroyAllSpritesOfKind(SpriteKind.Enemy)
    sprites.destroyAllSpritesOfKind(SpriteKind.Obstacle)
    sprites.destroyAllSpritesOfKind(SpriteKind.Trampolin)
    sprites.destroyAllSpritesOfKind(SpriteKind.UI)
    sprites.destroyAllSpritesOfKind(SpriteKind.Meta)
    sprites.destroyAllSpritesOfKind(SpriteKind.Fondo)
    sprites.destroyAllSpritesOfKind(SpriteKind.Projectile)
    tiles.setCurrentTilemap(null)
    pause(200)
    if (assets.tile`
        mundo_grande
        `) {
        tiles.setCurrentTilemap(tilemap`
            mundo_grande
            `)
    } else {
        tiles.setCurrentTilemap(tilemap`
            level1
            `)
    }
    
    if (assets.image`
        mapamundi2
        `) {
        mapa_visual = sprites.create(assets.image`
            mapamundi2
            `, SpriteKind.Fondo)
        mapa_visual.z = -100
        mapa_visual.setFlag(SpriteFlag.Ghost, true)
        mapa_visual.setPosition(400, 400)
    }
    
    cursor = sprites.create(assets.image`
        maduro
        `, SpriteKind.Cursor)
    tiles.placeOnTile(cursor, tiles.getTileLocation(10, 26))
    controller.moveSprite(cursor, 150, 150)
    scene.cameraFollowSprite(cursor)
    cursor.setStayInScreen(true)
    if (assets.image`
        venezuela0
        `) {
        icono1 = sprites.create(assets.image`
                venezuela0
                `, SpriteKind.IconoNivel)
        tiles.placeOnTile(icono1, tiles.getTileLocation(12, 26))
        if (nivel_desbloqueado > 1) {
            icono1.sayText("OK", 50000, false)
        } else {
            icono1.sayText("1", 50000, false)
        }
        
    }
    
    if (assets.image`
        barco venezuela
        `) {
        icono2 = sprites.create(assets.image`
                barco venezuela
                `, SpriteKind.IconoNivel)
        tiles.placeOnTile(icono2, tiles.getTileLocation(16, 18))
        if (nivel_desbloqueado >= 2) {
            icono2.sayText("2", 50000, false)
        } else {
            icono2.sayText("X", 50000, false)
        }
        
    }
    
    if (assets.image`
        comunista
        `) {
        icono3 = sprites.create(assets.image`
                comunista
                `, SpriteKind.IconoNivel)
        tiles.placeOnTile(icono3, tiles.getTileLocation(37, 9))
        if (nivel_desbloqueado >= 3) {
            icono3.sayText("3", 50000, false)
        } else {
            icono3.sayText("X", 50000, false)
        }
        
    }
    
    game.splash("Elige un nivel")
}

sprites.onOverlap(SpriteKind.Cursor, SpriteKind.IconoNivel, function on_mapa_overlap(sprite: Sprite, otherSprite: Sprite) {
    if (controller.A.isPressed()) {
        if (otherSprite == icono1) {
            iniciar_nivel_1()
        } else if (otherSprite == icono2) {
            if (nivel_desbloqueado >= 2) {
                game.splash("Nivel 2", "¡Huye del ejército!")
                iniciar_nivel_2()
            } else {
                game.splash("BLOQUEADO", "Completa el Nivel 1 primero")
            }
            
            pause(500)
        } else if (otherSprite == icono3) {
            if (nivel_desbloqueado >= 3) {
                game.splash("Nivel 3", "¡Guerra Aérea!")
                iniciar_nivel_3()
            } else {
                game.splash("BLOQUEADO", "Completa el Nivel 2 primero")
            }
            
            pause(500)
        }
        
    }
    
})
function iniciar_nivel_1() {
    let lugar: tiles.Location;
    let nueva_minita: Sprite;
    let tipo_actual: Image;
    let lista_lugares_toldo: tiles.Location[];
    let k: number;
    let lugar_t: tiles.Location;
    let nuevo_toldo: Sprite;
    let numero: number;
    
    nivel_actual = 1
    probabilidad_bomba = 0
    sprites.destroyAllSpritesOfKind(SpriteKind.Fondo)
    sprites.destroyAllSpritesOfKind(SpriteKind.Cursor)
    sprites.destroyAllSpritesOfKind(SpriteKind.IconoNivel)
    sprites.destroyAllSpritesOfKind(SpriteKind.Projectile)
    scene.setBackgroundImage(null)
    info.showScore(true)
    info.setScore(0)
    tiempo_inicio = game.runtime()
    tiles.setCurrentTilemap(tilemap`
        prova
        `)
    tanque = sprites.create(assets.image`
        tanque
        `, SpriteKind.Obstacle)
    tiles.placeOnTile(tanque, tiles.getTileLocation(116, 10))
    tanque02 = sprites.create(assets.image`
        tanque
        `, SpriteKind.Obstacle)
    tiles.placeOnTile(tanque02, tiles.getTileLocation(146, 10))
    mySpriteBarco = sprites.create(assets.image`
            barco venezuela
            `, SpriteKind.Meta)
    tiles.placeOnTile(mySpriteBarco, tiles.getTileLocation(245, 10))
    bot = sprites.create(assets.image`
        soldado0
        `, SpriteKind.Enemy)
    tiles.placeOnTile(bot, tiles.getTileLocation(1, 7))
    bot.ay = 350
    nena = sprites.create(assets.image`
        maduro
        `, SpriteKind.Player)
    tiles.placeOnTile(nena, tiles.getTileLocation(6, 9))
    nena.ay = 350
    nena.setStayInScreen(true)
    scene.cameraFollowSprite(nena)
    let lista_minas2 = tiles.getTilesByType(assets.tile`
        interrogacion
        `)
    i = 0
    while (i < lista_minas2.length) {
        lugar = lista_minas2[i]
        nueva_minita = sprites.create(assets.image`
            minita3
            `, SpriteKind.Enemy)
        tiles.placeOnTile(nueva_minita, lugar)
        i += 1
    }
    let partes_toldo2 = [assets.tile`
            toldo01
            `, assets.tile`
            toldo02
            `, assets.tile`
            toldo03
            `, assets.tile`
            toldo04
            `]
    t = 0
    while (t < partes_toldo2.length) {
        tipo_actual = partes_toldo2[t]
        lista_lugares_toldo = tiles.getTilesByType(tipo_actual)
        k = 0
        while (k < lista_lugares_toldo.length) {
            lugar_t = lista_lugares_toldo[k]
            nuevo_toldo = sprites.create(tipo_actual, SpriteKind.Trampolin)
            tiles.placeOnTile(nuevo_toldo, lugar_t)
            tiles.setTileAt(lugar_t, assets.tile`
                transparency16
                `)
            k += 1
        }
        t += 1
    }
    controller.moveSprite(nena, 0, 0)
    k = 0
    while (k < 3) {
        numero = 3 - k
        if (nena) {
            nena.sayText("" + ("" + numero), 1000, true)
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
        animation.runImageAnimation(nena, assets.animation`
                maduro-right0
                `, 200, true)
    } else if (controller.left.isPressed()) {
        animation.runImageAnimation(nena, assets.animation`
                maduro-left
                `, 200, true)
    }
    
}

function iniciar_nivel_2() {
    let numero_cuenta: number;
    
    nivel_actual = 2
    probabilidad_bomba = 100
    sprites.destroyAllSpritesOfKind(SpriteKind.Fondo)
    sprites.destroyAllSpritesOfKind(SpriteKind.Cursor)
    sprites.destroyAllSpritesOfKind(SpriteKind.IconoNivel)
    sprites.destroyAllSpritesOfKind(SpriteKind.Projectile)
    scene.setBackgroundImage(null)
    info.showScore(true)
    info.setScore(0)
    tiles.setCurrentTilemap(tilemap`
        nivel02
        `)
    let img_ola = null
    if (assets.image`
        ola
        `) {
        img_ola = assets.image`
            ola
            `
    } else {
        img_ola = img`
            8 8 8 8 8 8 8 8
            8 8 8 8 8 8 8 8
            8 8 8 8 8 8 8 8
            8 8 8 8 8 8 8 8
            `
    }
    
    let ola1 = sprites.create(img_ola, SpriteKind.Fondo)
    tiles.placeOnTile(ola1, tiles.getTileLocation(50, 12))
    ola1.z = 1
    ola1.ay = 0
    ola1.setFlag(SpriteFlag.Ghost, true)
    let ola2 = sprites.create(img_ola, SpriteKind.Fondo)
    tiles.placeOnTile(ola2, tiles.getTileLocation(130, 13))
    ola2.z = 1
    ola2.ay = 0
    ola2.setFlag(SpriteFlag.Ghost, true)
    let ola3 = sprites.create(img_ola, SpriteKind.Fondo)
    tiles.placeOnTile(ola3, tiles.getTileLocation(200, 12))
    ola3.z = 1
    ola3.ay = 0
    ola3.setFlag(SpriteFlag.Ghost, true)
    if (assets.image`
        maduro-lancha-right
        `) {
        nena = sprites.create(assets.image`
                maduro-lancha-right
                `, SpriteKind.Player)
    } else {
        nena = sprites.create(assets.image`
            maduro
            `, SpriteKind.Player)
    }
    
    nena.z = 2
    tiles.placeOnTile(nena, tiles.getTileLocation(11, 10))
    nena.ay = 350
    nena.setStayInScreen(true)
    scene.cameraFollowSprite(nena)
    bot = sprites.create(assets.image`
        usarmy
        `, SpriteKind.Enemy)
    tiles.placeOnTile(bot, tiles.getTileLocation(4, 9))
    bot.ay = 350
    bot.setBounceOnWall(true)
    mySpriteBarco2 = sprites.create(assets.image`
            barco venezuela
            `, SpriteKind.Meta)
    tiles.placeOnTile(mySpriteBarco2, tiles.getTileLocation(240, 10))
    controller.moveSprite(nena, 0, 0)
    l = 0
    while (l < 3) {
        numero_cuenta = 3 - l
        if (nena) {
            nena.sayText("" + ("" + numero_cuenta), 1000, true)
        }
        
        pause(1000)
        l += 1
    }
    if (nena) {
        nena.sayText("¡YA!", 500, true)
    }
    
    juego_empezado = true
    controller.moveSprite(nena, 100, 0)
    tiempo_inicio = game.runtime()
}

function iniciar_nivel_3() {
    
    nivel_actual = 3
    sprites.destroyAllSpritesOfKind(SpriteKind.Fondo)
    sprites.destroyAllSpritesOfKind(SpriteKind.Cursor)
    sprites.destroyAllSpritesOfKind(SpriteKind.IconoNivel)
    sprites.destroyAllSpritesOfKind(SpriteKind.Projectile)
    sprites.destroyAllSpritesOfKind(SpriteKind.Enemy)
    sprites.destroyAllSpritesOfKind(SpriteKind.Meta)
    scene.setBackgroundImage(null)
    scene.setBackgroundColor(9)
    info.showScore(true)
    info.setScore(0)
    tiles.setCurrentTilemap(tilemap`
        nivel03
        `)
    let img_avion = null
    if (assets.image`
        maduro-avion-right
        `) {
        img_avion = assets.image`
            maduro-avion-right
            `
    } else if (assets.image`
        avion_venezuela_pixelart
        `) {
        img_avion = assets.image`
            avion_venezuela_pixelart
            `
    } else {
        img_avion = assets.image`
            maduro
            `
    }
    
    nena = sprites.create(img_avion, SpriteKind.Player)
    tiles.placeOnTile(nena, tiles.getTileLocation(25, 10))
    nena.ay = 0
    nena.setStayInScreen(true)
    scene.cameraFollowSprite(nena)
    let img_heli = null
    if (assets.image`
        helicoptero
        `) {
        img_heli = assets.image`
            helicoptero
            `
    } else {
        img_heli = img`
            . . . . . . . .
            . . . 2 2 2 . .
            . . 2 2 2 2 2 .
            . . . . . . . .
            `
    }
    
    bot = sprites.create(img_heli, SpriteKind.Enemy)
    tiles.placeOnTile(bot, tiles.getTileLocation(5, 10))
    bot.ay = 0
    bot.setBounceOnWall(true)
    let meta_avion = sprites.create(assets.image`
            helicopteroruso
            `, SpriteKind.Meta)
    tiles.placeOnTile(meta_avion, tiles.getTileLocation(200, 10))
    juego_empezado = true
    controller.moveSprite(nena, 100, 100)
    tiempo_inicio = game.runtime()
    nena.sayText("¡A VOLAR!", 1000, true)
}

function game_over_personalizado() {
    
    juego_empezado = false
    game.splash("¡HAS MUERTO!", "Volviendo al mapa...")
    selector_de_mapa()
}

function cinematica_final() {
    
    juego_empezado = false
    info.showScore(false)
    sprites.destroyAllSpritesOfKind(SpriteKind.Player)
    sprites.destroyAllSpritesOfKind(SpriteKind.Enemy)
    sprites.destroyAllSpritesOfKind(SpriteKind.Projectile)
    sprites.destroyAllSpritesOfKind(SpriteKind.Meta)
    scene.cameraFollowSprite(null)
    scene.centerCameraAt(80, 60)
    tiles.setCurrentTilemap(null)
    if (assets.image`
        madrerusia
        `) {
        scene.setBackgroundImage(assets.image`
            madrerusia
            `)
    } else {
        scene.setBackgroundColor(2)
    }
    
    pause(500)
    game.showLongText("¡HEMOS GANADO!", DialogLayout.Center)
    game.showLongText("Hemos llegado sanos y salvos a la Madre Rusia.", DialogLayout.Bottom)
    game.splash("Volver al Menú")
    menu_inicial()
}

sprites.onOverlap(SpriteKind.Player, SpriteKind.Meta, function on_nivel_completado(sprite2: Sprite, otherSprite2: Sprite) {
    
    tiempo_final = info.score()
    if (nivel_actual == 1) {
        game.splash("¡NIVEL 1 SUPERADO!", "Tiempo: " + ("" + ("" + tiempo_final)) + "s")
        if (nivel_desbloqueado < 2) {
            nivel_desbloqueado = 2
            game.splash("¡NIVEL 2 DESBLOQUEADO!")
        }
        
        selector_de_mapa()
    } else if (nivel_actual == 2) {
        game.splash("¡NIVEL 2 SUPERADO!", "Tiempo: " + ("" + ("" + tiempo_final)) + "s")
        if (nivel_desbloqueado < 3) {
            nivel_desbloqueado = 3
            game.splash("¡NIVEL 3 DESBLOQUEADO!")
        }
        
        selector_de_mapa()
    } else if (nivel_actual == 3) {
        cinematica_final()
    }
    
})
sprites.onOverlap(SpriteKind.Player, SpriteKind.Trampolin, function on_on_overlap(sprite3: Sprite, otherSprite3: Sprite) {
    if (nena) {
        if (nivel_actual != 3) {
            nena.vy = -250
            if (nena.vx > 0) {
                nena.vx = 250
            } else {
                nena.vx = -250
            }
            
        }
        
    }
    
})
controller.right.onEvent(ControllerButtonEvent.Pressed, function on_right_pressed() {
    if (nena) {
        if (nivel_actual == 1) {
            animation.runImageAnimation(nena, assets.animation`
                    maduro-right0
                    `, 200, true)
        } else if (nivel_actual == 2) {
            if (assets.image`
                maduro-lancha-right
                `) {
                nena.setImage(assets.image`
                    maduro-lancha-right
                    `)
            }
            
        } else if (nivel_actual == 3) {
            if (assets.image`
                maduro-avion-right
                `) {
                nena.setImage(assets.image`
                    maduro-avion-right
                    `)
            }
            
        }
        
    }
    
})
controller.left.onEvent(ControllerButtonEvent.Pressed, function on_left_pressed() {
    if (nena) {
        if (nivel_actual == 1) {
            animation.runImageAnimation(nena, assets.animation`
                    maduro-left
                    `, 200, true)
        } else if (nivel_actual == 2) {
            if (assets.image`
                maduro-lancha-left
                `) {
                nena.setImage(assets.image`
                    maduro-lancha-left
                    `)
            }
            
        } else if (nivel_actual == 3) {
            if (assets.image`
                maduro-avion-left
                `) {
                nena.setImage(assets.image`
                    maduro-avion-left
                    `)
            }
            
        }
        
    }
    
})
function on_a_pressed() {
    if (nivel_actual != 3) {
        if (nena && nena.isHittingTile(CollisionDirection.Bottom)) {
            nena.vy = -155
        }
        
    }
    
}

controller.A.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
controller.up.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function on_on_overlap2(sprite22: Sprite, otherSprite22: Sprite) {
    game_over_personalizado()
})
game.onUpdateInterval(1000, function generar_bomba() {
    let cam_x: number;
    let cam_top: number;
    let img_bomba: Image;
    let bomba: Sprite;
    if (juego_empezado && nivel_actual == 2 && randint(0, 100) < probabilidad_bomba) {
        cam_x = scene.cameraProperty(CameraProperty.X)
        cam_top = scene.cameraProperty(CameraProperty.Top)
        img_bomba = null
        if (assets.image`
            bomba
            `) {
            img_bomba = assets.image`
                bomba
                `
        } else {
            img_bomba = img`
                2 2 2 2
                2 2 2 2
                2 2 2 2
                2 2 2 2
                `
        }
        
        bomba = sprites.create(img_bomba, SpriteKind.Projectile)
        bomba.setPosition(randint(cam_x - 100, cam_x + 100), cam_top)
        bomba.vy = 100
        bomba.z = 100
        bomba.setFlag(SpriteFlag.AutoDestroy, true)
    }
    
})
game.onUpdateInterval(2500, function disparar_helicoptero() {
    let img_bala: Image;
    let misil: Sprite;
    let offset_x: number;
    let dx: number;
    let dy: number;
    let angulo: number;
    let velocidad_disparo: number;
    if (juego_empezado && nivel_actual == 3 && bot) {
        img_bala = null
        if (assets.image`
            misil
            `) {
            img_bala = assets.image`
                misil
                `
        } else {
            img_bala = img`
                2 2
                2 2
                `
        }
        
        misil = sprites.create(img_bala, SpriteKind.Projectile)
        offset_x = 0
        if (nena.x < bot.x) {
            offset_x = -70
        } else {
            offset_x = 70
        }
        
        misil.setPosition(bot.x + offset_x, bot.y + 5)
        dx = nena.x - misil.x
        dy = nena.y - misil.y
        angulo = Math.atan2(dy, dx)
        velocidad_disparo = 200
        misil.vx = Math.cos(angulo) * velocidad_disparo
        misil.vy = Math.sin(angulo) * velocidad_disparo
        misil.z = 95
        misil.lifespan = 3000
    }
    
})
sprites.onOverlap(SpriteKind.Player, SpriteKind.Projectile, function on_player_hit_bomb(player: Sprite, bomb: Sprite) {
    bomb.destroy(effects.fire, 100)
    game_over_personalizado()
})
scene.onHitWall(SpriteKind.Projectile, function on_bomb_hit_wall(bomb2: Sprite, location: tiles.Location) {
    
    bomb2.destroy(effects.disintegrate, 100)
    if (probabilidad_bomba > 10) {
        probabilidad_bomba -= 10
    }
    
})
if (assets.tile`
    nube02
    `) {
    scene.onOverlapTile(SpriteKind.Player, assets.tile`
            nube02
            `, function on_nube_tocada(sprite4: Sprite, location2: tiles.Location) {
        if (nivel_actual == 3) {
            game_over_personalizado()
        }
        
    })
}

let tiles_petroleo = [assets.tile`
        petroleo0
        `, assets.tile`
        petroleo02
        `, assets.tile`
        petroleo1
        `]
let tile_mina = assets.tile`
    interrogacion
    `
game.onUpdate(function on_on_update() {
    let tiempo_actual: number;
    let segundos: number;
    let loc_actual: tiles.Location;
    let columna: number;
    let fila_abajo: number;
    let ubicacion_suelo: tiles.Location;
    let imagen_suelo: Image;
    let estoy_en_petroleo: boolean;
    
    if (juego_empezado) {
        tiempo_actual = game.runtime()
        segundos = Math.trunc((tiempo_actual - tiempo_inicio) / 1000)
        info.setScore(segundos)
    }
    
    if (!nena) {
        return
    }
    
    if (juego_empezado && nivel_actual != 3) {
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
        
        if (bot) {
            distancia3 = Math.abs(nena.x - bot.x)
            if (nivel_actual == 1) {
                if (distancia3 > 90) {
                    velocidad3 = 320
                } else if (distancia3 > 30) {
                    velocidad3 = 190
                } else {
                    velocidad3 = 95
                }
                
            } else if (nivel_actual == 2) {
                if (distancia3 > 120) {
                    velocidad3 = 320
                } else {
                    velocidad3 = 60
                }
                
            }
            
            if (nena.x < bot.x) {
                bot.vx = 0 - velocidad3
                if (nivel_actual == 1) {
                    if (bot_mirando_derecha == true) {
                        animation.runImageAnimation(bot, assets.animation`
                                soldado-left0
                                `, 500, true)
                        bot_mirando_derecha = false
                    }
                    
                }
                
            } else {
                bot.vx = velocidad3
                if (nivel_actual == 1) {
                    if (bot_mirando_derecha == false) {
                        animation.runImageAnimation(bot, assets.animation`
                                soldado-right0
                                `, 200, true)
                        bot_mirando_derecha = true
                    }
                    
                }
                
            }
            
            if (bot.isHittingTile(CollisionDirection.Left) || bot.isHittingTile(CollisionDirection.Right)) {
                if (bot.isHittingTile(CollisionDirection.Bottom)) {
                    bot.vy = -155
                }
                
            }
            
        }
        
    } else if (juego_empezado && nivel_actual == 3) {
        if (bot) {
            distancia3 = Math.abs(nena.x - bot.x)
            if (distancia3 > 120) {
                velocidad3 = 200
            } else if (distancia3 > 30) {
                velocidad3 = 60
            } else {
                velocidad3 = 40
            }
            
            if (nena.x < bot.x) {
                bot.vx = -velocidad3
            } else {
                bot.vx = velocidad3
            }
            
            if (nena.y < bot.y) {
                bot.vy = -velocidad3
            } else {
                bot.vy = velocidad3
            }
            
            if (bot.isHittingTile(CollisionDirection.Left) || bot.isHittingTile(CollisionDirection.Right)) {
                bot.vx = -bot.vx
            }
            
        }
        
    }
    
})
game.onUpdate(function debug_coordenadas_mapa() {
    let mi_cursor: Sprite;
    let col: any;
    let fila: any;
    let lista_cursores2 = sprites.allOfKind(SpriteKind.Cursor)
    if (lista_cursores2.length > 0) {
        mi_cursor = lista_cursores2[0]
        col = Math.trunc(mi_cursor.x / 16)
        fila = Math.trunc(mi_cursor.y / 16)
        mi_cursor.sayText("" + ("" + col) + ", " + ("" + ("" + fila)))
    }
    
})
// menu_inicial()
iniciar_nivel_3()
