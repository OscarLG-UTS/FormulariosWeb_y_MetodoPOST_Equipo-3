from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json

app = FastAPI(title = "FastAPI con Jinja2")
app.mount("/rutarecursos", StaticFiles(directory="recursos"), name="mirecurso")
miPlantilla = Jinja2Templates(directory="plantillas")

async def cargarJSON():
    with open('lista_alumnos.json',"r") as archivo_json:
        datos = json.load(archivo_json)
    return datos

async def guardarJSON(datosAgregar:List):
    with open('lista_alumnos.json',"w") as archivo_json:
        #json.dump(datosAgregar, archivo_json)
        json.dump(datosAgregar, archivo_json, indent=4)


@app.get("/inicio/", response_class=HTMLResponse)
async def read_item(request: Request):
    datos = await cargarJSON()
    return miPlantilla.TemplateResponse("index.html",{"request":request, "lista":datos})


@app.get("/lista", response_class=HTMLResponse)
async def iniciar(request: Request):
    datos = await cargarJSON()
    return miPlantilla.TemplateResponse("integrantes.html",{"request":request,"lista":datos})

#Método de agregación
@app.post("/agregar")
async def agregar(request:Request):
    datos = await cargarJSON()
    nuevos_datos = {}
    datos_formulario = await request.form()
    ultmimo_id = datos[-1].get("item_id")
    nuevos_datos["item_id"] = ultmimo_id+1
    nuevos_datos["matri"] = int(datos_formulario["f_matri"])
    nuevos_datos["nomb"] = datos_formulario["f_nomb"]
    nuevos_datos["pater"] = (datos_formulario["f_pater"])
    nuevos_datos["mater"] = (datos_formulario["f_mater"])
    nuevos_datos["edad"] = int(datos_formulario["f_edad"])
    nuevos_datos["mail"] = (datos_formulario["f_mail"])
    nuevos_datos["telef"] = int(datos_formulario["f_telef"])
    nuevos_datos["carr"] = (datos_formulario["f_carr"])
    print(nuevos_datos)
    datos.append(nuevos_datos)
    print(datos)

    await guardarJSON(datos)

    return RedirectResponse("/lista",303)


#Metodo de eliminación
@app.get("/eliminar/{id}")
async def eliminar(request:Request,id:int):
    datos = await cargarJSON()

    del datos[id]

    await guardarJSON(datos)

    return RedirectResponse("/lista",303)

#Método de modificación
@app.get("/modificar/{id}")
async def modificar(request:Request,id:int):
    datos = await cargarJSON()
    id1 = datos[id]
    id2 = id1['item_id']
    print (id2)
    return miPlantilla.TemplateResponse("actualizar.html",{"request":request,"lista":datos,"id":id2})


@app.post("/modificar_l/{id}")
async def modificar(request:Request,id:int):
    datos = await cargarJSON()
    #print (datos)
    #print (datos[id])
    datos[id]
    nuevos_datos = datos[id]
    datos_formulario = await request.form()
    nuevos_datos["matri"] = int(datos_formulario["f_matri"])
    nuevos_datos["nomb"] = datos_formulario["f_nomb"]
    nuevos_datos["pater"] = (datos_formulario["f_pater"])
    nuevos_datos["mater"] = (datos_formulario["f_mater"])
    nuevos_datos["edad"] = int(datos_formulario["f_edad"])
    nuevos_datos["mail"] = (datos_formulario["f_mail"])
    nuevos_datos["telef"] = int(datos_formulario["f_telef"])
    nuevos_datos["carr"] = (datos_formulario["f_carr"])
    datos[id] = nuevos_datos
    await guardarJSON(datos)
    return RedirectResponse("/lista",303)

@app.get("/datospersonales/{id}")
async def modificar(request:Request,id:int):
    datos = await cargarJSON()
    id1 = datos[id]
    id2 = id1['item_id']
    print (id2)
    return miPlantilla.TemplateResponse("datos.html",{"request":request,"lista":datos,"id":id2})