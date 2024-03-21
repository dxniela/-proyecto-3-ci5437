from sympy import symbols, Not

# Constraint: Todos los participantes deben jugar dos veces con cada uno
# de los otros participantes, una como "visitantes" y la otra como "locales".
# (forall i,j | i!=j : (exists only one d,h |: X(i,j,d,h) )
def rule_1(participants, dates, hours):
    clauses = []
    for i in participants:
        for j in participants:
            if i == j:
                continue

            for d in dates:
                for h in hours:
                    # Define the proposition
                    x_ijdh = symbols(f'X({i},{j},{d},{h})')

                    # Add the proposition to the clauses
                    clauses.append(x_ijdh)
                    
    return clauses
                    
            
# Constraint: Dos juegos no pueden ocurrir al mismo tiempo.
# (forall i,j,d,h | i!=j : X(i,j,d,h) ⇒ not (exists n,m | (i!=n or j!=m) and n!=m : X(n,m,d,h))) and 
# (forall i,j,d,h | i!=j and h<H-2 : X(i,j,d,h)⇒ not (exists n,m | (i!=n or j!=m) and n!=m : X(n,m,d,h+1))) 
def rule_2(participants, dates, hours):
    clauses = []
    for i in participants:
        for j in participants:
            if i == j:
                continue

            for d in dates:
                for h in hours:
                    # Define the proposition
                    x_ijdh = symbols(f'X({i},{j},{d},{h})')

                    # Negate the proposition
                    not_x_ijdh = Not(x_ijdh)

                    for n in participants:
                        for m in participants:
                            if (i == n and j == m) or (n == m):
                                continue
                            
                            # Define the second proposition
                            x_nmdh = symbols(f'X({n},{m},{d},{h})')
                            not_x_nmdh = Not(x_nmdh)

                            # Add the clause as a list
                            clauses.append([not_x_ijdh, not_x_nmdh])

                            if h < len(hours) - 2:
                                # Define the third proposition
                                x_nmdh_plus_1 = symbols(f'X({n},{m},{d},{h + 1})')
                                not_x_nmdh_plus_1 = Not(x_nmdh_plus_1)

                                # Add the clause as a list
                                clauses.append([not_x_ijdh, not_x_nmdh_plus_1])
    
    return clauses

# Constraint: Un participante puede jugar a lo sumo una vez por día.
# (forall i,j,d,h | i!=j : X(i,j,d,h) => not(exists k,l | : X(i,k,d,l) or X(k,j,d,l) or X(j,k,d,l) or X(k,i,d,l)))
def rule_3(participants, dates, hours):
    clauses = []
    for i in participants:
        for j in participants:
            if i == j:
                continue

            for d in dates:
                for h in hours:
                    # Define the proposition
                    x_ijdh = symbols(f'X({i},{j},{d},{h})')

                    # Negate the proposition
                    not_x_ijdh = Not(x_ijdh)

                    for _k in participants:
                        for l in hours:
                            if l == h:
                                continue
                            
                            # Define the other propositions
                            not_x_ikdl = Not(symbols(f'X({i},{_k},{d},{l})'))
                            not_x_kjdl = Not(symbols(f'X({_k},{j},{d},{l})'))
                            not_x_jkdl = Not(symbols(f'X({j},{_k},{d},{l})'))
                            not_x_kidl = Not(symbols(f'X({_k},{i},{d},{l})'))

                            # Add the clauses as lists
                            clauses.append([not_x_ijdh, not_x_ikdl])
                            clauses.append([not_x_ijdh, not_x_kjdl])
                            clauses.append([not_x_ijdh, not_x_jkdl])
                            clauses.append([not_x_ijdh, not_x_kidl])
    
    return clauses

# Constraint: Un participante no puede jugar de "visitante" en dos días consecutivos,
# ni de "local" dos días seguidos.
# (forall i,j,d,h | i!=j  d<D-1 : X(i,j,d,h) => not(exists k,l | : X(i,k,d+1,l) or X(k,j,d+1,l)))
def rule_4(participants, dates, hours):
    clauses = []
    for i in participants:
        for j in participants:
            if i == j:
                continue

            for d in range(len(dates) - 1):  # Subtract 1 to avoid index out of range for d + 1
                for h in hours:
                    # Define the proposition
                    x_ijdh = symbols(f'X({i},{j},{dates[d]},{h})')

                    # Negate the proposition
                    not_x_ijdh = Not(x_ijdh)

                    for _k in participants:
                        for l in hours:
                            # Define the other propositions
                            not_x_ikd1l = Not(symbols(f'X({i},{_k},{dates[d + 1]},{l})'))
                            not_x_kjd1l = Not(symbols(f'X({_k},{j},{dates[d + 1]},{l})'))

                            # Add the clauses as lists
                            clauses.append([not_x_ijdh, not_x_ikd1l])
                            clauses.append([not_x_ijdh, not_x_kjd1l])
    
    return clauses