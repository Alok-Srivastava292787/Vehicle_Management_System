import { Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Dashboard from "./pages/Dashboard";
import Vehicles from "./pages/Vehicles";
import Drivers from "./pages/Drivers";
import Employees from "./pages/Employees";
import Complaints from "./pages/Complaints";
import Maintenance from "./pages/Maintenance";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="vehicles" element={<Vehicles />} />
        <Route path="drivers" element={<Drivers />} />
        <Route path="employees" element={<Employees />} />
        <Route path="complaints" element={<Complaints />} />
        <Route path="maintenance" element={<Maintenance />} />
      </Route>
    </Routes>
  );
};

export default App;