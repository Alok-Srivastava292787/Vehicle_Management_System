
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
import {  getPartReturns,} from "../services/partReturnService";
import {
  createPartReturnDetail,
  updatePartReturnDetail,
  deactivatePartReturnDetail,
  getPartReturnDetails,
} from "../services/partReturnDetailService";
import {  getPartIssueDetails,} from "../services/partIssueDetailService";


import {  getEmployees,} from "../services/employeeService";

import {  getParts,} from "../services/partService";
import {SearchableSelect } from "../components/SearchableSelect";
const { Title } =
  Typography;

const PartReturnDetails =
  () => {

    const {
      returnId,
    } = useParams();

    const navigate =
      useNavigate();

    const [returnPart,
      setReturn] =
      useState(null);

    const [details,
      setDetails] =
      useState([]);

    const [employees,
      setEmployees] =
      useState([]);
    const [
      issueDetailParts,
      setIssueDetailParts,
    ] = useState([]);

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

    const loadData =
      async () => {

        try {

          const [
            returnData,
            detailData,
            employeeData,
            partData,
            issueDetailParts,
          ] =
            await Promise.all([
              getPartReturns(),
              getPartReturnDetails(),
              getEmployees(),
              getParts(),
              getPartIssueDetails(),
            ]);

          const currentReturn =
            returnData.find(
              item =>
                String(
                  item.return_id
                ) ===
                String(
                  returnId
                )
            );
          const issueDetails =
            await getPartIssueDetails();

          const allowedParts =
            issueDetails.filter(
              detail =>
                detail.issue_id ===
                  currentReturn.issue_id
                &&
                detail.active_flag===true
            );

          setIssueDetailParts(
            allowedParts
          );
          setReturn(
            currentReturn
          );

          setDetails(
            detailData.filter(
              item =>
                String(
                  item.return_id
                ) ===
                String(
                  returnId
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
            "Failed to load return details"
          );
        }
      };

    useEffect(() => {

      loadData();

    }, [returnId]);

    if (!returnPart)
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
    const issuePartOptions = [
      ...new Map(
        issueDetailParts.map(
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
          "Qty Returnd",
        dataIndex:
          "quantity_returned",
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

                await deactivatePartReturnDetail(
                  record.return_detail_id
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
                Deactivate
              </Button>

            </Popconfirm>

          </Space>

        ),
      }
    ];

    const handleSubmit =
      async () => {

        try {

          const values =
            await form.validateFields();

          values.return_id =
            Number(
              returnId
            );

          if (
            editingRecord
          ) {

            await updatePartReturnDetail(
              editingRecord.return_detail_id,
              values
            );

          } else {

            await createPartReturnDetail(
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
                  "/part-returns"
                )
              }
            >
              Back
            </Button>
            <Button
              type="primary"
              onClick={() =>
                window.open(
                  `${API_BASE_URL}/return_print/${returnPart.return_id}/pdf`,
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
            Part Return Details
          </Title>

          <Descriptions
            bordered
            column={2}
          >

            <Descriptions.Item
              label="Return Number"
            >
              {
                returnPart.return_number
              }
            </Descriptions.Item>

            <Descriptions.Item
              label="Status"
            >
              {
                returnPart.status
              }
            </Descriptions.Item>

            <Descriptions.Item
              label="Returnd By"
            >
              {
                employeeMap[
                  returnPart.returned_by_employee_id
                ]
              }
            </Descriptions.Item>

            <Descriptions.Item
              label="Received By"
            >
              {
                employeeMap[
                  returnPart.received_by_employee_id
                ]
              }
            </Descriptions.Item>

            <Descriptions.Item
              label="Issue ID"
            >
              {
                returnPart.issue_id
              }
            </Descriptions.Item>

          </Descriptions>

        </Card>

        <Card>
<Button
  type="primary"
  onClick={() => {

    setEditingRecord(
      null
    );

    form.resetFields();

    form.setFieldsValue({
      return_id:
        Number(returnId),

      active_flag:
        true,
    });

    setModalOpen(
      true
    );
  }}
>
  Add Returned Part
</Button>
          <Title level={4}>
            Returnd Parts
          </Title>

          <Table
            rowKey="return_detail_id"
            columns={columns}
            dataSource={details}
            pagination={false}
          />

        </Card>
<Modal
  title={
    editingRecord
      ? "Edit Return Detail"
      : "Add Return Detail"
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
    issuePartOptions
  }
/>
    </Form.Item>

    <Form.Item
      name="quantity_returned"
      label="Quantity Returned"
      rules={[
        {
          required: true,
        },
      ]}
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
      </Space>
    );
  };

export default PartReturnDetails;