# works without Eyes

def main(num_iterations=sys.maxsize):
    colors = ["red", "orange", "yellow", "green", "blue", "magenta"]
    device = get_device()
    frame_count = 0
    fps = ""
    regulator = set_display_frame_rate(fps=10)

    while num_iterations > 0:
        with regulator:
            num_iterations -= 1

            frame_count += 1
            with create_canvas(device) as canvas:
                draw_eye(canvas, "test", 0, 0, 120, 120, fill='#14F6FA', outline='#14F6FA')


# works with Eyes (not tuned)
def main(num_iterations=sys.maxsize):

    eyes = Eyes(width=128,
        height=128,
        background_color='#14F6FA',
        eye_radius=46,
        eye_color='#14F6FA',
        pupil_radius=10,
        pupil_color='#14F6FA')


    device = get_device()
    frame_count = 0
    fps = ""
    regulator = set_display_frame_rate(fps=10)
    while num_iterations > 0:
        with regulator:
            num_iterations -= 1

            frame_count += 1
            with create_canvas(device) as canvas:
                # draw_eye(canvas, "test", 0, 0, 120, 120, fill='#14F6FA', outline='#14F6FA')

                angle = None
                distance_from_center_percent = None
                emotion = None

            # check params
                if angle is None:
                    eyes.move_eyes(canvas)
                elif distance_from_center_percent is None:
                # set default params to draw eyes in center position
                    eyes.move_eyes(canvas)

            # main instructions for eyes
                else:
                # set eyes working mode
                    eyes.set_emotion(emotion)
                    eyes.move_eyes(canvas, angle, distance_from_center_percent)