from manim import *

class ManimVisualization(Scene):
    def construct(self):
        # Step 1: Draw a right triangle.
        self.next_section(name="Draw a right triangle")
        triangle = Polygon([0, 0, 0], [4, 0, 0], [4, 3, 0], color=BLUE, fill_opacity=0.5)
        a_label = MathTex("a").move_to([2, -0.3, 0])
        b_label = MathTex("b").move_to([4.3, 1.5, 0])
        c_label = MathTex("c").move_to([2, 1.7, 0])
        self.play(Create(triangle), Write(a_label), Write(b_label), Write(c_label))
        self.wait(1)

        # Step 2: Draw squares on each side of the triangle.
        self.next_section(name="Draw squares on each side")
        square_a = Square(side_length=4, color=GREEN, fill_opacity=0.5).move_to([2, -2, 0])
        square_b = Square(side_length=3, color=YELLOW, fill_opacity=0.5).move_to([5.5, 1.5, 0])
        square_c = Square(side_length=5, color=RED, fill_opacity=0.5).move_to([-0.5, 3, 0]).rotate(np.arctan(3/4))

        a_squared_label = MathTex("a^2").move_to(square_a.get_center())
        b_squared_label = MathTex("b^2").move_to(square_b.get_center())
        c_squared_label = MathTex("c^2").move_to(square_c.get_center())

        self.play(Create(square_a), Create(square_b), Create(square_c))
        self.play(Write(a_squared_label), Write(b_squared_label), Write(c_squared_label))
        self.wait(1)

        # Step 3: Show that a^2 + b^2 = c^2
        self.next_section(name="Show a^2 + b^2 = c^2")
        equation = MathTex("a^2 + b^2 = c^2").move_to([0, -3, 0])
        self.play(Write(equation))
        self.wait(2)

        # Step 4: Highlight the squares a^2 and b^2, then c^2
        self.next_section(name="Highlight and Transform")
        self.play(square_a.animate.set_fill(opacity=1), square_b.animate.set_fill(opacity=1))
        self.wait(0.5)
        self.play(square_a.animate.set_fill(opacity=0.5), square_b.animate.set_fill(opacity=0.5), square_c.animate.set_fill(opacity=1))
        self.wait(0.5)
        self.play(square_c.animate.set_fill(opacity=0.5))
        self.wait(1)

        self.play(FadeOut(triangle, square_a, square_b, square_c, a_label, b_label, c_label, a_squared_label, b_squared_label, c_squared_label, equation))
        self.wait(1)