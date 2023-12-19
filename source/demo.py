visited = [20 * [0] for i in range(20)]
for i in range(19):
    picked = 20 * [0]
    for j in range(10):
        k = 0
        while picked[k] == 1:
            k = (k + 1) % 20
        picked[k] = 1
        l = k + 1
        while picked[l] == 1:
            l = (l + 1) % 20
        picked[l] = 1
        print(k + 1, l + 1) 
        if visited[k][l] == 1:
            print("false!")
            exit(0)
        visited[k][l] = 1