from re import A
from scipy.optimize import linprog
from manim import *
import math
import solarized




class Tree(Graph):
    def __init__(self, *args, label_class=MathTex, **kwargs):
        # Hack to fix "labels=True" when TeX is not available
        # (uses `Text` instead of `MathTex`)
        # if kwargs.get("labels") == True: #sorryjako
        #     # Assumes vertices are positional arg
        #     assert "vertices" not in kwargs
        #     labels = dict(
        #         (v, label_class(str(v), fill_color=solarized.BASE00).scale(0.7)) for v in args[0]
        #     )
        #     kwargs["labels"] = labels

        super().__init__(*args, **kwargs)

    def get_adjacency_list(self):
        adj = dict([(v, []) for v in self.vertices])
        for v1, v2 in self.edges:
            adj[v1].append(v2)
            adj[v2].append(v1)

        return adj

    def rot(self, mid, theta):
        new_layout = {}
        for u in self.vertices:
            pos_u = self[u].get_center()
            pos_u -= mid
            new_layout[u] = np.array( \
                (pos_u[0] * math.cos(theta) + pos_u[1] * math.sin(theta), \
                pos_u[1] * math.cos(theta) - pos_u[0] * math.sin(theta), \
                pos_u[2]))
            new_layout[u] += mid
        self.change_layout(new_layout)

    def dfsAnimation(self, start):
        adj = self.get_adjacency_list()

        res_vertices = [[]]
        res_edges = [[]]
        res_parents = {start: None}
        seen = set()

        def dfs_visit(v):
            if(v in seen): return
            res_vertices.append([v])
            seen.add(v)
            for v2 in adj[v]:
                if v2 not in seen:
                    res_edges.append([(v, v2)])
                    res_parents[v2] = v
                    dfs_visit(v2)

        dfs_visit(start)

        return res_vertices, res_edges, res_parents

    def bfs(self, start):
        adj = self.get_adjacency_list()

        res_vertices = [[start]]
        res_edges = [[]]
        res_parents = {start: None}
        seen = set([start])

        while True:
            cur_vertices = []
            cur_edges = []

            for v1 in res_vertices[-1]:
                for v2 in adj[v1]:
                    if v2 not in seen:
                        cur_vertices.append(v2)
                        seen.add(v2)
                        cur_edges.append((v1, v2))
                        res_parents[v2] = v1 

            if cur_vertices:
                res_vertices.append(cur_vertices)
                res_edges.append(cur_edges)
            else:
                break

        return res_vertices, res_edges, res_parents

    def get_path(self, start, end):
        _, _, parents = self.dfs(end)
        path = [start]

        while path[-1] != end:
            path.append(parents[path[-1]])

        return path

    def set_colors_all(self, color=solarized.BASE00):
        for v in self.vertices:
            self[v].set_color(color)

        for e in self.edges:
            self.edges[e].set_color(color)

        return self

    def set_colors(self, vertex_colors=None, edge_colors=None):
        if vertex_colors is not None:
            for v, c in vertex_colors.items():
                self[v].set_fill(c)

        if edge_colors is not None:
            for e, c in edge_colors.items():
                if e not in self.edges:
                    e = e[1], e[0]

                self.edges[e].set_color(c)

        return self

    def set_colors_and_enlarge(self, vertex_colors=None, edge_colors=None, sc=1):
        if vertex_colors is not None:
            for v, c in vertex_colors.items():
                self[v].set_fill(c)
                self[v].scale(sc)

        if edge_colors is not None:
            for e, c in edge_colors.items():
                if e not in self.edges:
                    e = e[1], e[0]

                self.edges[e].set_color(c)

        return self

    def set_path_color(self, start, end, color=solarized.RED):
        path = self.get_path(start, end)
        vertex_colors = dict((v, color) for v in path)
        edge_colors = dict(((a, b), color) for a, b in zip(path, path[1:]))

        return self.set_colors(vertex_colors, edge_colors)

    def hanging_position(
        self,
        start,
        end,
        shift=(0.0, 0.0, 0.0),
        delta=0.3,
        scale=0.5,
        pinned_vertex=None,  # A vertex that should not change position
        custom_layers = {}    # a dictionary containing the order of nodes in some layers
    ):
        if pinned_vertex is not None:
            original_pos = self[pinned_vertex].get_center()

        positions = {}
        top = self.get_path(start, end)

        adj = self.get_adjacency_list()
        weights = {}
        level_order = {}
        pi = {}
        parent = {}
        i = 0
        for u in self.vertices:
            pi[u] = i
            i = i + 1

        def weight(v, parents, depth):
            w = 1
            for v2 in adj[v]:
                if v2 not in parents:
                    w += weight(v2, [v], depth + 1)
            weights[v] = w
            if depth > 0:
                parent[v] = parents[0]
                positions[v] = np.array([0.0, -depth, 0])
                if not depth in level_order:
                    level_order[depth] = []
                level_order[depth].append(v)
            return w

        for i, v1 in enumerate(top):
            positions[v1] = np.array([i * 1.0 - len(top) / 2.0 + 0.5, 0.0, 0.0])
            weight(v1, top, 0)

        for depth, order in custom_layers.items():
            level_order[depth] = order

        # LP
        # variably:    n* x_i ... pozice na x-ove ose
        #              n* c_i ... rozdil na x-ove ose me a meho otce
        #              vektor promennych je konkatenace x_i a c_i
        # constrainty: pro rooty je x_i = jejich pozice
        #              jinak kdyz x_i a x_j vedle sebe tak x_j > x_i + delta
        #              a nakonec c_i >= |x_i - x_p(i)|
        # MIN sum w_i * c_i kde w_i je velikost podstromu

        n = len(self.vertices)
        num_var = 2 * n

        A = []
        b = []
        c = np.zeros(num_var)

        for u in self.vertices:
            if u in top:  # je-li to root tak x_i = současná pozice i
                l = np.zeros(num_var)
                l[pi[u]] = 1
                A.append(l)
                A.append(-l)
                b.append(positions[u][0])
                b.append(-positions[u][0])
            else:  # jinak c_i >= |x_i - x_p(i)|
                c[n + pi[u]] = weights[u]
                l = np.zeros(num_var)
                l[pi[u]] = 1
                l[pi[parent[u]]] = -1
                l[n + pi[u]] = -1
                A.append(l)
                l = -l
                l[n + pi[u]] = -1
                A.append(l)
                b.append(0)
                b.append(0)

        for i in level_order:
            lev = level_order[i]
            for i in range(1, len(lev)):  # pro ty vedle plati x_j > x_i + delta
                l = np.zeros(num_var)
                l[pi[lev[i]]] = -1
                l[pi[lev[i - 1]]] = 1

                A.append(l)
                b.append(-delta)

        constraints = []
        for i in range(num_var):
            constraints.append((None, None))

        res = linprog(c, A_ub=A, b_ub=b, bounds=constraints)

        for u in self.vertices:
            positions[u][0] = 1.0 * res.x[pi[u]]

        for k in positions:
            positions[k] *= scale

        # nema smysl mit oboje
        assert (tuple(shift) == (0.0, 0.0, 0.0)) or (pinned_vertex is None)

        if pinned_vertex is not None:
            shift = original_pos - positions[pinned_vertex]

        for k in positions:
            positions[k] += shift

        return positions

    def path_animation(self, start, end, time_per_step=0.5, color=solarized.RED, base_color=solarized.BASE00, rect=None):
        path = self.get_path(start, end)
        
        vertices = []
        edges = []
        prev = -42
        for u in path:
            vertices.append([u])
            if prev != -42:
                edges.append([(prev, u)])
            prev = u
        edges.append([])
        #print(vertices)
        #print(edges)
        return self.dfs_animation(start, \
            time_per_step = time_per_step, \
            override_layers = (vertices, edges), \
            color = color, \
            annotations = False,\
            blinking = False, \
            rect = rect)

    def bfs_animation(
        self,
        start,
        turn_furthest_off=False,
        time_per_step=2,
        override_layers=None,  # Použije tyhle data místo bfs
        annotations=False,
        annotations_scale = 0.75,
        blinking=True,
        rect = None,
        color = solarized.MAGENTA, 
        final_highlight = None,
        custom_angles = None,
        distance_offset=0,
    ):
        

        if override_layers is None:
            v_layers, e_layers, _ = self.dfs(start)
            e_layers.append([])
        else:
            v_layers, e_layers = override_layers

        def vertex_on(v: Dot):
            v.set_fill(color)
            # v.scale(1.5)
            return v

        temp_mobjects = []

        all_anims = []
        to_unhighlight = []

        anims_next = []
        trigger_was_used = False
        txt_to_highlight = []
        for i in range(len(v_layers)):
            anims = anims_next
            anims_next = []

            for (v1, v2) in e_layers[i]:
                progress_line = Line(
                    self[v1].get_center(),
                    self[v2].get_center(),
                    color=color,
                    stroke_width=6 * 1.1,
                )
                temp_mobjects.append(progress_line)
                anims.append(Create(progress_line, rate_func=linear))

            
            for v in v_layers[i]:
                if blinking == True:
                    anims_next.append(
                        Flash(self[v], color=solarized.BASE1, time_width=0.25)
                    )
                if rect != None and trigger_was_used == False:
                    trigger_node, obj1, obj2 = rect
                    if v == trigger_node:
                        anims_next.extend([
                            Indicate(obj1, color = solarized.BASE1, run_time=2),
                            Indicate(obj2, color = solarized.BASE1, run_time=2)
                        ])
                        trigger_was_used = True

                anims.append(ApplyFunction(vertex_on, self[v]))

                if annotations:
                    custom_angle = None
                    if custom_angles != None and v in custom_angles:
                        custom_angle = custom_angles[v]
                    txt = Tex(
                            str(i+distance_offset),
                            color=solarized.BASE00#,font="Helvetica Neue",weight="SEMIBOLD",
                        ).scale(annotations_scale).move_to(self.get_annotation_position(v, custom_angle = custom_angle))
                    annotation = (
                        txt
                    )
                    anims.append(Create(annotation))
                    # anims_next.append(Create(annotation))
                    temp_mobjects.append(annotation)
                    if i == final_highlight:
                        txt_to_highlight.append(txt)

                if i == len(v_layers) - 1 and not turn_furthest_off:
                    # Do not turn these off.
                    pass
                else:
                    to_unhighlight.append(v)

            all_anims.append(AnimationGroup(*anims, run_time=time_per_step))

        # Add any remaining animations
        all_anims.append(AnimationGroup(*anims_next, run_time=time_per_step))

        highlight_anims = []
        if final_highlight != None:
            for txt in txt_to_highlight:
                highlight_anims.append(Indicate(txt, color = solarized.BLUE))

        # Tuple of animations
        if final_highlight == None:
            return (
                AnimationGroup(*all_anims, lag_ratio=0.95),
                # Cleanup animations
                AnimationGroup(
                    *(
                        [FadeOut(l) for l in temp_mobjects]
                        + [
                            self[v].animate.set_fill(solarized.BASE00)
                            for v in to_unhighlight
                        ]
                    ),
                ),
            )
        else:
            return (
                AnimationGroup(*all_anims, lag_ratio=0.95),
                highlight_anims,
                # Cleanup animations
                AnimationGroup(
                    *(
                        [FadeOut(l) for l in temp_mobjects]
                        + [
                            self[v].animate.set_fill(solarized.BASE00)
                            for v in to_unhighlight
                        ]
                    ),
                ),
            )

    def get_annotation_position(self, vi, custom_angle=None):
        v: Dot = self[vi]

        # v.radius does not take into account v.scale(3.) etc
        radius = np.linalg.norm(v.get_top() - v.get_bottom()) / 2
        distance = radius + 0.2

        if custom_angle != None:
            angle, dist_scale = custom_angle
            angle *= 2*math.pi / 360.0
            pos = v.get_center()
            pos[0] += np.cos(angle) * distance * dist_scale
            pos[1] += np.sin(angle) * distance * dist_scale
            return pos

        neighbors = self.get_adjacency_list()[vi]

        if not neighbors:
            return v.get_center() + UP * distance

        best = None
        best_score = None
        for angle in np.linspace(0, 2 * np.pi):
            pos = v.get_center()
            pos[0] += np.cos(angle) * distance
            pos[1] += np.sin(angle) * distance

            score = 1000000
            for nei in neighbors:
                ne: Dot = self[nei]
                score = min(score, np.linalg.norm(pos - ne.get_center()))

            if best is None or score > best_score:
                best = pos
                best_score = score
                # if vi == 52:
                #     print("Angle", angle, best_score, pos)

        assert best is not None
        return best


class ExternalLabeledDot(Dot):
    def __init__(self, label, *args, **kwargs):
        if isinstance(label, str):
            rendered_label = Tex(label, color=solarized.BASE00).scale(3)
        else:
            rendered_label = label

        self.label = rendered_label
        super().__init__(*args, **kwargs)

        self.label.move_to(self.get_center())
        self.add(label)

    def reposition_label(self, g: Tree, v):
        pos = g.get_annotation_position(v)

        alignment = LEFT
        if (pos - g[v].get_center())[0] < 0:
            alignment = RIGHT

        self.label.move_to(pos).shift(-self.label.width * 0.5 * alignment)
    
    def get_center(self) -> np.ndarray:
        # This ignores the label when computing the center,
        # only considering the dot
        return self.get_arc_center()

class OScene(Scene):
    def outline(self, part):
        greyish = solarized.BASE00
        sz = 1
        fst = MarkupText(f"1) Trees", color=greyish, size = sz)
        snd = MarkupText(f"2) The algorithm", color=greyish, size = sz)
        thd = MarkupText(f"3) Why it works", color=greyish, size = sz)
        outline_list = [
            fst, snd, thd
        ]
        fst.shift(1.5*UP)
        thd.shift(1.5*DOWN)

        full_list = VGroup(*outline_list)

        for i in range(3):
            outline_list[i].align_to(full_list, LEFT)

        self.play(FadeIn(full_list))

        self.play(Indicate(outline_list[part - 1], color=solarized.BASE02))
        self.wait()

        self.play(FadeOut(full_list))


class RotPolygon(Polygon):
    def align_and_rotate(self, obj, leftright, bottomtop, rot, correction = np.array((0,0,0))):
        self.rotate(rot)
        self.align_to(obj, leftright)
        self.align_to(obj, bottomtop)
        self.shift(correction)

    def align(self, obj, leftright, bottomtop):
        self.align_to(obj, leftright)
        self.align_to(obj, bottomtop)


class OSVGMobject(SVGMobject):
    def move_and_resize(self, offset, scale):
        self.move_to(offset)
        self.scale(scale)

class OGroup(Group):
    def move_and_resize(self, offset, scale):
        self.move_to(offset)
        self.scale(scale)
