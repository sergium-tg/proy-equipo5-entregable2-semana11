
import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import Dashboard from "./screens/Dashboard";
import Clientes from "./screens/Clientes";
import Tecnicos from "./screens/Tecnicos";
import Ordenes from "./screens/Ordenes";
import Mantenimientos from "./screens/Mantenimientos";
import MtoTecs from "./screens/MtoTecs";

export const router = createBrowserRouter([
  { path:"/", element:<App/>, children:[
    { index:true, element:<Dashboard/> },
    { path:"clientes", element:<Clientes/> },
    { path:"tecnicos", element:<Tecnicos/> },
    { path:"ordenes", element:<Ordenes/> },
    { path:"mantenimientos", element:<Mantenimientos/> },
    { path:"relaciones", element:<MtoTecs/> },
  ]}
]);
