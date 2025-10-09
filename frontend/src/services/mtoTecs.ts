
import { api } from "@/lib/api";

export interface MtoTecnico {
  numero_mto: number;
  id_tecnico: number;
  rol?: string;
}

export interface CrearMtoTecnico {
  numero_mto: number;
  id_tecnico: number;
  rol?: string;
}

export interface UpdateMtoTecnico extends Partial<CrearMtoTecnico> {}

export const MtoTecsAPI = {
  create: (data: CrearMtoTecnico) => api.post("/mtosTecs", data),
  getAll: () => api.get("/mtosTecs/todos"),
  getByMantenimiento: (numero_mto: number) => api.get(`/mtosTecs/${numero_mto}`),
  update: (numero_mto: number, id_tecnico: number, data: UpdateMtoTecnico) => api.put(`/mtosTecs/${numero_mto}/${id_tecnico}`, data),
  delete: (numero_mto: number, id_tecnico: number) => api.delete(`/mtosTecs/${numero_mto}/${id_tecnico}`),
};
