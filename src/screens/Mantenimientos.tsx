
import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { MantenimientosAPI, Mantenimiento, CrearMantenimiento } from "@/services/mantenimientos";

export default function Mantenimientos(){
  const qc = useQueryClient();
  const [search, setSearch] = useState("");
  const list = useQuery({
    queryKey:["mantenimientos", search],
    queryFn: ()=> (search? MantenimientosAPI.search({ q:search, order:"asc", offset:0, limit:50 }): MantenimientosAPI.getAll()).then(r=>r.data)
  });

  const [form, setForm] = useState<CrearMantenimiento>({ consecutivo_orden:0, tipo:"Preventivo", descripcion:"", apertura:new Date().toISOString(), precio:0 });

  const create = useMutation({
    mutationFn: (data: CrearMantenimiento)=> MantenimientosAPI.create(data),
    onSuccess: ()=>{ setForm({ consecutivo_orden:0, tipo:"Preventivo", descripcion:"", apertura:new Date().toISOString(), precio:0 }); qc.invalidateQueries({queryKey:["mantenimientos"]}) }
  });
  const remove = useMutation({
    mutationFn: (num:number)=> MantenimientosAPI.delete(num),
    onSuccess: ()=> qc.invalidateQueries({queryKey:["mantenimientos"]})
  });

  return (
    <section className="space-y-4">
      <div className="card"><h1 className="page">Mantenimientos</h1><p className="text-coffee-700">Búsqueda y CRUD</p></div>

      <div className="card flex gap-2">
        <input className="input flex-1" placeholder="Buscar por descripción" value={search} onChange={(e)=> setSearch(e.target.value)} />
        <button className="btn btn-ghost" onClick={()=> qc.invalidateQueries({queryKey:["mantenimientos", search]})}>Buscar</button>
      </div>

      <div className="card grid md:grid-cols-5 gap-2">
        <input className="input" placeholder="Consecutivo Orden" value={form.consecutivo_orden} onChange={(e)=> setForm({...form, consecutivo_orden:Number(e.target.value)})} />
        <input className="input" placeholder="Tipo" value={form.tipo||""} onChange={(e)=> setForm({...form, tipo:e.target.value})} />
        <input className="input" placeholder="Descripción" value={form.descripcion} onChange={(e)=> setForm({...form, descripcion:e.target.value})} />
        <input className="input" placeholder="Precio" value={form.precio||0} onChange={(e)=> setForm({...form, precio:Number(e.target.value)})} />
        <button className="btn btn-primary" onClick={()=> create.mutate(form)} disabled={!form.consecutivo_orden || !form.descripcion}>Crear</button>
      </div>

      <div className="card">
        {!list.data? <p>Cargando…</p> : (
          <table className="w-full text-left">
            <thead><tr><th>Número</th><th>Orden</th><th>Tipo</th><th>Descripción</th><th></th></tr></thead>
            <tbody>
              {list.data.map((m:Mantenimiento)=>(
                <tr key={m.numero} className="border-t">
                  <td>{m.numero}</td><td>{m.consecutivo_orden}</td><td>{m.tipo??"—"}</td><td>{m.descripcion}</td>
                  <td className="text-right"><button className="btn btn-ghost" onClick={()=> remove.mutate(m.numero)}>Eliminar</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
