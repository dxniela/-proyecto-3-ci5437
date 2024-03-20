# Constraint: Todos los participantes deben jugar dos veces con cada uno
# de los otros participantes, una como "visitantes" y la otra como "locales".
# (forall i,j | i!=j : (exists only one d,h |: X(i,j,d,h) )
def rule_1(file, map, np, nd, nh):
    for i in range(np):
        for j in range(np):
            if i == j:
                continue

            for d in range(nd):
                for h in range(nh):
                    file.write(str(map[i][j][d][h]) + " ")

            file.write("0\n")
            
# Constraint: Dos juegos no pueden ocurrir al mismo tiempo.
# (forall i,j,d,h | i!=j : X(i,j,d,h) ⇒ not (exists n,m | (i!=n or j!=m) and n!=m : X(n,m,d,h))) and 
# (forall i,j,d,h | i!=j and h<H-2 : X(i,j,d,h)⇒ not (exists n,m | (i!=n or j!=m) and n!=m : X(n,m,d,h+1))) 
def rule_2(file, map, np, nd, nh):
    for i in range(np):
        for j in range(np):
            if i == j:
                continue

            for d in range(nd):
                for h in range(nh):
                    not_x_ijdh = -map[i][j][d][h]

                    for n in range(np):
                        for m in range(np):
                            if (i == n and j == m) or (n == m):
                                continue
                            # Constraint 3.1
                            file.write(str(not_x_ijdh) + " " + str(-map[n][m][d][h]) + " 0\n")

                            # Constraint 3.2
                            if h < nh - 1:
                                file.write(str(not_x_ijdh) + " " + str(-map[n][m][d][h + 1]) + " 0\n")

# Constraint: Un participante puede jugar a lo sumo una vez por día.
# (forall i,j,d,h | i!=j : X(i,j,d,h) => not(exists k,l | : X(i,k,d,l) or X(k,j,d,l) or X(j,k,d,l) or X(k,i,d,l)))
def rule_3(file, map, np, nd, nh):
    for i in range(np):
        for j in range(np):
            if i == j:
                continue

            for d in range(nd):
                for h in range(nh):
                    not_x_ijdh = -map[i][j][d][h]

                    for _k in range(np):
                        for l in range(nh):
                            if l == h:
                                continue

                            file.write(str(not_x_ijdh) + " " + str(-map[i][_k][d][l]) + " 0\n")
                            file.write(str(not_x_ijdh) + " " + str(-map[_k][j][d][l]) + " 0\n")
                            file.write(str(not_x_ijdh) + " " + str(-map[j][_k][d][l]) + " 0\n")
                            file.write(str(not_x_ijdh) + " " + str(-map[_k][i][d][l]) + " 0\n")

# Constraint: Un participante no puede jugar de "visitante" en dos días consecutivos,
# ni de "local" dos días seguidos.
# (forall i,j,d,h | i!=j  d<D-1 : X(i,j,d,h) => not(exists k,l | : X(i,k,d+1,l) or X(k,j,d+1,l)))
def rule_4(file, map, np, nd, nh):
    for i in range(np):
        for j in range(np):
            if i == j:
                continue

            for d in range(nd - 1):
                for h in range(nh):
                    not_x_ijdh = -map[i][j][d][h]

                    for _k in range(np):
                        for l in range(nh):
                            file.write(str(not_x_ijdh) + " " + str(-map[i][_k][d + 1][l]) + " 0\n")
                            file.write(str(not_x_ijdh) + " " + str(-map[_k][j][d + 1][l]) + " 0\n")