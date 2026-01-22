/**
 * 1. PRIMER: Creem les variables i els personatges
 */
// Animació Dreta
controller.right.onEvent(ControllerButtonEvent.Pressed, function () {
    animation.runImageAnimation(
    nena,
    assets.animation`nena-animation-right`,
    500,
    false
    )
})
// Animació Esquerra
controller.left.onEvent(ControllerButtonEvent.Pressed, function () {
    animation.runImageAnimation(
    nena,
    assets.animation`nena-animation-left`,
    500,
    false
    )
})
// 5. ARA SÍ: Els controls i animacions (un cop la nena ja existeix)
// Funció de saltar
function on_a_pressed () {
    // Només salta si toca el terra
    if (nena.isHittingTile(CollisionDirection.Bottom)) {
        nena.vy = -150
    }
}
let nena: Sprite = null
// Posem el mapa
tiles.setCurrentTilemap(tilemap`prova`)
// 2. Creem la NENA
nena = sprites.create(assets.image`nena-front`, SpriteKind.Player)
// 2. Creem la NENA
nena = sprites.create(assets.image`tanque`, SpriteKind.Enemy)
// Gravetat
nena.ay = 350
// Només es mou esquerra/dreta amb tecles
controller.moveSprite(nena, 100, 0)
nena.setStayInScreen(true)
// IMPORTANT: Això fa que la nena es pinti PER SOBRE de tot
nena.z = 10
// 4. Càmera
scene.cameraFollowSprite(nena)
controller.A.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
controller.up.onEvent(ControllerButtonEvent.Pressed, on_a_pressed)
let mySprite20260122T170716803Z = 0
