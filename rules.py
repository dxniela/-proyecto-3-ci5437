from sympy import symbols, Not

# Constraint: Todos los participantes deben jugar dos veces con cada uno
# de los otros participantes, una como "visitantes" y la otra como "locales".
# (forall i,j | i!=j : (exists only one d,h |: X(i,j,d,h) )
def rule_1(participants, dates, hours, variables):
    clauses = []
    for i in participants:
        for j in participants:
            if i != j:
                # Crea una lista para almacenar las variables de los juegos en los que i y j participan
                games = []
                for d in dates:
                    for h in hours:
                        # Agrega la variable del juego al final de la lista
                        games.append(variables[(i, j, d, h)])
                # Agrega una cláusula que dice que al menos uno de estos juegos debe ocurrir
                clauses.append([g for g in games])
                # Agrega cláusulas que dicen que a lo sumo uno de estos juegos puede ocurrir
                for game in games:
                    for other_game in games:
                        if game != other_game:
                            clauses.append([-game, -other_game])
    return clauses

            
# Constraint: Dos juegos no pueden ocurrir al mismo tiempo.
# (forall i,j,d,h | i!=j : X(i,j,d,h) ⇒ not (exists n,m | (i!=n or j!=m) and n!=m : X(n,m,d,h))) 
def rule_2(participants, dates, hours, variables):
    clauses = []
    for i in participants:
        for j in participants:
            for i2 in participants:
                for j2 in participants:
                    if i != j and i2 != j2 and (i, j) != (i2, j2):
                        for d in dates:
                            for h in hours:
                                # Add the proposition to the clauses
                                clauses.append([-variables[(i, j, d, h)], -variables[(i2, j2, d, h)]])

    return clauses

# Constraint: Un participante puede jugar a lo sumo una vez por día.
# (forall i,j,d,h | i!=j : X(i,j,d,h) => not(exists k,l | : X(i,k,d,l) or X(k,j,d,l) or X(j,k,d,l) or X(k,i,d,l)))
def rule_3(participants, dates, hours, variables):
    clauses = []
    for i in participants:
        for j in participants:
            if i == j:
                continue

            for d in dates:
                for h in hours:
                    # Define the proposition
                    x_ijdh = variables[(i, j, d, h)]
                    # Negate the proposition
                    not_x_ijdh = -x_ijdh

                    for _k in participants:
                        if _k != i and _k != j:
                            for l in hours:
                                if l == h:
                                    continue
                                
                                # Define the other propositions
                                not_x_ikdl = -variables[i,_k,d,l]
                                not_x_kjdl = -variables[_k,j,d,l]
                                not_x_jkdl = -variables[j,_k,d,l]
                                not_x_kidl = -variables[_k,i,d,l]

                                # Add the clauses as lists
                                clauses.append([not_x_ijdh, not_x_ikdl])
                                clauses.append([not_x_ijdh, not_x_kjdl])
                                clauses.append([not_x_ijdh, not_x_jkdl])
                                clauses.append([not_x_ijdh, not_x_kidl])
    
    return clauses

# Constraint: Un participante no puede jugar de "visitante" en dos días consecutivos,
# ni de "local" dos días seguidos.
# (forall i,j,d,h | i!=j  d<D-1 : X(i,j,d,h) => not(exists k,l | : X(i,k,d+1,l) or X(k,j,d+1,l)))
def rule_4(participants, dates, hours, variables):
    clauses = []
    date_keys = list(dates.keys())  # Convertir las claves a una lista
    for i in participants:
        for j in participants:
            if i == j:
                continue

            for d in range(len(date_keys) - 1):  # Subtract 1 to avoid index out of range for d + 1
                for h in hours:
                    # Define the proposition
                    x_ijdh = variables[i,j,date_keys[d],h]

                    # Negate the proposition
                    not_x_ijdh = -x_ijdh

                    for _k in participants:
                        for l in hours:
                            if _k != i:
                                # Define the other propositions
                                not_x_ikd1l = -variables[i,_k,date_keys[d + 1],l]
                                # Add the clauses as lists
                                clauses.append([not_x_ijdh, not_x_ikd1l])
                            if _k != j:
                                # Define the other propositions
                                not_x_kjd1l = -variables[_k,j,date_keys[d + 1],l]
                                # Add the clauses as lists
                                clauses.append([not_x_ijdh, not_x_kjd1l])            
    
    return clauses
