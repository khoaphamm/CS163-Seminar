from manim import *

import solarized
import graph_data
from utils import Tree

class DFS_scene(Scene):
    def construct(self):
        pass
        
        self.g = Tree(
            graph_data.example_vertices,
            graph_data.example_edges,
            layout="kamada_kawai",
            layout_scale= 3.5,
            vertex_config={
                #"radius": 0.4,
                "color": solarized.BASE00,
                1: {"fill_color": solarized.RED}
            },
            edge_config={"color": solarized.BASE00, "stroke_width": 6},
            labels=True,
            label_fill_color=ManimColor('#ffffff'),
        )
        self.play(DrawBorderThenFill(self.g))
        self.wait()

        adj = self.g.get_adjacency_list()

        labels = []

        def dfs(node, parent, visited):
            if node in visited:
                return
            visited.add(node)
            anims = []
            if parent is not None:
                if ((parent, node) in self.g.edges):
                    anims.append(self.g.edges[(parent, node)].animate.set_stroke(solarized.MAGENTA))
                else:
                    anims.append(self.g.edges[(node, parent)].animate.set_stroke(solarized.MAGENTA))
                anims.append(self.g[node].animate.set_fill(solarized.MAGENTA))
                acko = Tex(node, color=solarized.BASE2).move_to(self.g[node].get_center())
                labels.append(acko)
                self.add_foreground_mobjects(acko)
                anims.append(Create(acko))

                anims.append(Flash(self.g[node], color=solarized.BASE1,
                                   time_width=0.5,
                                   num_lines = 10,
                                   line_stroke_width = 3,
                                   line_length=0.3,
                                    run_time=0.7,
                                    rate_func=rush_from,
                                    flash_radius = 0.2)
                             )

                self.play(*anims)

            for child in adj[node]:
                dfs(child, node, visited)
            if parent is not None:
                anims = []
                if(node != 1):
                    anims.append(self.g[node].animate.set_fill(solarized.RED))

                    if ((parent, node) in self.g.edges):
                        anims.append(self.g.edges[(parent, node)].animate.set_stroke(solarized.RED))
                    else:
                        anims.append(self.g.edges[(node, parent)].animate.set_stroke(solarized.RED))
                    
                    self.play(*anims)
         
            self.wait(0.1)
        

        dfs(1, None, set())

        self.wait(2)

        anims = []

        for label in labels:
            anims.append(Uncreate(label))
        
        back_edges = [(1, 5), (3, 7), (3, 8), (1, 6), (9, 12)] 

        for edge in back_edges:
            anims.append(self.g.edges[edge].animate.set_stroke(solarized.BASE2, opacity=0))

        self.play(*anims)

        self.play(self.g[1].animate.move_to([0, 2.5, 0]),
                  self.g[2].animate.move_to([0, -0.5, 0]),
                  self.g[3].animate.move_to([-1, 1.5, 0]),
                  self.g[4].animate.move_to([1, -1.5, 0]),
                  self.g[5].animate.move_to([-2, 0.5, 0]),
                  self.g[8].animate.move_to([-1, -1.5, 0]),
                  self.g[7].animate.move_to([-2, -0.5, 0]),
                  self.g[6].animate.move_to([0, 0.5, 0]),
                  self.g[9].animate.move_to([1, 1.5, 0]),
                  self.g[10].animate.move_to([1, -2.5, 0]),
                  self.g[11].animate.move_to([1, 0.5, 0]),
                  self.g[12].animate.move_to([1, -0.5, 0]))
        
        labels_anims = []
        
        for i in range(2, 13):
            acko = Tex(i, color=solarized.BASE2).move_to(self.g[i].get_center())
            self.add_foreground_mobjects(acko)
            labels_anims.append(Create(acko))
        
        self.play(*labels_anims)

        arc1 = ArcBetweenPoints(self.g[1].get_center(), self.g[5].get_center(), angle=-PI/2, color=solarized.BASE00, stroke_width=6)
        arc2 = ArcBetweenPoints(self.g[9].get_center(), self.g[12].get_center(), angle=-PI/2, color=solarized.BASE00, stroke_width=6)
        
        self.add(arc1)
        self.add(arc2)
        self.bring_to_back(arc1)
        self.bring_to_back(arc2)

        progress_line1 = Line(
                        self.g[1].get_center(),
                        self.g[6].get_center(),
                        color=solarized.BASE00,
                        stroke_width=6 * 1.1,
                        )
        
        progress_line2 = Line(
                        self.g[3].get_center(),
                        self.g[8].get_center(),
                        color=solarized.BASE00,
                        stroke_width=6 * 1.1,
                        )
        
        progress_line3 = Line(
                        self.g[3].get_center(),
                        self.g[7].get_center(),
                        color=solarized.BASE00,
                        stroke_width=6 * 1.1,
                        )
        
        self.add(progress_line1)
        self.add(progress_line2)
        self.add(progress_line3)
        self.bring_to_back(progress_line1)
        self.bring_to_back(progress_line2)
        self.bring_to_back(progress_line3)
        

        self.play(Create(arc1),
                 Create(arc2),
                 Create(progress_line1),
                 Create(progress_line2),
                 Create(progress_line3))

        self.wait(2)
