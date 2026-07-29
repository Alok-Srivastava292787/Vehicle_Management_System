
import {
  useEffect,
  useState,
} from "react";

import {
  Button,
  Card,
  Descriptions,
  Row,
  Space,
  Table,
  Typography,
  message,
  Modal,
  Form,
  Input,
  InputNumber,
  Popconfirm,
  Select,
  Switch,
  Tag,
} from "antd";
import {
  useNavigate,
  useParams,
} from "react-router-dom";

import {  API_BASE_URL,} from "../utils/config";
import {  getPartIssues,} from "../services/partIssueService";

import {
  createPartIssueDetail,
  updatePartIssueDetail,
  deactivatePartIssueDetail,
} from "../services/partIssueDetailService";
import {  getPartIssueDetails,} from "../services/partIssueDetailService";
import {  getEmployees,} from "../services/employeeService";
import {  getPartRequisitionDetails,} from "../services/partRequisitionDetailService";

import {  getParts,} from "../services/partService";

const { Title } =
  Typography;

const PartIssueDetails =
  () => {

    const {
      issueId,
    } = useParams();

    const navigate =
      useNavigate();

    const [issue,
      setIssue] =
      useState(null);

    const [details,
      setDetails] =
      useState([]);

    const [employees,
      setEmployees] =
      useState([]);

    const [parts,
      setParts] =
      useState([]);
    
    const [
      requisitionDetailParts,
      setRequisitionDetailParts,
    ] = useState([]);

    const [modalOpen,
      setModalOpen] =
      useState(false);

    const [editingRecord,
      setEditingRecord] =
      useState(null);

    const [form] =
      Form.useForm();

    const loadData =
      async () => {

        try {

          const [
            issueData,
            detailData,
            employeeData,
            partData,
          ] =
            await Promise.all([
              getPartIssues(),
              getPartIssueDetails(),
              getEmployees(),
              getParts(),
            ]);

          const currentIssue =
            issueData.find(
              item =>
                String(
                  item.issue_id
                ) ===
                String(
                  issueId
                )
            );
          const requisitionDetails =
            await getPartRequisitionDetails();

          const allowedParts =
            requisitionDetails.filter(
              detail =>
                detail.requisition_id ===
                  currentIssue.requisition_id
                &&
                detail.active_flag
            );

          setRequisitionDetailParts(
            allowedParts
          );

          setIssue(
            currentIssue
          );

          setDetails(
            detailData.filter(
              item =>
                String(
                  item.issue_id
                ) ===
                String(
                  issueId
                )
            )
          );

          setEmployees(
            employeeData
          );

          setParts(
            partData
          );

        } catch {

          message.error(
            "Failed to load issue details"
          );
        }
      };

    useEffect(() => {

      loadData();

    }, [issueId]);

    if (!issue)
      return null;

    const employeeMap =
      Object.fromEntries(
        employees.map(
          emp => [
            emp.employee_id,
            emp.full_name,
          ]
        )
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
          (_, record) =>
            partMap[
              record.part_id
            ] ?? "-",
      },

      {
        title:
          "Qty Issued",
        dataIndex:
          "quantity_issued",
      },

      {
        title:
          "Serial Number",
        dataIndex:
          "serial_number",
      },

      {
        title:
          "Remarks",
        dataIndex:
          "remarks",
      },
      {
        title: "Status",
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
        title: "Actions",
        render: (_, record) => (
          <Space>
            <Button
              onClick={() => {
                setEditingRecord(
                  record
                );
                form.resetFields();
                form.setFieldsValue(
                  record
                );
                setModalOpen(
                  true
                );
              }}
            >
              Edit
            </Button>
            <Popconfirm
              title="Deactivate Detail?"
              onConfirm={async () => {
                await deactivatePartIssueDetail(
                  record.issue_detail_id
                );
                message.success(
                  "Detail deactivated"
                );
                await loadData();
              }}
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
      },

    ];
const handleSubmit =
  async () => {

    try {

      const values =
        await form.validateFields();

      values.issue_id =
        Number(issueId);

      if (
        editingRecord
      ) {

        await updatePartIssueDetail(
          editingRecord.issue_detail_id,
          values
        );

      } else {

        await createPartIssueDetail(
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

      await loadData();

    } catch (
      error
    ) {

      message.error(
        error?.response?.data?.detail
        || "Operation failed"
      );
    }
  };

  const requisitionPartOptions = [
      ...new Map(
        requisitionDetailParts.map(
          detail => [
            detail.part_id,
            {
              value:
                detail.part_id,
              label:
                partMap[
                  detail.part_id
                ] ??
                `Part ${detail.part_id}`,
            },
          ]
        )
      ).values(),
    ];

    return (

      <Space
        direction="vertical"
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
                  "/part-issues"
                )
              }
            >
              Back
            </Button>
            <Button
              type="primary"
              onClick={() =>
                window.open(
                  `${API_BASE_URL}/issue_print/${issue.issue_id}/pdf`,
                  "_blank"
                )
              }
            >
              Download PDF
            </Button>
          </Row>
          <Title level={2}
            style={{
              textAlign:
                "center",
            }}
          >
            Part Issue Details
          </Title>

          <Descriptions
            bordered
            column={2}
          >

            <Descriptions.Item
              label="Issue Number"
            >
              {
                issue.issue_number
              }
            </Descriptions.Item>

            <Descriptions.Item
              label="Status"
            >
              {
                issue.status
              }
            </Descriptions.Item>

            <Descriptions.Item
              label="Issued By"
            >
              {
                employeeMap[
                  issue.issued_by_employee_id
                ]
              }
            </Descriptions.Item>

            <Descriptions.Item
              label="Received By"
            >
              {
                employeeMap[
                  issue.received_by_employee_id
                ]
              }
            </Descriptions.Item>

            <Descriptions.Item
              label="Requisition"
            >
              {
                issue.requisition_id
              }
            </Descriptions.Item>

          </Descriptions>
        </Card>

        <Card>
          <Title level={4}>
            Issued Parts
          </Title>
<Button
  type="primary"

  onClick={() => {

    setEditingRecord(
      null
    );

    form.resetFields();

    form.setFieldsValue({
      issue_id:
        Number(issueId),

      active_flag:
        true,
    });

    setModalOpen(
      true
    );
  }}
>
  Add Issued Part
</Button>

          <Table
            rowKey="issue_detail_id"
            columns={columns}
            dataSource={details}
            pagination={false}
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
>
<Select
  options={
    requisitionPartOptions
  }
/></Form.Item>

<Form.Item
  name="quantity_issued"
  label="Quantity Issued"
>
  <InputNumber
    min={0}
    style={{
      width: "100%",
    }}
  />
</Form.Item>

<Form.Item
  name="serial_number"
  label="Serial Number"
>
  <Input />
</Form.Item>

<Form.Item
  name="remarks"
  label="Remarks"
>
  <Input.TextArea />
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
      </Space>
    );
  };

export default PartIssueDetails;