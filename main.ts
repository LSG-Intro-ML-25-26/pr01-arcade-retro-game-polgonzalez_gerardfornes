// Variables Globales
controller.right.onEvent(ControllerButtonEvent.Pressed, function () {
    animation.runImageAnimation(
    nena,
    assets.animation`maduro-right0`,
    200,
    true
    )
})
controller.left.onEvent(ControllerButtonEvent.Pressed, function () {
    animation.runImageAnimation(
    nena,
    assets.animation`maduro-left`,
    200,
    true
    )
})
function on_a_pressed () {
    // Solo salta si está tocando el suelo
    if (nena.isHittingTile(CollisionDirection.Bottom)) {
        nena.vy = -150
    }
}
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function (sprite, otherSprite) {
    game.over(false)
})
let bot_mirando_derecha = false
let velocidad3 = 0
let distancia3 = 0
let nena: Sprite = null
// Cargar Mapa
tiles.setCurrentTilemap(tilemap`prova`)
// Crear Bot (Soldado)
let bot = sprites.create(assets.image`soldado`, SpriteKind.Enemy)
let mySprite20260122T172436281Z = sprites.create(assets.image`helicoptero`, SpriteKind.Food)
// Crear Jugador (Maduro)
nena = sprites.create(assets.image`maduro`, SpriteKind.Player)
// Posicionar personajes
tiles.placeOnTile(nena, tiles.getTileLocation(6, 5))
tiles.placeOnTile(bot, tiles.getTileLocation(1, 10))
// Físicas
nena.ay = 350
bot.ay = 350
controller.moveSprite(nena, 100, 0)
nena.setStayInScreen(true)
scene.cameraFollowSprite(nena)
controller.A.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
controller.up.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
game.onUpdate(function () {
    // Calcular distancia entre Jugador y Bot
    distancia3 = Math.abs(nena.x - bot.x)
    // Ajustar velocidad según distancia (Efecto Goma Elástica)
    if (distancia3 > 120) {
        // Muy rápido si está lejos
        velocidad3 = 300
    } else if (distancia3 > 60) {
        // Rápido
        velocidad3 = 170
    } else {
        // Normal
        velocidad3 = 95
    }
    // Movimiento y Animación del Bot
    if (nena.x < bot.x) {
        // Ir a la IZQUIERDA
        bot.vx = 0 - velocidad3
        if (bot_mirando_derecha == true) {
            animation.runImageAnimation(
            bot,
            assets.animation`soldado-left`,
            200,
            true
            )
            bot_mirando_derecha = false
        }
    } else {
        // Ir a la DERECHA
        bot.vx = velocidad3
        if (bot_mirando_derecha == false) {
            animation.runImageAnimation(
            bot,
            assets.animation`soldado-right`,
            200,
            true
            )
            bot_mirando_derecha = true
        }
    }
    // Salto automático de obstáculos del Bot
    if (bot.isHittingTile(CollisionDirection.Left) || bot.isHittingTile(CollisionDirection.Right)) {
        if (bot.isHittingTile(CollisionDirection.Bottom)) {
            bot.vy = -150
        }
    }
})
let tanque = sprites.create(assets.image`tanque`, SpriteKind.Player)