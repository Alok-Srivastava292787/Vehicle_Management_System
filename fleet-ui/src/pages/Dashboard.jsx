import { useEffect, useState } from "react";
import { Card, Col, Row, Spin, Typography } from "antd";

import { getVehicles } from "../services/vehicleService";
import { getDrivers } from "../services/driverService";
import { getEmployees } from "../services/employeeService";
import { getComplaints } from "../services/complaintService";

const { Title } = Typography;

const Dashboard = () => {
  const [loading, setLoading] = useState(false);

  const [counts, setCounts] = useState({
    vehicles: 0,
    drivers: 0,
    employees: 0,
    complaints: 0,
  });

  const loadDashboard = async () => {
    try {
      setLoading(true);

      const [vehicles, drivers, employees, complaints] = await Promise.all([
        getVehicles(),
        getDrivers(),
        getEmployees(),
        getComplaints(),
      ]);

      setCounts({
        vehicles: vehicles.length,
        drivers: drivers.length,
        employees: employees.length,
        complaints: complaints.length,
      });
    } catch (error) {
      console.error("Dashboard load failed:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) {
    return <Spin size="large" />;
  }

  return (
    <>
      <Title level={3}>Dashboard</Title>

      <Row gutter={16}>
        <Col span={6}>
          <Card title="Vehicles" bordered={false}>
            <Title level={2}>{counts.vehicles}</Title>
          </Card>
        </Col>

        <Col span={6}>
          <Card title="Drivers" bordered={false}>
            <Title level={2}>{counts.drivers}</Title>
          </Card>
        </Col>

        <Col span={6}>
          <Card title="Employees" bordered={false}>
            <Title level={2}>{counts.employees}</Title>
          </Card>
        </Col>

        <Col span={6}>
          <Card title="Complaints" bordered={false}>
            <Title level={2}>{counts.complaints}</Title>
          </Card>
        </Col>
      </Row>
    </>
  );
};

export default Dashboard;