controller.right.onEvent(ControllerButtonEvent.Pressed, function on_right_pressed() {
    animation.runImageAnimation(nena, assets.animation`
            nena-animation-right
            `, 500, false)
})
controller.left.onEvent(ControllerButtonEvent.Pressed, function on_left_pressed() {
    animation.runImageAnimation(nena, assets.animation`
            nena-animation-left
            `, 500, false)
})
//  Boton saltar + gravetat
function on_a_pressed() {
    if (nena.isHittingTile(CollisionDirection.Bottom)) {
        nena.vy = -150
    }
    
}

let nena : Sprite = null
tiles.setCurrentTilemap(tilemap`
    prova
    `)
nena = sprites.create(assets.image`
    nena-front
    `, SpriteKind.Player)
nena.ay = 350
controller.moveSprite(nena, 100, 0)
nena.setStayInScreen(true)
controller.A.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
controller.up.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
scene.cameraFollowSprite(nena)
