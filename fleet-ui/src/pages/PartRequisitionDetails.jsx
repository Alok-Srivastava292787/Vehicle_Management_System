import { useEffect, useState } from "react";

import {
  Button,
  Card,
  Descriptions,
  Form,
  Input,
  InputNumber,
  message,
  Modal,
  Popconfirm,
  Row,
  Select,
  Space,
  Spin,
  Steps,
  Switch,
  Table,
  Tag,
  Typography,
} from "antd";

import {  data, useNavigate,  useParams,} from "react-router-dom";
import dayjs from "dayjs";
import {  getPartRequisitions, submitRequest, approveRequest,} from "../services/partRequisitionService";
import {  getPartRequisitionDetails,} from "../services/partRequisitionDetailService";
import {  getVehicles,} from "../services/vehicleService";
import {  getEmployees,} from "../services/employeeService";
import {  getParts,} from "../services/partService";
import {  API_BASE_URL,} from "../utils/config";
import {SearchableSelect } from "../components/SearchableSelect";
import {
  createPartRequisitionDetail,
  updatePartRequisitionDetail,
  deactivatePartRequisitionDetail,
} from "../services/partRequisitionDetailService";
import {createIssueFromRequisition} from "../services/partIssueService"

const { Title } =
  Typography;

const PartRequisitionDetails =
  () => {
    const {
      requisitionId,
    } = useParams();
    const navigate =
      useNavigate();
    const [loading,
      setLoading] =
      useState(true);
    const [requisition,
      setRequisition] =
      useState(null);
    const [details,
      setDetails] =
      useState([]);
    const [vehicles,
      setVehicles] =
      useState([]);
    const [employees,
      setEmployees] =
      useState([]);
    const [parts,
      setParts] =
      useState([]);
    const [modalOpen,
      setModalOpen] =
      useState(false);
    const [editingRecord,
      setEditingRecord] =
      useState(null);
    const [form] =
      Form.useForm();

      const loadData = async () => {
        try {
          setLoading(
            true
          );
          const [
            requisitionData,
            detailData,
            vehicleData,
            employeeData,
            partData,
          ] =
            await Promise.all([
              getPartRequisitions(),
              getPartRequisitionDetails(),
              getVehicles(),
              getEmployees(),
              getParts(),
            ]);
          const current =
            requisitionData.find(
              item =>
                String(
                  item.requisition_id
                ) ===
                String(
                  requisitionId
                ) 
            );
          setRequisition(
            current
          );
          setDetails(
            detailData.filter(
              item =>
                String(
                  item.requisition_id
                ) ===
                String(
                  requisitionId 
                )
            )
          );
          setVehicles(
            vehicleData
          );
          setEmployees(
            employeeData
          );
          setParts(
            partData
          );
        } catch (
          error
        ) {
          console.error(
            error
          );
          message.error(
            "Failed to load requisition"
          );
        } finally {
          setLoading(
            false
          );
        }
      };

    useEffect(() => {  loadData();}, [requisitionId]);
    if (loading) {
      return (
        <div
          style={{
            textAlign:
              "center",
            marginTop:
              100,
          }}
        >
          <Spin
            size="large"
          />
        </div>
      );
    }
    if (
      !requisition
    ) {
      return (
        <Card>
          Requisition
          not found
        </Card>
      );
    }
    const getWorkflowStep =
      () => {

        switch (
          requisition.status
        ) {

          case "OPEN":
            return 0;

          case "APPROVED":
            return 1;

          case "ISSUED":
            return 2;

          case "CLOSED":
            return 3;

          default:
            return 0;
        }
      };
        const handleApproveRequest =
        async () => {
          try {
            await approveRequest(
              requisition.requisition_id
            );
            message.success(
              "Request approved"
            );
            loadData();
          } catch (error) {
            message.error(
              error?.response?.data?.detail
              ||
              "Operation failed"
            );
          }
        };
      const vehicle =
      vehicles.find(
        v =>
          v.vehicle_id ===
          requisition.vehicle_id
      );
    const technician =
      employees.find(
        e =>
          e.employee_id ===
          requisition.technician_id
      );
    const partMap =
      Object.fromEntries(
        parts.map(
          part => [
            part.part_id,
            part.part_name,
          ]
        )
      );
    const columns = [
      {
        title:
          "Part",
        render:
          (
            _,
            record
          ) =>
            partMap[
              record.part_id
            ] ?? "-",
      },
      {
        title:
          "Qty Required",

        dataIndex:
          "quantity_required",
      },
      {
        title:
          "Qty Returned",

        dataIndex:
          "quantity_returned",
      },
      {
        title:
          "Required Serial No",

        dataIndex:
          "required_serial_number",
      },
      {
        title:
          "Returned Serial No",

        dataIndex:
          "returned_serial_number",
      },
      {
        title:
          "Remarks",

        dataIndex:
          "remarks",
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

<Button
  onClick={() => {

    console.log("Edit Clicked");

    setEditingRecord(record);

    form.resetFields();

    form.setFieldsValue(record);

    setModalOpen(true);
  }}
>
  Edit
</Button>
        <Popconfirm
          title=
          "Deactivate Detail?"

          onConfirm={
            async () => {

              await deactivatePartRequisitionDetail(
                record.requisition_detail_id
              );

              message.success(
                "Detail deactivated"
              );

              await loadData();
            }
          }
        >

<Button
  danger
  disabled={
    !record.active_flag
  }
>
  Delete
</Button>
        </Popconfirm>

      </Space>
    ),
}    ];
    const handleSubmit =
      async () => {

        try {

          const values =
            await form.validateFields();

          values.requisition_id =
            Number(
              requisitionId
            );

          if (
            editingRecord
          ) {

            await updatePartRequisitionDetail(
              editingRecord.requisition_detail_id,
              values
            );

          } else {

            await createPartRequisitionDetail(
              values
            );
          }

          message.success(
            "Detail saved successfully"
          );

          setModalOpen(
            false
          );

          form.resetFields();

          loadData();

        } catch (
          error
        ) {

          message.error(
            error?.response?.data?.detail
            || "Operation failed"
          );
        }
      };
      const handleCreateIssue =
        async () => {
          try {
            const data =
              await createIssueFromRequisition(
                requisition.requisition_id
              );
            message.success(
              `Issue ${data.issue_number} created`
            );
    window.open(
      `/part-issues/${data.issue_id}`,
      "_blank"
    );
} catch (error) {

  console.error(
    "Create Issue Error",
    error
  );

  console.error(
    "Response",
    error?.response?.data
  );

  message.error(
    JSON.stringify(
      error?.response?.data
    )
  );
}        };

const handleViewIssue =
  () => {

    window.open(
      `/part-issues/${requisition.issue_id}`,
      "_blank"
    );

  };      const approved_by =
        employees.find(
          e =>
          e.employee_id ===
          (requisition.approved_by)
      );

    return (

      <Space
        direction="vertical"
        size="large"
        style={{
          width:
            "100%",
        }}
      >
        <Card>
          <Row
            justify="space-between"
            style={{
              marginBottom: 1,
            }}
          >
            <Button
              onClick={() =>
                navigate(
                  "/requisitions"
                )
              }
            >
              Back To Requisitions
            </Button>
{
  requisition.status ===
  "APPROVED" ? (

    <Button
      type="primary"
      onClick={
        handleCreateIssue
      }
    >
      Create Issue
    </Button>

  ) : requisition.status ===
      "ISSUE_CREATED" ? (

    <Button
      onClick={
        handleViewIssue
      }
    >
      View Issue
    </Button>

  ) : (

    ["DRAFT","OPEN","SUBMITTED"]
      .includes(
        requisition.status
      ) && (

      <Button
        type="primary"
        onClick={
          handleApproveRequest
        }
      >
        Approve
      </Button>
    )
  )
}            <Button
              type="primary"
              onClick={() =>
                window.open(
                  `${API_BASE_URL}/requisitions_print/${requisition.requisition_id}/pdf`,
                  "_blank"
                )
              }
            >
              Download PDF
            </Button>
          </Row>      
          <Title
            level={2}
            style={{
              textAlign:
                "center",
            }}
          >
            Part Requisition
          </Title>
          <Descriptions
            bordered
            column={2}
          >
            <Descriptions.Item
              label="Requisition No"
            >
              {
                requisition.requisition_number
              }
            </Descriptions.Item>
            <Descriptions.Item
              label="Status"
            >
              {
                requisition.status
              }
            </Descriptions.Item>
            <Descriptions.Item
              label="Vehicle"
            >
              {
                vehicle
                  ?.rc_number
              }
            </Descriptions.Item>
            <Descriptions.Item
              label="Job Card"
            >
              {
                requisition.job_card_id
              }
            </Descriptions.Item>
            <Descriptions.Item
              label="Technician"
            >
              {
                technician
                  ?.full_name
              }
            </Descriptions.Item>
            <Descriptions.Item
              label="Date"
            >
              {
                requisition.requisition_date
              }
            </Descriptions.Item>
            <Descriptions.Item
              label="Remarks"
              span={2}
            >
              {
                requisition.remarks
              }
            </Descriptions.Item>
          </Descriptions>
        </Card>
        <Card>
          <Card
            title="Requested Parts"
            extra={
              <Space>
                <Button
                     type="primary"
                  onClick={() => {
                    setEditingRecord(null);
                    form.resetFields();
                    form.setFieldsValue({
                      requisition_id:
                        Number(requisitionId),
                        active_flag: true,
                    });

                    setModalOpen(true);
                  }}
                >
                  Add Part
                </Button>
              </Space>
            }
        >

        </Card>
          <Table
            rowKey={
              "requisition_detail_id"
            }
            columns={
              columns
            }
            dataSource={
              details
            }
            pagination={
              false
            }
          />
        </Card>
<Modal
  title={
    editingRecord
      ? "Edit Part Detail"
      : "Add Part Detail"
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
      name="part_id"
      label="Part"
      rules={[
        {
          required: true,
          message:
            "Part is required",
        },
      ]}
    >

      <SearchableSelect
        options={
          parts.map(
            part => ({
              value:
                part.part_id,

              label:
                part.part_name,
            })
          )
        }
      />

    </Form.Item>

    <Form.Item
      name="quantity_required"
      label="Quantity Required"
    >

      <InputNumber
        min={0}
        style={{
          width: "100%",
        }}
      />

    </Form.Item>

    <Form.Item
      name="quantity_returned"
      label="Quantity Returned"
    >

      <InputNumber
        min={0}
        style={{
          width: "100%",
        }}
      />

    </Form.Item>

    <Form.Item
      name="required_serial_number"
      label="Required Serial Number"
    >

      <Input />

    </Form.Item>

    <Form.Item
      name="returned_serial_number"
      label="Returned Serial Number"
    >

      <Input />

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
  label="Active"
  name="active_flag"
  valuePropName="checked"
>
  <Switch />
</Form.Item>

  </Form>

</Modal>
<Card
  style={{
    borderTop:
      "4px solid #1677ff",
  }}
>
  <Title level={4}>
    Requisition Workflow
  </Title>
  <Steps
    current={
      getWorkflowStep()
    }
    items={[
      {
        title: "Open",
        description:"Resquested"
      },
      {
        title: "Approved",
     description: (
        <>
          <div>
            {
              approved_by?.full_name
              || "-"
            }
          </div>

          <div
            style={{
              color: "#888",
              fontSize: 12,
            }}
          >
            {
              requisition.approved_at
                ? dayjs(
                    requisition.approved_at
                  ).format(
                    "DD-MMM-YYYY HH:mm"
                  )
                : "-"
            }
          </div>
        </>
      ),
      },
      {
        title: "Issued",
        description:
          "Parts Issued",
      },
      {
        title: "Closed",
        description:
          "Completed",
      },
    ]}
  />
</Card>


      </Space>
    );
  };

export default
  PartRequisitionDetails;