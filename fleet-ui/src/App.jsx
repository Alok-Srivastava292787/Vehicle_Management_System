import { Routes, Route } from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Dashboard from "./pages/Dashboard";
import Vehicles from "./pages/Vehicles";
import Drivers from "./pages/Drivers";
import Employees from "./pages/Employees";
import Complaints from "./pages/Complaints";
import Maintenance from "./pages/Maintenance";
import Inspections from "./pages/Inspections";
{/* import JobCardParts from "./pages/JobCardParts"; */}
import Parts from "./pages/Parts";
import Checklists from "./pages/Checklists";
import AuditLogs  from "./pages/AuditLogs";
import JobCards from "./pages/JobCards";
import JobCardDetail from "./pages/JobCardDetail";
import PartRequisitions from "./pages/PartRequisitions";
import PartRequisitionDetails from "./pages/PartRequisitionDetails";
import PartIssues from "./pages/PartIssues"
import PartIssueDetails from "./pages/PartIssuesDetails"
import PartReturns from "./pages/PartReturns";
import PartReturnDetails from "./pages/PartReturnDetails";
import StockLedger  from "./pages/StockLedger";
import OpeningStock  from "./pages/OpeningStock";
import InventoryDashboard  from "./pages/InventoryDashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";


const App = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />}/>
      <Route path="/" element={<ProtectedRoute> <MainLayout /></ProtectedRoute> }>
        <Route index element={<ProtectedRoute> <Dashboard /></ProtectedRoute> } />
        <Route path="jobcards" element={<ProtectedRoute> <JobCards /></ProtectedRoute> }/>
        <Route path="/jobcards" element={<ProtectedRoute> <JobCards /> </ProtectedRoute> }/>
        <Route path="jobcards/:jobCardId" element={<ProtectedRoute> <JobCardDetail /></ProtectedRoute> }/>
        <Route path="vehicles" element={<ProtectedRoute> <Vehicles /></ProtectedRoute> } />
        <Route path="drivers" element={<ProtectedRoute> <Drivers /></ProtectedRoute> } />
        <Route path="employees" element={<ProtectedRoute> <Employees /></ProtectedRoute> } />
        <Route path="complaints" element={<ProtectedRoute> <Complaints /></ProtectedRoute> } />
        <Route path="maintenance" element={<ProtectedRoute> <Maintenance /></ProtectedRoute> } />
        <Route path="inspections" element={<ProtectedRoute> <Inspections /></ProtectedRoute> }/>
{/*         <Route path="jobcardparts" element={<JobCardParts />}/> */}
        <Route path="parts" element={<ProtectedRoute> <Parts /></ProtectedRoute> }/>
        <Route path="checklists" element={<ProtectedRoute> <Checklists /></ProtectedRoute> }/>
        <Route path="audit-logs" element={<ProtectedRoute> <AuditLogs /></ProtectedRoute> }/>
        <Route path="requisitions" element={<ProtectedRoute> <PartRequisitions /></ProtectedRoute> }/>
        <Route path="requisitions/:requisitionId"  element={<ProtectedRoute> <PartRequisitionDetails /></ProtectedRoute> }/>
        <Route path="part-issues" element={<ProtectedRoute> <PartIssues /></ProtectedRoute> }/>
        <Route path="part-issues/:issueId" element={<ProtectedRoute> <PartIssueDetails /></ProtectedRoute> }/>
        <Route path="issues/create" element={<ProtectedRoute> <PartIssueDetails /></ProtectedRoute> }/>
        <Route path="part-returns" element={<ProtectedRoute> <PartReturns /></ProtectedRoute> }/>
        <Route path="part-returns/:returnId" element={<ProtectedRoute> <PartReturnDetails /></ProtectedRoute> }/>
        <Route path="stock-ledger" element={<ProtectedRoute> <StockLedger /></ProtectedRoute> }/>
        <Route path="opening-stock" element={<ProtectedRoute> <OpeningStock /></ProtectedRoute> }/>
        <Route path="inventory-dashboard" element={<ProtectedRoute> <InventoryDashboard /></ProtectedRoute> }/>
      </Route>
    </Routes>
  );
};

export default App;