import manim

class SquareToCircle(manim.Scene):
    def construct(self):
        square = manim.Square()
        circle = manim.Circle()
        self.play(manim.Create(square))
        self.play(manim.Transform(square, circle))
        self.play(manim.FadeOut(circle))

