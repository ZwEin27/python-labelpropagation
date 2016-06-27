# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-06-24 14:56:40
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-06-27 13:30:18

import ast
import heapq

class Edge():
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

class LabelProp():

    def __init__(self):
        self.initialize_env()

    def initialize_env(self):
        self.vertex_adj_map = {}         # int: [Edge]
        self.vertex_in_adj_map = {}      # int: float
        self.vertex_deg_map = {}         # int, float
        self.vertex_label_map = {}       # int, int
        self.label_index_map = {}        # int, int
        self.vertex_f_map = {}           # int, [float]
        self.vertex_size = 0
        self.label_size = 0
        self.labelled_size = 0
        
    def setup_env(self):

        # initialize vertex_in_adj_map
        for vertex_id in self.vertex_adj_map.keys():
            if vertex_id not in self.vertex_in_adj_map:
                self.vertex_in_adj_map.setdefault(vertex_id, [])

        # setup vertex_in_adj_map
        for vertex_id in self.vertex_in_adj_map.keys():
            for edge in self.vertex_adj_map[vertex_id]:
                self.vertex_in_adj_map[edge.dest].append(edge)

        # setup vertex_deg_map
        for vertex_id in self.vertex_adj_map.keys():
            degree = .0
            if vertex_id in self.vertex_deg_map:
                degree = self.vertex_deg_map[vertex_id]
            for edge in self.vertex_adj_map[vertex_id]:
                degree += edge.weight
            self.vertex_deg_map[vertex_id] = degree

        # setup vertex_f_map
        v_set = self.vertex_label_map.keys()
        l_set = []
        # for v in v_set:
        #     l = self.vertex_label_map[v]
        #     heapq.heappush(l_set, l)
        #     self.vertex_size += 1
        # print heapq.nsmallest(len(l_set), l_set)
        for v in v_set:
            l = self.vertex_label_map[v]
            l_set.append(l)
        l_set = list(set(self.vertex_label_map.values()))
        l_set.sort()

        label_enum = 0
        for l in l_set:
        # for l in heapq.nsmallest(len(l_set), l_set):
            if int(l) == 0:
                continue
            self.label_index_map[l] = label_enum
            label_enum += 1
        self.label_size = label_enum
        print label_enum

        self.labelled_size = 0
        for v in v_set:
            arr = []
            l = int(self.vertex_label_map[v])
            if l == 0:
                # unlabelled
                for i in range(label_enum):
                    arr.append(.0)
            else:
                # labelled
                self.labelled_size += 1
                ix = int(self.label_index_map[self.vertex_label_map[v]])
                for i in range(label_enum):
                    if i == ix:
                        arr.append(1.)
                    else:
                        arr.append(0.)
            self.vertex_f_map.setdefault(v, arr)


    def load_data_from_file(self, filename):
        with open(filename, 'rb') as f:
            lines = f.readlines()
            self.load_data_from_mem(lines)

    def load_data_from_mem(self, data):
        for line in data:
            line = line.strip()
            self.process_data_line(line)
        self.setup_env()

    def process_data_line(self, dataline):
        # [vertexId, vertexLabel, [edges]]
        # unlabeled vertex if vertexLabel == 0
        # i.e. [2, 1, [[1, 1.0], [3, 1.0]]]
        
        try:

            line = ast.literal_eval(dataline)
            vertex_id = line[0]
            vertex_label = line[1]
            edges = line[2]
            edge_list = []
            self.vertex_label_map.setdefault(vertex_id, vertex_label)
            for edge in edges:
                dest_vertex_id = int(edge[0])
                edge_weight = float(edge[1])
                edge_list.append(Edge(vertex_id, dest_vertex_id, edge_weight))
            self.vertex_adj_map.setdefault(vertex_id, edge_list)

        except Exception as e:

            raise Exception("Coundn't parse vertex from line: ", line, e)

        

    def show_detail(self):
        print "Number of vertices:            ", self.vertex_size
        print "Number of class labels:        ", self.label_size
        print "Number of unlabeled vertices:  ", (self.vertex_size - self.labelled_size)
        print "Numebr of labeled vertices:    ", self.labelled_size

    def debug(self):
        labels = []
        for label in self.label_index_map.keys():
            labels.insert(int(self.label_index_map[label]), label)
        ans = []
        for vertex_id in self.vertex_f_map.keys():
            arr = self.vertex_f_map[vertex_id]
            max_f_val = .0
            max_f_val_idx = 0
            vi_ans = [vertex_id]
            im_ans = []
            for i in range(len(labels)):
                f_val = arr[i]
                if f_val > max_f_val:
                    max_f_val = f_val
                    max_f_val_idx = i
                im_ans.append([labels[i], arr[i]])

            vi_ans.append(labels[max_f_val_idx])
            vi_ans.append(im_ans)
            ans.append(vi_ans)

        return ans


    def iterate(self):
        next_vertex_f_map = {}              # int, [double]
        diff = 0

        for vertex_id in self.vertex_f_map.keys():
            if self.vertex_label_map[vertex_id]:    # skip labelled
                continue

            # update F(vertex_id) .. vertex_f_map
            next_f_value = []   # double
            f_values = self.vertex_f_map[vertex_id]

            for i in range(self.label_size):
                f_value = 0.

                for edge in self.vertex_in_adj_map[vertex_id]:
                    weight = edge.weight
                    src = edge.src
                    deg = self.vertex_deg_map[vertex_id]
                    f_value += self.vertex_f_map[src][i] * (weight / deg)
                next_f_value.append(f_value)
                if self.vertex_label_map[vertex_id] == 0:
                    if f_value > f_values[i]:
                        diff += f_value - f_values[i]
                    else:
                        diff += f_values[i] - f_value
                next_vertex_f_map[vertex_id] = next_f_value

        for vertex_id in self.vertex_label_map.keys():
            if self.vertex_label_map[vertex_id] == 0:
                continue
            next_vertex_f_map[vertex_id] = self.vertex_f_map[vertex_id]

        self.vertex_f_map = next_vertex_f_map

        return diff


    def run(self, eps, max_iter):
        self.show_detail()
        print "eps:                           ", eps
        print "max iteration                  ", max_iter

        diff = 0.
        iteration = 0
        for i in xrange(max_iter):
            iteration = i
            diff = self.iterate()
            if diff < eps:
                break
            if i % 50 == 49:
                print '\n'

        print "\niter = ", (iteration + 1), ", eps = ", diff

        return self.debug()

    def show_vertex_adj(self):
        for k, v in self.vertex_adj_map.items():
            print str([4, [[_.src, _.dest, _.weight] for _ in v]])


if __name__ == '__main__':
    labelprop = LabelProp()
    labelprop.load_data_from_file('data/sample.json')
    # labelprop.show_vertex_adj()


    ans = labelprop.run(0.00001, 1000)

    with open('data/lpop.json', 'wb') as f:
        for line in ans:
            f.write(str(line) + '\n')





