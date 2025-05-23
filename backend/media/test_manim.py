from manim import *

class ManimVisualization(Scene):
    def construct(self):
        # Step 1: Introduce the concept of vectors
        text_vector = Tex("Vectors").scale(1.5)
        self.play(Write(text_vector))
        self.wait(1)
        self.play(FadeOut(text_vector))

        # Step 2: Show a vector in 2D space
        vector_2d = Arrow(start=ORIGIN, end=[2, 1, 0], buff=0)
        text_2d = Tex("Vector in 2D").next_to(vector_2d, UP)
        self.play(Create(vector_2d), Write(text_2d))
        self.wait(2)

        # Step 3: Introduce vector addition
        text_addition = Tex("Vector Addition").scale(1.2).to_edge(UP)
        self.play(Write(text_addition))
        v1 = Arrow(start=ORIGIN, end=[1, 2, 0], buff=0, color=BLUE)
        v2 = Arrow(start=v1.get_end(), end=[3, 1, 0], buff=0, color=GREEN)
        v3 = Arrow(start=ORIGIN, end=[4, 3, 0], buff=0, color=YELLOW)
        plus_sign = Tex("+").move_to(v1.get_end() + [0.5, 0, 0])
        self.play(Create(v1), Create(v2), Create(v3), Write(plus_sign))
        self.wait(2)
        self.play(FadeOut(v1, v2, plus_sign, v3))
        self.play(FadeOut(text_2d))
        self.play(FadeOut(text_addition))

        # Step 4: Scalar multiplication
        text_scalar = Tex("Scalar Multiplication").scale(1.2).to_edge(UP)
        self.play(Write(text_scalar))
        vector = Arrow(start=ORIGIN, end=[1, 1, 0], buff=0, color=RED)
        scalar = 2
        scaled_vector = Arrow(start=ORIGIN, end=[scalar * 1, scalar * 1, 0], buff=0, color=PURPLE)
        scalar_text = Tex(f"${scalar} \\times$").next_to(vector, LEFT)
        self.play(Create(vector), Write(scalar_text))
        self.wait(1)
        self.play(Transform(vector, scaled_vector), Transform(scalar_text, Tex(f"${scalar} \\times$").next_to(scaled_vector, LEFT)))
        self.wait(2)
        self.play(FadeOut(vector, scalar_text))
        self.play(FadeOut(text_scalar))

        # Step 5: Linear combinations
        text_linear_combination = Tex("Linear Combinations").scale(1.2).to_edge(UP)
        self.play(Write(text_linear_combination))

        v1 = Arrow(start=ORIGIN, end=[1, 0, 0], color=BLUE)
        v2 = Arrow(start=ORIGIN, end=[0, 1, 0], color=GREEN)

        a = 2
        b = 1
        av1 = Arrow(start=ORIGIN, end=[a * 1, a * 0, 0], color=BLUE)
        bv2 = Arrow(start=av1.get_end(), end=[a*1 + b * 0, a*0 + b * 1, 0], color=GREEN)
        resultant = Arrow(start=ORIGIN, end=[a*1 + b*0, a*0 + b*1, 0], color=YELLOW)

        eq = MathTex(f"{a} \\vec{{v_1}} + {b} \\vec{{v_2}}").next_to(resultant, UP)
        self.play(Create(v1), Create(v2))
        self.wait(1)
        self.play(Transform(v1, av1))
        self.play(Transform(v2, bv2))
        self.play(Create(resultant))
        self.play(Write(eq))
        self.wait(3)

        self.play(FadeOut(v1, v2, resultant, eq))
        self.play(FadeOut(text_linear_combination))

        # Step 6: Matrices
        text_matrix = Tex("Matrices").scale(1.5)
        self.play(Write(text_matrix))
        self.wait(1)
        self.play(FadeOut(text_matrix))

        # Step 7: Example Matrix
        matrix = Matrix([[1, 2], [3, 4]])
        self.play(Write(matrix))
        self.wait(2)
        self.play(FadeOut(matrix))

        # Step 8: Linear Transformations
        text_linear_transformations = Tex("Linear Transformations").scale(1.2).to_edge(UP)
        self.play(Write(text_linear_transformations))

        square = Square(side_length=2)
        self.play(Create(square))

        matrix = [[1, 1], [0, 1]]
        linear_transformation_words = Tex("Linear Transformation").next_to(square, UP)
        self.play(Write(linear_transformation_words))
        self.wait(1)
        self.play(square.animate.apply_matrix(matrix))
        self.wait(2)

        self.play(FadeOut(square, linear_transformation_words))
        self.play(FadeOut(text_linear_transformations))

        # Step 9: Eigenvectors
        text_eigenvectors = Tex("Eigenvectors").scale(1.5)
        self.play(Write(text_eigenvectors))
        self.wait(1)
        self.play(FadeOut(text_eigenvectors))

        #Step 10 : Show a conclusion
        conclusion = Tex("Linear Algebra is Cool!").scale(2)
        self.play(Write(conclusion))
        self.wait(3)
        self.play(FadeOut(conclusion))

        self.wait(1)