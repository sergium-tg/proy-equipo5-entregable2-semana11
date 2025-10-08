
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { OrdenesAPI, CrearOrden, Orden } from "@/services/ordenes";

export default function Ordenes(){
  const qc = useQueryClient();
  const list = useQuery({ queryKey:["ordenes"], queryFn: ()=> OrdenesAPI.getAll().then(r=>r.data) });
  const [form, setForm] = useState<CrearOrden>({ id_cliente:0, tipo:"Mantenimiento", descripcion:"", fecha:new Date().toISOString() });

  const create = useMutation({
    mutationFn: (data: CrearOrden)=> OrdenesAPI.create(data),
    onSuccess: ()=>{ setForm({ id_cliente:0, tipo:"Mantenimiento", descripcion:"", fecha:new Date().toISOString() }); qc.invalidateQueries({queryKey:["ordenes"]}) }
  });
  const remove = useMutation({
    mutationFn: (consecutivo:number)=> OrdenesAPI.delete(consecutivo),
    onSuccess: ()=> qc.invalidateQueries({queryKey:["ordenes"]})
  });

  return (
    <section className="space-y-4">
      <div className="card"><h1 className="page">Órdenes</h1><p className="text-coffee-700">Listado y creación</p></div>

      <div className="card grid md:grid-cols-4 gap-2">
        <input className="input" placeholder="ID Cliente" value={form.id_cliente} onChange={(e)=>setForm({...form, id_cliente:Number(e.target.value)})} />
        <input className="input" placeholder="Tipo" value={form.tipo||""} onChange={(e)=>setForm({...form, tipo:e.target.value})} />
        <input className="input" placeholder="Descripción" value={form.descripcion||""} onChange={(e)=>setForm({...form, descripcion:e.target.value})} />
        <button className="btn btn-primary" onClick={()=> create.mutate(form)} disabled={!form.id_cliente}>Crear</button>
      </div>

      <div className="card">
        {!list.data? <p>Cargando…</p> : (
          <table className="w-full text-left">
            <thead><tr><th>Consecutivo</th><th>Cliente</th><th>Tipo</th><th>Descripción</th><th></th></tr></thead>
            <tbody>
              {list.data.map((o:Orden)=>(
                <tr key={o.consecutivo} className="border-t">
                  <td>{o.consecutivo}</td><td>{o.id_cliente}</td><td>{o.tipo??"—"}</td><td>{o.descripcion??"—"}</td>
                  <td className="text-right"><button className="btn btn-ghost" onClick={()=> remove.mutate(o.consecutivo)}>Eliminar</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
