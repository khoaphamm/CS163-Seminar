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

class TarjanScene(Scene):
    def construct(self):
        pass
        
        self.g = Tree(
            graph_data.tarjan_vertices,
            graph_data.tarjan_edges,
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

                self.play(*anims, run_time=0.5, rate_func=rush_from)

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
                    
                    self.play(*anims, run_time=0.2, rate_func=linear)
         
            
        

        dfs(1, None, set())
        self.wait()

        anims = []

        for label in labels:
            anims.append(Uncreate(label))
        
        back_edges = [(1, 5), (3, 7), (10, 8)] 

        for edge in back_edges:
            anims.append(self.g.edges[edge].animate.set_stroke(solarized.BASE2, opacity=0))

        self.play(*anims)

        self.play(self.g[1].animate.move_to([-3.5, 3, 0]),
                  self.g[2].animate.move_to([-2, 2, 0]),
                  self.g[3].animate.move_to([-5, 2, 0]),
                  self.g[4].animate.move_to([-2, 0, 0]),
                  self.g[5].animate.move_to([-2, 1, 0]),
                  self.g[6].animate.move_to([-5, 1, 0]),
                  self.g[7].animate.move_to([-5, 0, 0]),
                  self.g[8].animate.move_to([-5, -1, 0]),
                  self.g[9].animate.move_to([-5, -2, 0]),
                  self.g[10].animate.move_to([-5, -3, 0]))
        
        labels_anims = []
        
        for i in range(1, 11):
            acko = Tex(i, color=solarized.BASE2).move_to(self.g[i].get_center())
            self.add_foreground_mobjects(acko)
            labels_anims.append(Create(acko))
        
        self.play(*labels_anims)

        arc1 = ArcBetweenPoints(self.g[3].get_center(), self.g[7].get_center(), angle=PI/2, color=solarized.BASE00, stroke_width=6)
        arc2 = ArcBetweenPoints(self.g[8].get_center(), self.g[10].get_center(), angle=PI/2, color=solarized.BASE00, stroke_width=6)
        
        self.add(arc1)
        self.add(arc2)
        self.bring_to_back(arc1)
        self.bring_to_back(arc2)

        progress_line1 = Line(
                        self.g[1].get_center(),
                        self.g[5].get_center(),
                        color=solarized.BASE00,
                        stroke_width=6 * 1.1,
                        )
        
        
        self.add(progress_line1)
        self.bring_to_back(progress_line1)
        
        self.play(Create(arc1),
                 Create(arc2),
                 Create(progress_line1))
        
        back_edges_line = [arc1, arc2, progress_line1]
        
        self.wait()

        ##Create table 

        

        self.table = MathTable(
            [[0,0],
             [0,0],
             [0,0],
             [0,0],
             [0,0],
             [0,0],
             [0,0],
             [0,0],
             [0,0],
             [0,0]],
            row_labels = [Tex("1"), Tex("2"), Tex("3"), Tex("4"), Tex("5"), Tex("6"), Tex("7"), Tex("8"), Tex("9"), Tex("10")],                     
                          
            col_labels = [Text("num"), Text("low")],

            line_config = {"stroke_color" : solarized.BASE00, "stroke_width": 6, "color": solarized.BASE00},
            include_outer_lines=True,
            ).scale(0.5).move_to([4, 0, 0])
        
        ent = self.table.get_entries()
        for item in ent:
            item.set_color(solarized.BASE00)
            item.scale(1.5)
        
        col = self.table.get_col_labels()
        for item in col:
            item.set_color(solarized.BASE00)
            item.scale(0.75)
        
        self.play(Create(self.table))
        self.wait()

        ## Tarjan's algorithm

        # Constants
        MAXN = 20

        # Variables
        n = 0
        m = 0
        joint = [False] * MAXN

        time_dfs = 0

        holder = Tex("Time: ")
        holder.set_color(solarized.BASE00).scale(0.8).move_to([0, 3, 0])
        self.add(holder)
        cnt = Tex("0")
        cnt.set_color(solarized.BASE00).scale(0.8).next_to(holder, RIGHT)
        self.add(cnt)
        self.play(Create(holder), Create(cnt))

        bridge = 0
        low = [0] * MAXN
        num = [0] * MAXN

        display_pos = [0, 2, 0]

        def tarjan(u, pre):
            nonlocal time_dfs, bridge
            child = 0  # Number of direct children of vertex u in the DFS tree
            num[u] = low[u] = time_dfs + 1

            pos1 = self.table.get_entries((u+1, 2)).get_center()
            pos2 = self.table.get_entries((u+1, 3)).get_center()

            self.play(Transform(cnt, Tex(str(time_dfs + 1).replace("L", "")).set_color(solarized.BASE00).scale(0.8).next_to(holder, RIGHT)), run_time = 0.3)
            
            tmp1 = Tex(str(time_dfs + 1).replace("L", "")).set_color(solarized.BASE00).scale(0.8).move_to(pos1)
            tmp2 = Tex(str(time_dfs + 1).replace("L", "")).set_color(solarized.BASE00).scale(0.8).move_to(pos2)


            
            self.play(Indicate(self.g[u], color = solarized.GREEN), run_time = 0.5)
            self.play(self.g[u].animate.set_fill(solarized.VIOLET), run_time = 0.2)
            
            val1 = cnt.copy()
            val2 = cnt.copy()
            self.play(val1.animate.move_to(pos1), 
                      val2.animate.move_to(pos2), 
                      Transform(self.table.get_entries((u+1, 2)), tmp1), 
                      Transform(self.table.get_entries((u+1, 3)), tmp2), 
                      run_time = 0.3, 
                      rate_func = rush_from)  
            self.play(FadeOut(val1), 
                      FadeOut(val2),
                      ShowPassingFlash(self.table.get_cell((u+1, 2)).copy().set_color(solarized.GREEN), 
                                       run_time = 0.7,
                                       time_width = 0.20),
                      ShowPassingFlash(self.table.get_cell((u+1, 3)).copy().set_color(solarized.GREEN),
                                        run_time = 0.7,
                                        time_width = 0.20))
         

            time_dfs += 1
            for v in adj[u]:
                if v == pre:
                    continue
                if num[v] == 0:
                    tarjan(v, u)

                    pair = (u, v) if (u, v) in self.g.edges else (v, u)

                    self.play(Indicate(self.g[v], color = solarized.GREEN), 
                              Indicate(self.g[u], color = solarized.GREEN),
                              Indicate(self.g.edges[pair], color = solarized.GREEN),
                              Indicate(self.table.get_entries((u+1, 3)), color = solarized.RED, scale_factor = 1.5),
                              Indicate(self.table.get_entries((v+1, 3)), color = solarized.RED, scale_factor = 1.5),
                              run_time = 1.5)
                    

                    if(low[v] < low[u]):
                        cmpval1 = self.table.get_entries((v+1, 3)).copy()
                        cmpval2 = self.table.get_entries((u+1, 3)).copy()

                        tmp = Tex(str(low[v]).replace("L", "")).set_color(solarized.BASE00).scale(0.8).move_to(cmpval2.get_center())

                        eql_sign = Tex(f"$low[{v}] < low[{u}]$").set_color(solarized.BASE00).scale(0.8).move_to(display_pos)
                        position = Tex("$ < $").set_color(solarized.BASE00).next_to(eql_sign, DOWN).scale(0.8)
                        
                        self.play(Create(eql_sign), 
                                Create(position),
                                cmpval1.animate.move_to(position.get_center() + LEFT * 0.5), 
                                cmpval2.animate.move_to(position.get_center() + RIGHT * 0.5) , 
                                run_time = 1)
                        
                        self.wait()

                        cmpcopy1 = cmpval1.copy()
                        
                        self.play(cmpcopy1.animate.move_to(self.table.get_entries((u+1, 3)).get_center()), 
                                  Transform(self.table.get_entries((u+1, 3)), tmp), 
                                  run_time = 1)
                        self.wait()
                        
                        self.play(Uncreate(eql_sign), Uncreate(position), Uncreate(cmpval1), Uncreate(cmpval2), Uncreate(cmpcopy1), run_time = 0.5)
                    
                    low[u] = min(low[u], low[v])

                    
                
                    if low[v] == num[v]:
                        bridge_edge = DashedLine(
                        self.g[u].get_center(),
                        self.g[v].get_center(),
                        color=solarized.BASE00,
                        stroke_width=6 * 1.1,
                        dash_length=0.05)

                        

                        eql_sign = Tex(f"num[{v}] = low[{v}] =").set_color(solarized.BASE00).scale(0.8).move_to(display_pos)
                        cmpval1 = self.table.get_entries((v+1, 2)).copy()
                        cmpval2 = self.table.get_entries((v+1, 3)).copy()
                        position = Tex("0").next_to(eql_sign, RIGHT)
                        

                        self.play(Create(eql_sign),
                                  cmpval1.animate.move_to(position.get_center()), 
                                  cmpval2.animate.move_to(position.get_center()),  
                                  run_time = 1)
                        

                        self.add(bridge_edge)
                        self.bring_to_back(bridge_edge)

                        self.play(Create(bridge_edge), self.g.edges[pair].animate.set_stroke(opacity = 0), run_time = 1)

                        self.play(Uncreate(eql_sign), Uncreate(cmpval1), Uncreate(cmpval2), run_time = 0.5)

                        bridge += 1
                    child += 1
                    if u == pre:  # If u is the root of the DFS tree
                        if child > 1:
                            joint[u] = True
                    elif low[v] >= num[u]:
                        joint[u] = True
                else:
                    cmpval1 = self.table.get_entries((u+1, 3)).copy()
                    cmpval2 = self.table.get_entries((v+1, 2)).copy()

                    tmp = Tex(str(num[v]).replace("L", "")).set_color(solarized.BASE00).scale(0.8).move_to(cmpval1.get_center())

                    if(u == 7):
                        self.play(Wiggle(back_edges_line[0], scale_factor = 1.5))
                        
                    elif(u == 10):
                        self.play(Wiggle(back_edges_line[1], scale_factor = 1.5))
                    elif(u == 5):
                        self.play(Wiggle(back_edges_line[2], scale_factor = 1.5))
                    
                    if(num[v] < low[u]):
                        eql_sign = Tex(f"$num[{v}] < low[{u}]$", ).set_color(solarized.BASE00).scale(0.8).move_to(display_pos)
                        position = Tex("$ < $").set_color(solarized.BASE00).next_to(eql_sign, DOWN).scale(0.8)
                        self.play(Create(eql_sign), 
                                Create(position),
                                cmpval1.animate.move_to(position.get_center() + RIGHT * 0.5), 
                                cmpval2.animate.move_to(position.get_center() + LEFT * 0.5) , 
                                run_time = 1)
                        
                        self.wait()

                        cmpcopy2 = cmpval2.copy()
                        
                        self.play(cmpcopy2.animate.move_to(self.table.get_entries((u+1, 3)).get_center()), 
                                  Transform(self.table.get_entries((u+1, 3)), tmp), 
                                  run_time = 1)
                        self.wait()
                        
                        self.play(Uncreate(eql_sign), Uncreate(position), Uncreate(cmpval1), Uncreate(cmpval2), Uncreate(cmpcopy2), run_time = 0.5)

                    low[u] = min(low[u], num[v])
            
            self.play(self.g[u].animate.set_fill(solarized.RED), run_time = 0.2)
        
        tarjan(1, 1)
        self.wait()
