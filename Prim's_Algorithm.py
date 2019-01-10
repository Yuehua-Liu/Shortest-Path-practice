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


def prime_algorithm(G, start):
    selected_nodes = list(start)
    selected_edges = []

    flag = 1  # 判斷是不是全部點都被選到的指標
    while flag:
        compare_dict = {}
        # 確定現在選到那些點，建一個list裡面有所有點延伸出去的邊
        for n in selected_nodes:
            for e in G.edges(n):
                # 第一個判斷式排除已經選過的edges
                if e in selected_edges:
                    pass
                # 第二個判斷式排除會形成circuit的edges
                elif (e[0] in selected_nodes) and (e[1] in selected_nodes):
                    pass
                else:
                    # print(e)
                    # print(G.get_edge_data(e[0], e[1]))
                    weight = G.get_edge_data(e[0], e[1])['weight']
                    compare_dict.update({e: weight})
        # 從包含當前可選擇邊的dict中找最小加入
        # 先隨便取字典第一組資料當參考基準
        x = list(compare_dict.keys())[0]
        present_group = [x, compare_dict[x]]
        # 從loop中比出最小邊，要用這個方法是為了防止相同weight的邊出現讓抓取edge資料出錯
        # 下面loop 結束後，present_group 的值就會是最小的edge，就可以進到下一步append
        for i in compare_dict:
            if compare_dict[i] >= present_group[1]:
                pass
            else:
                present_group[0] = i
                present_group[1] = compare_dict[i]

        # selected_nodes append新的點 selected_edges append 新的邊
        selected_edges.append([present_group[0], present_group[1]])
        if present_group[0][0] in selected_nodes:
            selected_nodes.append(present_group[0][1])
        else:
            selected_nodes.append(present_group[0][0])

        # 驗證是否所有點都已經選到
        if len(selected_nodes) == len(G._nodes):
            flag = 0
        else:
            pass
    temp = []
    for i in selected_edges:
        temp.append((i[0][0], i[0][1], i[1]))
    for x in range(len(temp)-1, 1, -1):
        for y in range(0, x, 1):
            if int(temp[y][2]) > int(temp[y+1][2]):
                move = temp[y]
                temp[y] = temp[y+1]
                temp[y+1] = move
    for e in temp:
        print(e[0] + ' ' + e[1] + ' ' + str(e[2]))


# 建立初始 graph
G = Graph()
edge_num = input('輸入Edge組數：')
for i in range(int(edge_num)):
    edge_data = input('')
    edge_data = edge_data.split(' ')
    G.add_edge(edge_data[0], edge_data[1], weight=int(edge_data[2]))
beg_vex = input('start vertex：')

prime_algorithm(G, beg_vex)
