import { Layout, Menu, Typography } from "antd";
import {
  DashboardOutlined,
  CarOutlined,
  UserOutlined,
  TeamOutlined,
  ToolOutlined,
  FileTextOutlined,
  AuditOutlined,
} from "@ant-design/icons";
import { Link, Outlet, useLocation } from "react-router-dom";

const { Header, Sider, Content } = Layout;
const { Title } = Typography;

const MainLayout = () => {
  const location = useLocation();

  const menuItems = [
  {
    key: "/",
    icon: <DashboardOutlined />,
    label: ( <Link to="/"> Dashboard</Link>),
  },
  {
    key: "inventory-dashboard",
    icon: <DashboardOutlined />,
    label: (<Link to="inventory-dashboard"> Inventory Dashboard </Link>),
  },
  {
    key: "masterdata",
    icon: <TeamOutlined />,
    label: "Master Data",

    children: [

      {
        key: "/vehicles",
        label: (
          <Link to="/vehicles">
            Vehicles
          </Link>
        ),
      },

      {
        key: "/drivers",
        label: (
          <Link to="/drivers">
            Drivers
          </Link>
        ),
      },

      {
        key: "/employees",
        label: (
          <Link to="/employees">
            Employees
          </Link>
        ),
      },

      {
        key: "/parts",
        label: (
          <Link to="/parts">
            Parts
          </Link>
        ),
      },

      {
        key: "/checklists",
        label: (
          <Link to="/checklists">
            Checklists
          </Link>
        ),
      },
    ],
  },

  {
    key: "operations",
    icon: <ToolOutlined />,
    label: "Operations",

    children: [
      {
        key: "/complaints",
        label: (<Link to="/complaints">Complaints</Link>        ),
      },
      {
        key: "/inspections",
        label: (<Link to="/inspections">Inspections</Link>        ),
      },
      {
        key: "/jobcards",
        label: (<Link to="/jobcards">Job Cards</Link>        ),
      },
/*
        {
        key: "/jobcard-parts",
        label: (<Link to="/jobcardparts">Job Card Parts</Link>),
      },
*/
      {
        key: "/maintenance",
        label: (<Link to="/maintenance">Maintenance</Link>),
      },
    ],
  },

  {
    key: "inventory",
    icon: <FileTextOutlined />,
    label: "Inventory",
    children: [
      {
        key: "/opening-stock",
        label: (<Link to="/opening-stock">Opening Stock</Link>),
      },
      {
        key: "/requisitions",
        label: (<Link to="/requisitions">Part Requisitions</Link>        ),
      },
      {
        key: "/part-issues",
        label: (<Link to="/part-issues">Part Issues</Link>        ),
      },
      {
        key: "/part-returns",
        label: (<Link to="/part-returns">Part Returns</Link>),
      },
      {
        key: "/stock-ledger",
        label: (<Link to="/stock-ledger"> Stock Ledger</Link>),
      },
    ],
  },

  {
    key: "admin",
    icon: <AuditOutlined />,
    label: "Administration",

    children: [

      {
        key: "/audit-logs",
        label: ( <Link to="/audit-logs"> Audit Logs</Link>),
      },
    ],
  },
];

const openKeys = [];

if (
  location.pathname.includes(
    "part"
  ) ||
  location.pathname.includes(
    "requisition"
  ) ||
  location.pathname.includes(
    "stock"
  )
) {
  openKeys.push(
    "inventory"
  );
}

if (
  location.pathname.includes(
    "vehicle"
  ) ||
  location.pathname.includes(
    "driver"
  ) ||
  location.pathname.includes(
    "employee"
  ) ||
  location.pathname.includes(
    "part"
  ) ||
  location.pathname.includes(
    "checklist"
  )
) {
  openKeys.push(
    "masterdata"
  );
}
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider width={240}>
        <div
          style={{
            color: "#ffffff",
            padding: "18px",
            fontSize: "20px",
            fontWeight: "bold",
          }}
        >
          FMS MVP
        </div>

<Menu
  theme="dark"
  mode="inline"
  selectedKeys={[
    location.pathname,
  ]}
  defaultOpenKeys={
    openKeys
  }
  items={menuItems}
/>
      </Sider>

      <Layout>
        <Header
          style={{
            background: "#ffffff",
            borderBottom: "1px solid #eee",
            padding: "0 24px",
          }}
        >
          <Title level={4} style={{ marginTop: 14 }}>
            Fleet Management System
          </Title>
        </Header>

        <Content style={{ padding: 24 }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;