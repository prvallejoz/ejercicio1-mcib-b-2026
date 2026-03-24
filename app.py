#API main code for exercise 1

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Modelo de datos
class Recibo(BaseModel):
    cliente: str
    monto: float

# Base de datos simulada
recibos = [
    {"id": 1, "cliente": "Carlos", "monto": 100, "pagado": True},
    {"id": 2, "cliente": "Ana", "monto": 200, "pagado": False}
]

# GET: todos los recibos
@app.get("/recibos")
def obtener_recibos():
    return recibos

# GET: estado de un recibo
@app.get("/recibos/{id}")
def estado_recibo(id: int):
    for r in recibos:
        if r["id"] == id:
            return {
                "id": r["id"],
                "cliente": r["cliente"],
                "estado": "Pagado" if r["pagado"] else "Pendiente"
            }
    raise HTTPException(status_code=404, detail="Recibo no encontrado")

# POST: crear recibo
@app.post("/recibos")
def crear_recibo(recibo: Recibo):
    nuevo = {
        "id": len(recibos) + 1,
        "cliente": recibo.cliente,
        "monto": recibo.monto,
        "pagado": False
    }
    recibos.append(nuevo)
    return nuevo

# PUT: pagar recibo
@app.put("/recibos/{id}/pagar")
def pagar_recibo(id: int):
    for r in recibos:
        if r["id"] == id:
            r["pagado"] = True
            return {"mensaje": "Recibo pagado", "recibo": r}
    raise HTTPException(status_code=404, detail="Recibo no encontrado")