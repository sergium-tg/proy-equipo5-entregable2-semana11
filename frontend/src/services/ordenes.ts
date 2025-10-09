
import { api } from "@/lib/api";

export interface Orden {
  consecutivo: number;
  id_cliente: number;
  tipo?: string;
  descripcion?: string;
  fecha?: string;
  mantenimientos?: any[];
}

export interface CrearOrden {
  id_cliente: number;
  tipo?: string;
  descripcion?: string;
  fecha?: string;
}

export interface UpdateOrden extends Partial<CrearOrden> {}

export const OrdenesAPI = {
  create: (data: CrearOrden) => api.post("/ordenes", data),
  getById: (consecutivo: number) => api.get<Orden>(`/ordenes/${consecutivo}`),
  getAll: () => api.get<Orden[]>("/ordenes/todos"),
  update: (consecutivo: number, data: UpdateOrden) => api.put(`/ordenes/${consecutivo}`, data),
  delete: (consecutivo: number) => api.delete(`/ordenes/${consecutivo}`),
};
