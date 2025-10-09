
import { api } from "@/lib/api";

export interface Cliente {
  id: number;
  nombre: string;
  apellido: string;
  email?: string;
  contacto?: number | string;
  direccion?: string;
}

export interface CrearCliente {
  id: number;
  nombre: string;
  apellido: string;
  email?: string;
  contacto?: number | string;
  direccion?: string;
}

export interface UpdateCliente extends Partial<CrearCliente> {}

export const ClientesAPI = {
  create: (data: CrearCliente) => api.post("/clientes", data),
  getAll: () => api.get<Cliente[]>("/clientes/todos"),
  getById: (id: number) => api.get<Cliente>(`/clientes/${id}`),
  update: (id: number, data: UpdateCliente) => api.put(`/clientes/${id}`, data),
  delete: (id: number) => api.delete(`/clientes/${id}`),
  search: (params?: {
    q?: string;
    sort?: "nombre" | "apellido";
    order?: "asc" | "desc";
    offset?: number;
    limit?: number;
  }) => api.get<Cliente[]>("/clientes", { params }),
};
