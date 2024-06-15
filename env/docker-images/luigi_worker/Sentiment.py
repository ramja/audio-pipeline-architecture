#!/usr/bin/python3 
import cohere 
from cohere import ClassifyExample
import sys

apiKey = "0PdK07VTWZio5GjPkU9GDi83YporLyIaX1HbbXrO"
co = cohere.Client(apiKey)

examples=[
  ClassifyExample(text="¡Estamos encantados de ayudarle a planificar sus vacaciones soñadas!", label="positive review"),
  ClassifyExample(text="Gracias por elegirnos, estamos seguros de que tendrá una experiencia maravillosa.", label="positive review"),
  ClassifyExample(text="Su satisfacción es nuestra prioridad, y estamos comprometidos a brindarle la mejor experiencia.", label="positive review"),
  ClassifyExample(text="Será un placer asistirte con cualquier consulta que tengas sobre tu próximo destino.", label="positive review"),
  ClassifyExample(text="Nos alegra saber que está considerando viajar con nosotros nuevamente.", label="positive review"),
  ClassifyExample(text="Lamentamos informarle que su vuelo ha sido cancelado.", label="negative review"),
  ClassifyExample(text="Desafortunadamente, no tenemos disponibilidad para las fechas solicitadas.", label="negative review"),
  ClassifyExample(text="Sentimos comunicarle que su reserva no pudo ser confirmada", label="negative review"),
  ClassifyExample(text="Quiero cancelar mi viaje", label="negative review"),
  ClassifyExample(text="Lamentamos que haya tenido una mala experiencia con nuestro servicio", label="negative review"),
  ClassifyExample(text="El vuelo partirá a las 8:00 a.m. del aeropuerto internacional.", label="neutral review"),
  ClassifyExample(text="Los documentos de viaje se enviarán por correo electrónico.", label="neutral review"),
  ClassifyExample(text="Le recordamos que el equipaje de mano tiene un límite de peso de 7 kg.", label="neutral review"),
  ClassifyExample(text="La tarifa incluye todos los impuestos y cargos aplicables.", label="neutral review"),
  ClassifyExample(text="Le informamos que el check-in se realiza a partir de las 3:00 p.m", label="neutral review")
]


for gFile in sys.argv[1:]:
    inputFile=f"/datalake/sen/{gFile}.sen"
    participants=[x.split(',')[0] for x in open(inputFile).readlines()]
    segments=[x.split(',')[2] for x in open(inputFile).readlines()]
    inputs=[x.split(',')[1] for x in open(inputFile).readlines()]
    t= len(inputs)
    l, r = divmod(t, 95) 
    with open(f"/datalake/clas/{gFile}.clas", "w+") as f:
       f.write('"Participant", "Prediction", "Confidence"\n')
    for i in range(l):
        b = 95*i
        e= b+95
        s = slice(b,e)

        response = co.classify(
            model='embed-multilingual-v3.0',
            inputs=inputs[b:e],
            examples=examples,
       )
        with open(f"/datalake/clas/{gFile}.clas", "w") as f:
            for i, result in enumerate(response.classifications):
                f.write(f"{participants[i]}, {result.prediction}, {result.confidence}, {segments[i]}\n")
    if r != 0:
        b = 95*l
        e= b+r
        s = slice(b,e)
        response = co.classify(
             model='embed-multilingual-v3.0',
             inputs=inputs[b:e],
             examples=examples,
           )
        with open(f"/datalake/clas/{gFile}.clas", "w") as f:
            for i, result in enumerate(response.classifications):
                f.write(f"{participants[i]}, {result.prediction}, {result.confidence}, {segments[i]}\n")

