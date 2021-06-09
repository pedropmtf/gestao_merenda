import plotly.express as px
import pandas as pd
import json
import plotly


def createGraphs(alimentos):
        energia = 0
        proteina = 0
        lipideos = 0
        carboidratos = 0
        calcio = 0
        ferro = 0
        retinol = 0
        vitamina_c = 0
        sodio = 0
        for i in alimentos:
            energia += i.energia
            proteina += i.proteina
            lipideos += i.lipideos
            carboidratos += i.carboidratos
            calcio += i.calcio
            ferro += i.ferro
            retinol += i.retinol
            vitamina_c += i.vitamina_c
            sodio += i.sodio
        df = pd.DataFrame({"Nutrientes": ["proteina", "lipideos", "carboidratos"],
                            "Valores": [proteina, lipideos, carboidratos]
        })

        fig = px.pie(df, values="Valores", names="Nutrientes", title="Macronutrientes")
        graphJSON = json.dumps(fig, cls =plotly.utils.PlotlyJSONEncoder) 
        return graphJSON





""" 
df = pd.DataFrame({"Nutrientes": ["energia", "proteina", "lipideos", "carboidratos", "calcio", "ferro", "retinol", "vitamina_c", "sodio"],
                            "Valores": [energia, proteina, lipideos, carboidratos, calcio, ferro, retinol, vitamina_c, sodio]
        }) """