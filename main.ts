let lugar: tiles.Location;
let nueva_minita: Sprite;
let tipo_actual: Image;
let lista_lugares_toldo: tiles.Location[];
let k: number;
let lugar_t: tiles.Location;
let nuevo_toldo: Sprite;
let numero: number;
namespace SpriteKind {
    export const Obstacle = SpriteKind.create()
    export const Trampolin = SpriteKind.create()
}

tiles.setCurrentTilemap(tilemap`prova`)
let bot_mirando_derecha = false
let velocidad3 = 0
let distancia3 = 0
let nena : Sprite = null
let juego_empezado = false
//  OBJETOS FIJOS
let tanque = sprites.create(assets.image`tanque`, SpriteKind.Obstacle)
tiles.placeOnTile(tanque, tiles.getTileLocation(116, 10))
let tanque02 = sprites.create(assets.image`tanque`, SpriteKind.Obstacle)
tiles.placeOnTile(tanque02, tiles.getTileLocation(146, 10))
//  PERSONAJES
let bot = sprites.create(assets.image`soldado0`, SpriteKind.Enemy)
tiles.placeOnTile(bot, tiles.getTileLocation(1, 7))
bot.ay = 350
nena = sprites.create(assets.image`maduro`, SpriteKind.Player)
tiles.placeOnTile(nena, tiles.getTileLocation(6, 9))
nena.ay = 350
nena.setStayInScreen(true)
scene.cameraFollowSprite(nena)
//  GENERADOR DE MINAS
let lista_minas = tiles.getTilesByType(assets.tile`interrogacion`)
let i = 0
while (i < lista_minas.length) {
    lugar = lista_minas[i]
    nueva_minita = sprites.create(assets.image`minita3`, SpriteKind.Enemy)
    tiles.placeOnTile(nueva_minita, lugar)
    i += 1
}
//  GENERADOR DE TOLDOS
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
//  CUENTA REGRESIVA
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

//  CONTROLES
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
//  LÓGICA IA + SUELOS
let tiles_petroleo = [assets.tile`petroleo0`, assets.tile`petroleo02`, assets.tile`petroleo1`]
let tile_mina = assets.tile`interrogacion`
game.onUpdate(function on_on_update() {
    let loc_actual: tiles.Location;
    let columna: number;
    let fila_abajo: number;
    let ubicacion_suelo: tiles.Location;
    let imagen_suelo: Image;
    let estoy_en_petroleo: boolean;
    
    if (!nena || !bot) {
        return
    }
    
    if (juego_empezado) {
        loc_actual = nena.tilemapLocation()
        columna = loc_actual.column
        fila_abajo = loc_actual.row + 1
        ubicacion_suelo = tiles.getTileLocation(columna, fila_abajo)
        imagen_suelo = tiles.tileImageAtLocation(ubicacion_suelo)
        //  1. MINAS
        if (imagen_suelo == tile_mina) {
            game.over(false)
            return
        }
        
        //  2. PETRÓLEO
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
    
})
//  COLISIONES
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function on_enemy_overlap(sprite2: Sprite, otherSprite2: Sprite) {
    game.over(false)
})
sprites.onOverlap(SpriteKind.Player, SpriteKind.Trampolin, function on_toldo_overlap(sprite: Sprite, otherSprite: Sprite) {
    if (nena) {
        nena.vy = -250
        if (nena.vx > 0) {
            nena.vx = 250
        } else {
            nena.vx = -250
        }
        
    }
    
})
