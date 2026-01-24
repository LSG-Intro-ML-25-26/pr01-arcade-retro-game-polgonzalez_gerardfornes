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
//  Variables Globales
let bot_mirando_derecha = false
let velocidad3 = 0
let distancia3 = 0
let nena : Sprite = null
//  Tanques
let tanque = sprites.create(assets.image`tanque`, SpriteKind.Obstacle)
tiles.placeOnTile(tanque, tiles.getTileLocation(116, 10))
let tanque02 = sprites.create(assets.image`tanque`, SpriteKind.Obstacle)
tiles.placeOnTile(tanque02, tiles.getTileLocation(146, 10))
//  Bot
let bot = sprites.create(assets.image`soldado0`, SpriteKind.Enemy)
tiles.placeOnTile(bot, tiles.getTileLocation(1, 7))
bot.ay = 350
//  Maduro
nena = sprites.create(assets.image`maduro`, SpriteKind.Player)
tiles.placeOnTile(nena, tiles.getTileLocation(6, 9))
nena.ay = 350
nena.setStayInScreen(true)
scene.cameraFollowSprite(nena)
//  Minas
let lista_minas = tiles.getTilesByType(assets.tile`interrogacion`)
for (let i = 0; i < lista_minas.length; i++) {
    lugar = lista_minas[i]
    nueva_minita = sprites.create(assets.image`minita3`, SpriteKind.Enemy)
    tiles.placeOnTile(nueva_minita, lugar)
    tiles.setTileAt(lugar, assets.tile`transparency16`)
}
// Salto Toldos
let partes_toldo = [assets.tile`toldo01`, assets.tile`toldo02`, assets.tile`toldo03`, assets.tile`toldo04`]
for (let t = 0; t < partes_toldo.length; t++) {
    tipo_actual = partes_toldo[t]
    lista_lugares_toldo = tiles.getTilesByType(tipo_actual)
    for (k = 0; k < lista_lugares_toldo.length; k++) {
        lugar_t = lista_lugares_toldo[k]
        nuevo_toldo = sprites.create(tipo_actual, SpriteKind.Trampolin)
        tiles.placeOnTile(nuevo_toldo, lugar_t)
        tiles.setTileAt(lugar_t, assets.tile`transparency16`)
    }
}
//  CUENTA REGRESIVA
for (k = 0; k < 3; k++) {
    numero = 3 - k
    if (nena) {
        nena.sayText("" + ("" + numero), 1000, true)
    }
    
    pause(1000)
}
if (nena) {
    nena.sayText("¡CORRE!", 500, true)
}

controller.moveSprite(nena, 100, 0)
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
game.onUpdate(function on_on_update() {
    
    if (!nena || !bot) {
        return
    }
    
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
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function on_enemy_overlap(sprite: Sprite, otherSprite: Sprite) {
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
