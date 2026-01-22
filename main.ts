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
//  Boton saltar + gravetat
function on_a_pressed() {
    if (nena.isHittingTile(CollisionDirection.Bottom)) {
        nena.vy = -150
    }
    
}

let bot_mirando_derecha = false
let velocidad3 = 0
let distancia3 = 0
let nena : Sprite = null
let velocidad2 = 0
let distancia2 = 0
let distancia = 0
let velocidad = 0
tiles.setCurrentTilemap(tilemap`
    prova
    `)
let bot = sprites.create(assets.image`
    soldado
    `, SpriteKind.Enemy)
nena = sprites.create(assets.image`
    maduro
    `, SpriteKind.Player)
tiles.placeOnTile(nena, tiles.getTileLocation(6, 14))
tiles.placeOnTile(bot, tiles.getTileLocation(1, 10))
nena.ay = 350
controller.moveSprite(nena, 100, 0)
nena.setStayInScreen(true)
bot.ay = 350
controller.A.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
controller.up.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
scene.cameraFollowSprite(nena)
game.onUpdate(function on_on_update() {
    
    distancia3 = Math.abs(nena.x - bot.x)
    if (distancia3 > 120) {
        velocidad3 = 300
    } else if (distancia3 > 60) {
        velocidad3 = 170
    } else {
        velocidad3 = 95
    }
    
    if (nena.x < bot.x) {
        bot.vx = 0 - velocidad3
        if (bot_mirando_derecha == true) {
            animation.runImageAnimation(bot, assets.animation`
                    soldado-left
                    `, 200, true)
            bot_mirando_derecha = false
        }
        
    } else {
        bot.vx = velocidad3
        if (bot_mirando_derecha == false) {
            animation.runImageAnimation(bot, assets.animation`
                    soldado-right
                    `, 200, true)
            bot_mirando_derecha = true
        }
        
    }
    
    if (bot.isHittingTile(CollisionDirection.Left) || bot.isHittingTile(CollisionDirection.Right)) {
        if (bot.isHittingTile(CollisionDirection.Bottom)) {
            bot.vy = -150
        }
        
    }
    
})
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function on_overlap(sprite: Sprite, otherSprite: Sprite) {
    game.over(false)
})
