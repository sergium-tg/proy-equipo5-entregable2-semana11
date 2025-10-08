
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { ClientesAPI, Cliente, CrearCliente, UpdateCliente } from "@/services/clientes";

export default function Clientes(){
  const qc = useQueryClient();
  const [search, setSearch] = useState("");
  const [form, setForm] = useState<CrearCliente>({ id: 0, nombre:"", apellido:"", email:"", contacto:"", direccion:"" });

  const list = useQuery({
    queryKey:["clientes", search],
    queryFn: ()=> ClientesAPI.search(search?{q:search, sort:"apellido", order:"asc", offset:0, limit:50}:undefined).then(r=>r.data)
  });

  const create = useMutation({
    mutationFn: (data: CrearCliente)=> ClientesAPI.create(data),
    onSuccess: ()=>{ setForm({ id:0, nombre:"", apellido:"", email:"", contacto:"", direccion:""}); qc.invalidateQueries({queryKey:["clientes"]}); }
  });

  const remove = useMutation({
    mutationFn: (id:number)=> ClientesAPI.delete(id),
    onSuccess: ()=> qc.invalidateQueries({queryKey:["clientes"]})
  });

  return (
    <section className="space-y-4">
      <div className="card"><h1 className="page">Clientes</h1><p className="text-coffee-700">Buscar y gestionar clientes</p></div>

      <div className="card flex gap-2">
        <input className="input flex-1" placeholder="Buscar por nombre o apellido" value={search} onChange={(e)=>setSearch(e.target.value)} />
        <button className="btn btn-ghost" onClick={()=> qc.invalidateQueries({queryKey:["clientes", search]})}>Buscar</button>
      </div>

      <div className="card grid md:grid-cols-5 gap-2">
        <input className="input" placeholder="ID" value={form.id} onChange={(e)=>setForm({...form, id: Number(e.target.value)})} />
        <input className="input" placeholder="Nombre" value={form.nombre} onChange={(e)=>setForm({...form, nombre:e.target.value})} />
        <input className="input" placeholder="Apellido" value={form.apellido} onChange={(e)=>setForm({...form, apellido:e.target.value})} />
        <input className="input" placeholder="Email" value={form.email||""} onChange={(e)=>setForm({...form, email:e.target.value})} />
        <div className="flex gap-2">
          <button className="btn btn-primary w-full" onClick={()=> create.mutate(form)} disabled={!form.id || !form.nombre || !form.apellido}>Crear</button>
        </div>
      </div>

      <div className="card">
        {!list.data? <p>Cargando…</p> : (
          <table className="w-full text-left">
            <thead><tr><th>ID</th><th>Nombre</th><th>Email</th><th></th></tr></thead>
            <tbody>
              {list.data.map((c:Cliente)=>(
                <tr key={c.id} className="border-t">
                  <td>{c.id}</td>
                  <td>{c.nombre} {c.apellido}</td>
                  <td>{c.email??"—"}</td>
                  <td className="text-right"><button className="btn btn-ghost" onClick={()=> remove.mutate(c.id)}>Eliminar</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
