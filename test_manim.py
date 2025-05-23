from manim import *

class ManimVisualization(Scene):
    def construct(self):
        # Step 1: Introduce the concept of vectors.
        text_vector = Tex("Vectors:").to_edge(UP)
        self.play(Write(text_vector))
        self.wait(0.5)

        vector_definition = Tex("Represent magnitude and direction.").next_to(text_vector, DOWN)
        self.play(Write(vector_definition))
        self.wait(1)

        # Step 2: Draw a vector in 2D space.
        arrow = Arrow(start=ORIGIN, end=[2, 1, 0], buff=0)
        vector_label = MathTex(r"\vec{v}").next_to(arrow.get_end(), UP * 0.2 + RIGHT * 0.2)

        self.play(Create(arrow), Write(vector_label))
        self.wait(1)

        # Step 3: Introduce linear combinations.
        text_linear_combination = Tex("Linear Combinations:").next_to(vector_definition, DOWN, buff=0.5)
        self.play(Write(text_linear_combination))
        self.wait(0.5)

        linear_combination_definition = Tex("Scaling and adding vectors.").next_to(text_linear_combination, DOWN)
        self.play(Write(linear_combination_definition))
        self.wait(1)

        # Step 4: Show an example of a linear combination.
        vector_u = Arrow(start=ORIGIN, end=[1, -1, 0], color=GREEN, buff=0)
        vector_u_label = MathTex(r"\vec{u}").next_to(vector_u.get_end(), DOWN * 0.2 + RIGHT * 0.2)
        vector_w = Arrow(start=ORIGIN, end=[-1, 1.5, 0], color=YELLOW, buff=0)
        vector_w_label = MathTex(r"\vec{w}").next_to(vector_w.get_end(), UP * 0.2 + LEFT * 0.2)

        self.play(Create(vector_u), Write(vector_u_label), Create(vector_w), Write(vector_w_label))
        self.wait(1)

        scalar_1 = 2
        scalar_2 = 1.5
        scaled_vector_u = Arrow(start=ORIGIN, end=scalar_1 * vector_u.get_end_point(), color=GREEN, buff=0)
        scaled_vector_w = Arrow(start=ORIGIN, end=scalar_2 * vector_w.get_end_point(), color=YELLOW, buff=0)

        self.play(Transform(vector_u, scaled_vector_u), Transform(vector_w, scaled_vector_w))
        self.wait(1)

        sum_vector = Arrow(start=ORIGIN, end=scalar_1 * vector_u.get_end_point() + scalar_2 * vector_w.get_end_point(),
        color=RED, buff=0)
        sum_vector_label = MathTex(r"2\vec{u} + 1.5\vec{w}").next_to(sum_vector.get_end(), UP * 0.2)
        self.play(Create(sum_vector), Write(sum_vector_label))
        self.wait(2)

        # Step 5: Introduce Linear Transformations
        text_linear_transformation = Tex("Linear Transformations:").next_to(linear_combination_definition, DOWN, buff=0.5)
        self.play(Write(text_linear_transformation))
        self.wait(0.5)

        linear_transformation_definition = Tex("Mapping vectors to vectors while preserving linear combinations.").next_to(text_linear_transformation, DOWN)
        self.play(Write(linear_transformation_definition))
        self.wait(1)

        # Step 6: Clean up
        self.play(FadeOut(text_vector, vector_definition, arrow, vector_label, text_linear_combination,
        linear_combination_definition, vector_u, vector_u_label, vector_w, vector_w_label, sum_vector, sum_vector_label,
        text_linear_transformation, linear_transformation_definition))
        self.wait(1)

        final_text = Tex("Linear Algebra provides tools to solve systems of equations, analyze data, and understand geometric transformations.").scale(0.8)
        self.play(Write(final_text))
        self.wait(3)