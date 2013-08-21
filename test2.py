import sfml as sf

# Move around a sprite using the absolute basics of the library.

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
video_mode = sf.VideoMode(SCREEN_WIDTH, SCREEN_HEIGHT)
window = sf.RenderWindow(video_mode, "Test")
# window.framerate_limit = 60
window.vertical_synchronization = True

#

texture = sf.Texture.from_file("img/triangle4.png")
sprite = sf.Sprite(texture)

running = True
while running:

    # Logic
    for event in window.events:
        if type(event) is sf.CloseEvent: running = False

    amt = 10
    if sf.Keyboard.is_key_pressed(sf.Keyboard.W): sprite.move((0, -amt))
    if sf.Keyboard.is_key_pressed(sf.Keyboard.S): sprite.move((0, +amt))
    if sf.Keyboard.is_key_pressed(sf.Keyboard.A): sprite.move((-amt, 0))
    if sf.Keyboard.is_key_pressed(sf.Keyboard.D): sprite.move((+amt, 0))

    # Graphics
    window.clear(sf.Color.YELLOW)
    window.draw(sprite)
    window.display()