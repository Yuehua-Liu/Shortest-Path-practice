class DiGraph(object):
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


def dijkstra_algorithm(G, start):
    selected_nodes = list(start)
    selected_nodes_with_weight = []
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
                # 感覺這裡需要再加一格篩掉方向不同的步驟
                else:
                    # ------------------working on it---------------------
                    # 這邊處理可以選的邊中，其累進值為多少，然後再打包進compare_dict做比較
                    # print(e)
                    # print(G.get_edge_data(e[0], e[1]))
                    # 首先處理root出發狀況，就照prime方式走
                    if start in e:
                        # print('up：', e)
                        if e[0] not in selected_nodes:
                            continue
                        else:
                            weight = G.get_edge_data(e[0], e[1])['weight']
                            compare_dict.update({e: weight})
                            G.data_dict[e]['count'] += 1
                            # print(G.data_dict)
                    # 這邊開始處理累加狀況
                    else:
                        # 先抓出某edge其中一個點在selected_edge list中的其他邊，然後比較count，最大的取用
                        count_compare = []
                        # print('down：', e)
                        if e[0] not in selected_nodes:
                            continue
                        else:
                            for n in e:
                                if n not in selected_nodes:
                                    pass
                                else:
                                    for m in selected_edges:
                                        # print('selected_edges：', selected_edges)
                                        # print('n is ：', n)
                                        # print('m is ：', m)
                                        # print(m[0][0])
                                        #
                                        # print('/////////////////')
                                        if n in m[0]:
                                            count_compare.append(m)
                                            # print('count_compare：', count_compare)
                                            # print('*********\n')


                            val_group = [count_compare[0][0], G.data_dict[count_compare[0][0]]['count']]
                            for each in count_compare:
                                if G.data_dict[each[0]]['count'] > val_group[1]:
                                    val_group[0] = each[0]
                                    val_group[1] = G.data_dict[each[0]]['count']
                                else:
                                    pass
                            last_weight = 0
                            for x in selected_edges:
                                if x[0] == val_group[0]:
                                    last_weight = x[1]
                                    break
                                else:
                                    pass
                            weight = last_weight + G.get_edge_data(e[0], e[1])['weight']
                            compare_dict.update({e: weight})
        # print('--------------------------------------------------------')
        # print(compare_dict)
        if len(compare_dict) == 0:
            flag = 0
        else:
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
                selected_nodes_with_weight.append([present_group[0][1], present_group[1]])
                G.data_dict[e]['count'] += 1
            else:
                selected_nodes.append(present_group[0][0])
                selected_nodes_with_weight.append([present_group[0][0], present_group[1]])
                G.data_dict[e]['count'] += 1

            # 驗證是否所有點都已經選到(這邊要修改成，compare_dict==none)
            # if compare_dict == None:
            #     flag = 0
            # else:
            #     pass

    # print(selected_edges)
    # print(selected_nodes_with_weight)
    min_ele = selected_nodes_with_weight[0]
    for element in selected_nodes_with_weight[1:]:
        if min_ele[1] > element[1]:
            # 交換
            min_ele = element

        else:
            pass

    temp = []
    for i in selected_nodes_with_weight:
        temp.append((i[0], i[1]))
    for x in range(len(temp) - 1, 1, -1):
        for y in range(0, x, 1):
            if int(temp[y][1]) > int(temp[y + 1][1]):
                move = temp[y]
                temp[y] = temp[y + 1]
                temp[y + 1] = move
    print(start + ' ' + str(0))
    for e in temp:
        print(e[0] + ' ' + str(e[1]))


# 建立初始 graph
G = DiGraph()
edge_num = input('輸入Edge組數：')
for i in range(int(edge_num)):
    edge_data = input('')
    edge_data = edge_data.split(' ')
    G.add_edge(edge_data[0], edge_data[1], weight=int(edge_data[2]), count=0)
beg_vex = input('start vertex：')

dijkstra_algorithm(G, beg_vex)

