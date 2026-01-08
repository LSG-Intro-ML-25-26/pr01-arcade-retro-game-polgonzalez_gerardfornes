def on_right_pressed():
    animation.run_image_animation(nena,
        assets.animation("""
            nena-animation-right
            """),
        500,
        False)
controller.right.on_event(ControllerButtonEvent.PRESSED, on_right_pressed)

def on_left_pressed():
    animation.run_image_animation(nena,
        assets.animation("""
            nena-animation-left
            """),
        500,
        False)
controller.left.on_event(ControllerButtonEvent.PRESSED, on_left_pressed)

# Boton saltar + gravetat
def on_a_pressed():
    if nena.is_hitting_tile(CollisionDirection.BOTTOM):
            nena.vy = -150
nena: Sprite = None
tiles.set_current_tilemap(tilemap("""
    prova
    """))
nena = sprites.create(assets.image("""
    nena-front
    """), SpriteKind.player)
nena.ay = 350
controller.move_sprite(nena, 100, 0)
nena.set_stay_in_screen(True)
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)
controller.up.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)
scene.camera_follow_sprite(nena)