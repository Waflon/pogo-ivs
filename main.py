import os
import time
import requests 
import pandas as pd
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('SID')
auth_token = os.getenv('TOKEN')
twilio_numero = os.getenv('TWILIO_NUMERO')
mi_numero = os.getenv('MI_NUMERO')
client = Client(account_sid, auth_token)

url = "https://moonani.com/PokeList/index.php"

lista = []
coor_nunoa = {
    'norte': -33.44,
    'sur': -33.47,
    'oeste': -70.63,
    'este': -70.57
}


def main():
    #obtener tabla
    respuesta = requests.get(url).content
    tables = pd.read_html(respuesta)

    #obtener pokemon, coordinada
    keys = tables[0].Name.to_list()
    values = tables[0].Coords.to_list()
        
    tuples = [(key, value) for i, (key, value) in enumerate(zip(keys, values))]    
    data = dict(tuples)

    pokemones=list(data.keys())
    coordenadas=list(data.values())

    #coor_nunoa = { #temporales que sirven casi siempre
    #    'norte': 24,
    #    'sur': 26,
    #    'oeste': 120,
    #    'este': 122
    #}

    for i, coor in enumerate(coordenadas):
        y, x = coor.split(',')
        y = float(y)
        x = float(x)

        # verificar si está en los rangos de ñuñoa
        if (float(coor_nunoa['norte']) < y and float(coor_nunoa['sur']) > y ):
            if (float(coor_nunoa['oeste']) < x and float(coor_nunoa['este']) > x ):
                # enviar mensaje con las coordenadas en caso de coincidencia
                message = client.messages.create(
                    from_ = twilio_numero,
                    body  = f"{pokemones[i]} | Coordenadas: {y}-{x}",
                    to    = mi_numero
                )
                print('mensaje enviado con exito')
                #break descomentar para las pruebas 
        
if __name__ == "__main__":
    main()