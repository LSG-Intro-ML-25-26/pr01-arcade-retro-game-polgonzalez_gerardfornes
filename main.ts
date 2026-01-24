let nueva_minita: Sprite;
let numero: number;
namespace SpriteKind {
    export const Obstacle = SpriteKind.create()
}

controller.right.onEvent(ControllerButtonEvent.Pressed, function on_right_pressed() {
    animation.runImageAnimation(nena, assets.animation`
            maduro-right0
            `, 200, true)
})
controller.left.onEvent(ControllerButtonEvent.Pressed, function on_left_pressed() {
    animation.runImageAnimation(nena, assets.animation`
            maduro-left
            `, 200, true)
})
function on_a_pressed() {
    if (nena.isHittingTile(CollisionDirection.Bottom)) {
        nena.vy = -155
    }
    
}

sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function on_on_overlap(sprite: Sprite, otherSprite: Sprite) {
    game.over(false)
})
let bot_mirando_derecha = false
let velocidad3 = 0
let distancia3 = 0
let nena : Sprite = null
tiles.setCurrentTilemap(tilemap`
    prova
    `)
let helicopter = sprites.create(assets.image`
        helicoptero
        `, SpriteKind.Obstacle)
tiles.placeOnTile(helicopter, tiles.getTileLocation(60, 10))
let tanque = sprites.create(assets.image`
    tanque
    `, SpriteKind.Obstacle)
tiles.placeOnTile(tanque, tiles.getTileLocation(66, 10))
let bot = sprites.create(assets.image`
    soldado0
    `, SpriteKind.Enemy)
tiles.placeOnTile(bot, tiles.getTileLocation(1, 7))
nena = sprites.create(assets.image`
    maduro
    `, SpriteKind.Player)
tiles.placeOnTile(nena, tiles.getTileLocation(6, 9))
//  Crear Minas
let lista_lugares = tiles.getTilesByType(assets.tile`
    interrogacion
    `)
for (let lugar of lista_lugares) {
    nueva_minita = sprites.create(assets.image`
        minita3
        `, SpriteKind.Enemy)
    tiles.placeOnTile(nueva_minita, lugar)
    tiles.setTileAt(lugar, assets.tile`
        transparency16
        `)
}
nena.ay = 350
bot.ay = 350
nena.setStayInScreen(true)
scene.cameraFollowSprite(nena)
// CUENTA REGRESIVA
controller.moveSprite(nena, 0, 0)
for (let i = 0; i < 3; i++) {
    numero = 3 - i
    nena.sayText("" + ("" + numero), 1000, true)
    pause(1000)
}
nena.sayText("¡CORRE!", 500, true)
controller.moveSprite(nena, 100, 0)
controller.A.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
controller.up.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
game.onUpdate(function on_on_update() {
    
    distancia3 = Math.abs(nena.x - bot.x)
    if (distancia3 > 90) {
        velocidad3 = 320
    } else if (distancia3 > 30) {
        velocidad3 = 190
    } else {
        velocidad3 = 95
    }
    
    //  Movimiento Bot
    if (nena.x < bot.x) {
        bot.vx = 0 - velocidad3
        if (bot_mirando_derecha == true) {
            animation.runImageAnimation(bot, assets.animation`
                    soldado-left0
                    `, 500, true)
            bot_mirando_derecha = false
        }
        
    } else {
        bot.vx = velocidad3
        if (bot_mirando_derecha == false) {
            animation.runImageAnimation(bot, assets.animation`
                    soldado-right0
                    `, 200, true)
            bot_mirando_derecha = true
        }
        
    }
    
    //  Salto Bot
    if (bot.isHittingTile(CollisionDirection.Left) || bot.isHittingTile(CollisionDirection.Right)) {
        if (bot.isHittingTile(CollisionDirection.Bottom)) {
            bot.vy = -155
        }
        
    }
    
})
