# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-06-24 14:56:40
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-06-27 11:11:13


class Edge():
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight



class LabelProp():

    def __init__(self, steps=10):
        self.vertex_adj_map = {}         # int: [Edge]
        self.vertex_in_adj_map = {}      # int: float
        self.vertex_deg_map = {}         # int, float
        self.vertex_label_map = {}       # int, int
        self.label_index_map = {}        # int, int
        self.vertex_f_map = {}           # int, [float]
        self.vertex_size = 0
        self.label_size = 0
        self.labelled_size = 0

        self.steps = steps

    def show_detail(self):
        print "Number of vertices:            ", self.vertex_size
        print "Number of class labels:        ", self.labelSize
        print "Number of unlabeled vertices:  ", (self.vertexSize - self.labeledSize)
        print "Numebr of labeled vertices:    ", self.labeledSize

    def debug(self):
        labels = []
        for label in self.label_index_map.keys():
            labels.insert(int(self.label_index_map[label]), label)
        ans = [vertex_id]
        for vertex_id in self.vertex_f_map.keys():
            arr = float(self.vertex_f_map[vertex_id])
            max_f_val = .0
            max_f_val_idx = 0

            im_ans = []
            for i in range(len(labels)):
                f_val = arr[i]
                if f_val > max_f_val:
                    max_f_val = f_val
                    max_f_val_idx = i
                im_ans.append([labels[i, arr[i]]])

            ans.append(labels[max_f_val_idx])
            ans.append(im_ans)

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
        print "max iteration                  ", maxIter

        diff = 0.
        iteration = 0
        for i in xrange(max_iter):
            iteration = i
            print '.'
            diff = self.iterate()
            if diff < eps:
                break
            if i % 50 == 49:
                print '\n'

        print "\niter = " + (iteration + 1) + ", eps = " + diff

        self.debug()



if __name__ == '__main__':
    labelprop = LabelProp()
    





