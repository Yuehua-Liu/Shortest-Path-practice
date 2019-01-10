class Graph(object):
    def __init__(self):
        self._nodes = []
        self._edges = []
        self.data_dict = {}

    def add_edge(self, u_of_edge, v_of_edge, **attr):
        u, v = u_of_edge, v_of_edge
        # add nodes
        if u not in self._nodes:
            self._nodes.append(u)
        if v not in self._nodes:
            self._nodes.append(v)
        if (u, v) not in self._edges:
            self._edges.append((u, v))
        # add the edge
        self.data_dict.update({(u, v): attr})

    def get_edge_data(self, u_of_edge, v_of_edge):
        u, v = u_of_edge, v_of_edge
        return self.data_dict[(u, v)]

    def edges(self, *attr):
        if len(attr) == 0:
            return self._edges
        else:
            temp_ls = []
            for e in self._edges:
                if attr[0] in e:
                    temp_ls.append(e)
                else:
                    pass
            return temp_ls


def is_bridge(new_edge, selected_edges, selected_nodes):
    correct_flag = 0
    if (new_edge[0] in selected_nodes) and (new_edge[1] in selected_nodes):
        present_edges = []
        for i in selected_edges:
            present_edges.append(i[0])

        e = new_edge
        node_list = [e[0]]
        pop_list = []
        flag = 1
        pointer = 0
        while flag:
            # find circuit
            # 從這段print表示 select edge跟本只是一直選到 (a,d) 沒跳到下一個過
            # 要再比對一下原本主函式跟這個函式中間的流程問題
            if e[1] in node_list:
                correct_flag = 0
                break
            # no circuit inside
            elif pointer == (len(node_list)):
                correct_flag = 1
                break
            else:
                pop_list.append(node_list[pointer])
                for i in selected_edges:
                    if node_list[pointer] in i:
                        for temp in i:
                            if temp not in pop_list:
                                if temp is not node_list[pointer]:
                                    node_list.append(temp)
                                else:
                                    pass
                            else:
                                pass
                pointer += 1

        # 針對新加入後的edge組來走訪一次，如果能走一圈代表為circuit

    else:
        pass
    return correct_flag


def kruskal_algorithm(G):
    selected_nodes = []
    selected_edges = []
    selected_edges_no_weight = []

    flag = 1  # 判斷是不是全部點都被選到的指標
    while flag:
        compare_dict = {}
        # 先把所有edge(排除選過跟會形成circuit的)加到compare_dict中
        for e in G.edges():
            # 第一個判斷式排除已經選過的edges
            if e in selected_edges_no_weight:
                pass
            # 第二個判斷式排除會形成circuit的edges
            # 但這個判斷式需要再一層，進一步分出bridge和circuit
            elif (e[0] in selected_nodes) and (e[1] in selected_nodes):
                # 進一步確認是否為bridge，是就加進去compare_dict
                # pass
                if is_bridge(e, selected_edges_no_weight, selected_nodes):
                    weight = G.get_edge_data(e[0], e[1])['weight']
                    compare_dict.update({e: weight})
                else:
                    pass
            else:
                weight = G.get_edge_data(e[0], e[1])['weight']
                compare_dict.update({e: weight})

        # 先隨便設一組邊的weight值為最小
        min_edge = list(compare_dict.keys())[0]
        min_group = [min_edge, compare_dict[min_edge]]
        # 然後在迴圈中再一一比較找最小
        for i in compare_dict:
            if min_group[1] >= compare_dict[i]:
                min_group = [i, compare_dict[i]]
            else:
                pass
        # min_group確定是這一輪比較下最小的edge組，放進selected中
        selected_edges.append(min_group)
        selected_edges_no_weight.append(min_group[0])
        for n in min_group[0]:
            if n not in selected_nodes:
                selected_nodes.append(n)

        # 驗證是否所有點都已經選到
        if len(selected_nodes) == len(G._nodes):
            flag = 0
        else:
            pass
    # 最後輸出，先將selected_edge中資料整理，排序，印出
    temp = []
    for i in selected_edges:
        temp.append((i[0][0], i[0][1], i[1]))
    for x in range(len(temp) - 1, 1, -1):
        for y in range(0, x, 1):
            if int(temp[y][2]) > int(temp[y + 1][2]):
                move = temp[y]
                temp[y] = temp[y + 1]
                temp[y + 1] = move
    for e in temp:
        print(e[0] + ' ' + e[1] + ' ' + str(e[2]))


# 建立初始 graph
g = Graph()
edge_num = input('輸入Edge組數：')
for i in range(int(edge_num)):
    edge_data = input('輸入Edge組：')
    edge_data = edge_data.split(' ')
    g.add_edge(edge_data[0], edge_data[1], weight=int(edge_data[2]))


kruskal_algorithm(g)
