import {
  useEffect,
  useState,
} from "react";

import {
  Button,
  Card,
  Form,
  Input,
  Modal,
  Popconfirm,
  Select,
  Space,
  Switch,
  Table,
  Tag,
  Typography,
  message,
} from "antd";

import {
  DeleteOutlined,
  EditOutlined,
} from "@ant-design/icons";

import {
  Link,
} from "react-router-dom";

import SearchToolbar from "../components/SearchToolbar";

import tablePagination from "../utils/tablePagination";


import {
    getPartIssues,
    createPartIssue,
    updatePartIssue,
    deactivatePartIssue,
} from "../services/partIssueService"
import {
  getPartRequisitions,
} from "../services/partRequisitionService";
import {
  getVehicles,
} from "../services/vehicleService";

import {
  getJobCards,
} from "../services/jobCardService";

import {
  getEmployees,
} from "../services/employeeService";

const { Title } = Typography;

const PartIssues = () => {

  const [loading,
    setLoading] =
    useState(false);

  const [issues,
    setIssues] =
    useState([]);

  const [vehicles,
    setVehicles] =
    useState([]);

  const [jobCards,
    setJobCards] =
    useState([]);

  const [employees,
    setEmployees] =
    useState([]);

  const [searchText,
    setSearchText] =
    useState("");

  const [statusFilter,
    setStatusFilter] =
    useState("ALL");

  const [modalOpen,
    setModalOpen] =
    useState(false);

  const [editingRecord,
    setEditingRecord] =
    useState(null);

  const [form] =
    Form.useForm();
  const [requisitions,
    setRequisitions] =
    useState([]);

  const loadData =
    async () => {

      try {

        setLoading(true);

          const [
            issueData,
            employeeData,
            requisitionData,
          ] = await Promise.all([
            getPartIssues(),
            getEmployees(),
            getPartRequisitions(),
          ]);

        setIssues(
          issueData
        );
        setEmployees(
          employeeData
        );
        setRequisitions(
          requisitionData
        );

      } catch (error) {

        console.error(
          error
        );

        message.error(
          "Failed to load issues"
        );

      } finally {

        setLoading(false);
      }
    };

  useEffect(() => {

    loadData();

  }, []);

  const openCreateModal =
    () => {

      setEditingRecord(
        null
      );

      form.resetFields();

      form.setFieldsValue({
        active_flag: true,
        status: "OPEN",
      });

      setModalOpen(true);
    };

  const openEditModal =
    (record) => {

      setEditingRecord(
        record
      );

      form.setFieldsValue(
        record
      );

      setModalOpen(true);
    };

  const handleSubmit =
    async () => {

      try {

        const values =
          await form.validateFields();

        if (
          editingRecord
        ) {

          await updatePartIssue(
            editingRecord.issue_id,
            values
          );

        } else {

          await createPartIssue(
            values
          );
        }

        message.success(
          "Issue saved successfully"
        );

        setModalOpen(false);

        await loadData();

      } catch (error) {

        console.error(
          error
        );

        message.error(
          "Operation failed"
        );
      }
    };

  const handleDeactivate =
    async (
      issueId
    ) => {

      try {

        await deactivatePartIssue(
          issueId
        );

        message.success(
          "Issue deactivated"
        );

        await loadData();

      } catch (error) {

        message.error(
          "Operation failed"
        );
      }
    };

  const vehicleMap =
    Object.fromEntries(
      vehicles.map(
        vehicle => [
          vehicle.vehicle_id,
          vehicle.rc_number,
        ]
      )
    );

  const employeeMap =
    Object.fromEntries(
      employees.map(
        employee => [
          employee.employee_id,
          employee.full_name,
        ]
      )
    );

  const filteredData =
    issues.filter(
      item => {

        const matchesSearch =
          item.issue_number
            ?.toLowerCase()
            .includes(
              searchText.toLowerCase()
            );

        const matchesStatus =
          statusFilter ===
            "ALL" ||
          (
            statusFilter ===
              "ACTIVE" &&
            item.active_flag
          ) ||
          (
            statusFilter ===
              "INACTIVE" &&
            !item.active_flag
          );

        return (
          matchesSearch &&
          matchesStatus
        );
      }
    );

  const columns = [

{
  title: "Issue No",
  dataIndex: "issue_number",
},

{
  title: "Requisition",
  dataIndex: "requisition_id",
},

{
  title: "Issued By",
      render:
        (_, record) =>
          employeeMap[
            record.issued_by_employee_id
          ] ?? "-",
},

{
  title: "Received By",
      render:
        (_, record) =>
          employeeMap[
            record.received_by_employee_id
          ] ?? "-",
},
    {
      title:
        "Status",

      dataIndex:
        "status",

      render:
        status => (
          <Tag color="blue">
            {status}
          </Tag>
        ),
    },
      {
        title: "Active",
        render: (_, record) => (
          <Tag
            color={
              record.active_flag
                ? "green"
                : "red"
            }
          >
            {
              record.active_flag
                ? "Active"
                : "Inactive"
            }
          </Tag>
        ),
      },

    {
      title:
        "Actions",

      render:
        (_, record) => (

          <Space>

            <Link
              to={`/part-issues/${record.issue_id}`}
            >
              <Button>
                View
              </Button>
            </Link>

            <Button
              icon={
                <EditOutlined />
              }
              onClick={() =>
                openEditModal(
                  record
                )
              }
            >
              Edit
            </Button>

            <Popconfirm
              title="Deactivate Issue?"
              onConfirm={() =>
                handleDeactivate(
                  record.issue_id
                )
              }
            >
              <Button
                danger
                icon={
                  <DeleteOutlined />
                }
              >
                Deactivate
              </Button>
            </Popconfirm>

          </Space>
        ),
    },

  ];

  return (
    <>

      <Title level={3}>
        Part Issues
      </Title>

      <SearchToolbar
        searchText={
          searchText
        }
        setSearchText={
          setSearchText
        }
        statusFilter={
          statusFilter
        }
        setStatusFilter={
          setStatusFilter
        }
        onRefresh={
          loadData
        }
        onAdd={
          openCreateModal
        }
        searchPlaceholder="Search Issue"
        addLabel="Add Issue"
      />

      <Card>

        <Table
          rowKey="issue_id"
          loading={loading}
          columns={columns}
          dataSource={
            filteredData
          }
          pagination={
            tablePagination
          }
        />

      </Card>

<Modal
  title={
    editingRecord
      ? "Edit Part Issue"
      : "Add Part Issue"
  }
  open={modalOpen}
  onOk={handleSubmit}
  onCancel={() =>
    setModalOpen(false)
  }
>
  <Form
    form={form}
    layout="vertical"
  >

<Form.Item
  name="requisition_id"
  label="Requisition"
  rules={[
    {
      required: true,
      message:
        "Requisition is required",
    },
  ]}
>
  <Select
    options={
      requisitions.map(
        req => ({
          value:
            req.requisition_id,
          label:
            req.requisition_number,
        })
      )
    }
  />
</Form.Item>
    <Form.Item
      name="issued_by_employee_id"
      label="Issued By"
    >
      <Select
        allowClear
        options={
          employees.map(
            emp => ({
              value:
                emp.employee_id,
              label:
                emp.full_name,
            })
          )
        }
      />
    </Form.Item>

    <Form.Item
      name="received_by_employee_id"
      label="Received By"
    >
      <Select
        allowClear
        options={
          employees.map(
            emp => ({
              value:
                emp.employee_id,
              label:
                emp.full_name,
            })
          )
        }
      />
    </Form.Item>

    <Form.Item
      name="status"
      label="Status"
    >
      <Select
        options={[
          {
            value:
              "OPEN",
            label:
              "OPEN",
          },
          {
            value:
              "ISSUED",
            label:
              "ISSUED",
          },
          {
            value:
              "PARTIAL",
            label:
              "PARTIAL",
          },
          {
            value:
              "CLOSED",
            label:
              "CLOSED",
          },
        ]}
      />
    </Form.Item>

    <Form.Item
      name="remarks"
      label="Remarks"
    >
      <Input.TextArea
        rows={4}
      />
    </Form.Item>

    <Form.Item
      name="active_flag"
      label="Active"
      valuePropName="checked"
    >
      <Switch />
    </Form.Item>

  </Form>
</Modal>
    </>
  );
};

export default PartIssues;