import heapq

# =====================================================
# DATOS BASE
# =====================================================

tipos_rueda = ["T", "H", "V", "W"]


# =====================================================
# HEURISTICA
# =====================================================

def heuristica(tipos_restantes, empresas_restantes, costos):

    return sum(
        min(costos[empresa][tipo] for empresa in empresas_restantes)
        for tipo in tipos_restantes
    )


# =====================================================
# ALGORITMO A*
# =====================================================

def a_estrella(costos):

    empresas = list(costos.keys())

    abiertos = []

    contador = 0

    pasos = []

    estado_inicial = (
        0,          # f(n)
        contador,   # contador
        0,          # g(n)
        {},         # asignaciones
        set(),      # empresas usadas
        0           # nivel
    )

    heapq.heappush(abiertos, estado_inicial)

    while abiertos:

        (
            f_actual,
            _,
            g_actual,
            asignaciones,
            usadas,
            nivel
        ) = heapq.heappop(abiertos)

        tipos_restantes = tipos_rueda[nivel:]

        empresas_restantes = [
            e for e in empresas if e not in usadas
        ]

        h_actual = heuristica(
            tipos_restantes,
            empresas_restantes,
            costos
        )

        # =================================================
        # GUARDAR PASO
        # =================================================

        pasos.append({
            "asignaciones": asignaciones.copy(),
            "g": g_actual,
            "h": h_actual,
            "f": g_actual + h_actual,
            "nivel": nivel
        })

        # =================================================
        # SOLUCION
        # =================================================

        if nivel == len(tipos_rueda):

            return {
                "solucion": asignaciones,
                "costo_total": g_actual,
                "pasos": pasos
            }

        # =================================================
        # EXPANDIR NODOS
        # =================================================

        tipo_actual = tipos_rueda[nivel]

        for empresa in empresas:

            if empresa not in usadas:

                costo_rueda = costos[empresa][tipo_actual]

                nuevo_g = g_actual + costo_rueda

                nuevas_asignaciones = asignaciones.copy()
                nuevas_asignaciones[tipo_actual] = empresa

                nuevas_usadas = usadas.copy()
                nuevas_usadas.add(empresa)

                nuevos_tipos_restantes = tipos_rueda[nivel + 1:]

                nuevas_empresas_restantes = [
                    e for e in empresas
                    if e not in nuevas_usadas
                ]

                nuevo_h = heuristica(
                    nuevos_tipos_restantes,
                    nuevas_empresas_restantes,
                    costos
                )

                nuevo_f = nuevo_g + nuevo_h

                contador += 1

                heapq.heappush(
                    abiertos,
                    (
                        nuevo_f,
                        contador,
                        nuevo_g,
                        nuevas_asignaciones,
                        nuevas_usadas,
                        nivel + 1
                    )
                )

    return None
