import { useEffect, useState } from "react";

import {
  Button,
  Card,
  Descriptions,
  Row,
  Space,
  Spin,
  Table,
  Tag,
  Typography,
  message,
  Modal,
  Form,
  Input,
  InputNumber,
  Popconfirm,
  Select,
  Steps,
  Switch,
} from "antd";

import {  useNavigate,useParams} from "react-router-dom";
import { 
  getJobCards,
  submitJobCard,
  verifyJobCard,
  approveJobCard,
} from "../services/jobCardService";
import { getVehicles } from "../services/vehicleService";
import { getDrivers } from "../services/driverService";
import { getEmployees } from "../services/employeeService";
import { getJobCardParts,createJobCardPart,updateJobCardPart, deactivateJobCardPart } from "../services/jobCardPartService";
import { getParts,createPart, updatePart }  from "../services/partService";
import { API_BASE_URL,} from "../utils/config";
import { generateRequisition,} from "../services/jobCardService";
import {updateJobCard,createJobCard} from "../services/jobCardDetailService";
import {SearchableSelect } from "../components/SearchableSelect";
import dayjs from "dayjs";

const { Title } = Typography;

const JobCardDetail = () => {

  const { jobCardId } =
    useParams();
  const { partId } = useParams();
  const [loading,
    setLoading] =
    useState(true);

  const [jobCard,
    setJobCard] =
    useState(null);
    const [editingRecord,
      setEditingRecord] =
      useState(null);
    const [modalOpen,
      setModalOpen] =
      useState(false);
    const [form] =
      Form.useForm();

  const [vehicles,
    setVehicles] =
    useState([]);
  const [
    totalAmount,
    setTotalAmount,
  ] = useState(0);

  const [drivers,
    setDrivers] =
    useState([]);

  const [employees,
    setEmployees] =
    useState([]);

  const [parts,
    setParts] =
    useState([]);

  const [partMaster,
    setPartMaster] =
    useState([]);  
  const navigate =
    useNavigate();
const [
  partModalOpen,
  setPartModalOpen,
  ] = useState(false);
const openAddPartModal =
  () => {
    setPartModalOpen(true);
  };
  const getStatusColor =
    (status) => {

      switch (status) {      
        case "OPEN":
          return "blue";
        case "IN_PROGRESS":
          return "orange";
        case "WAITING_PARTS":
          return "gold";
        case "COMPLETED":
          return "green";
        case "CANCELLED":
          return "red";
        default:
          return "default";
      }
    };
  const loadData =
    async () => {
      try {
        setLoading(true);
        const [
          jobCards,
          vehiclesData,
          driversData,
          employeesData,
          partsData,
          partMasterData,
        ] = await Promise.all([
          getJobCards(),
          getVehicles(),
          getDrivers(),
          getEmployees(),
          getJobCardParts(),
          getParts(),
        ]);
        const currentJobCard =
          jobCards.find(
            item =>
              String(
                item.job_card_id
              ) ===
              String(
                jobCardId
              )
          );
        setJobCard(
          currentJobCard
        );
        setVehicles(
          vehiclesData
        );
        setDrivers(
          driversData
        );
        setEmployees(
          employeesData
        );
        setPartMaster(
          partMasterData
        );
        const filteredParts =
          partsData.filter(
            part =>
              String(part.job_card_id) ===
              String(jobCardId)
          );

        setParts(
          filteredParts
        );
      } catch (error) {

        console.error(error);

        message.error(
          "Failed to load Job Card"
        );

      } finally {

        setLoading(false);
      }
    };

  useEffect(() => {
    loadData();
  }, [jobCardId]);

  if (loading) {

    return (
      <div
        style={{
          textAlign: "center",
          marginTop: 100,
        }}
      >
        <Spin size="large" />
      </div>
    );
  }

  if (!jobCard) {

    return (
      <Card>
        Job Card not found
      </Card>
    );
  }
  const vehicle =
    vehicles.find(
      v =>
        v.vehicle_id ===
        jobCard.vehicle_id
    );

  const driver =
    drivers.find(
      d =>
        d.driver_id ===
        jobCard.driver_id
    );

  const technician1 =
    employees.find(
      e =>
        e.employee_id ===
        jobCard.technician1_id
    );

  const technician2 =
    employees.find(
      e =>
        e.employee_id ===
        jobCard.technician2_id
    );

  const partMap =
    Object.fromEntries(
      parts.map(
        (part) => [
          part.part_id,
          part.part_name,
        ]
      )
    );
  const requestedBy =
    employees.find(
      e =>
        e.employee_id ===
        jobCard.requested_by_employee_id
    );

  const verifiedBy =
    employees.find(
      e =>
        e.employee_id ===
        jobCard.verified_by_employee_id
    );

  const approvedBy =
    employees.find(
      e =>
        e.employee_id ===
        jobCard.approved_by_employee_id
    );
const activeParts =
  parts.filter(
    part => part.active_flag
  );

const partCount =
  activeParts.length;

  const partColumns = [

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
    "Quantity",

  dataIndex:
    "quantity",
},

{
  title:
    "Unit Price",

  dataIndex:
    "unit_price",
},

{
  title:
    "Total",

  render:
    (_, record) =>
      (
        record.quantity
        *
        record.unit_price
      ).toFixed(2),
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
          title= "Delete Part?"
          onConfirm={
            async () => {
              await deactivateJobCardPart( record.id );
              message.success( "Detail deactivated" );
              await loadData();
            }
          }
        >
        <Button
          danger disabled={
            !record.active_flag
          }
        >
          Delete
        </Button>
                </Popconfirm>

              </Space>
            ),
        }
          ];

        const getApprovalTag =
          (employee) => {

            if (employee) {

              return (
                <Tag color="green">
                  Approved
                </Tag>
              );
            }
            return (
              <Tag color="orange">
                Pending
              </Tag>
            );
          };
        const handleGenerateRequisition =
          async () => {

            try {

              const data =
                await generateRequisition(
                  jobCard.job_card_id
                );

              message.success(
                `Requisition ${data.requisition_number} created successfully`
              );

              await loadData();

            } catch (error) {

              message.error(
                error?.response?.data?.detail
                ||
                "Failed to generate requisition"
              );
            }
          };
            const handleSubmit =
              async () => {

                try {

                  const values =
                    await form.validateFields();
                  console.log(
          "Submitting",
          values
        );
          values.job_card_id =
            Number(
              jobCardId
            );

          if (
            editingRecord
          ) {

            await updateJobCardPart(
              editingRecord.id,
              values
            );

          } else {

            await createJobCardPart(
              values
            );
          }
          message.success(
            "Part added successfully"
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
const totalPartsCost =
  activeParts.reduce(
    (
      total,
      item
    ) =>
      total +
      (
        (
          item.quantity
          || 0
        ) *
        (
          item.unit_price
          || 0
        )
      ),
    0
  );

const labourCharges =
  Number(
    jobCard.labour_charges
    || 0
  );

const grandTotal =
  totalPartsCost +
  labourCharges;

const handleSubmitSubmit =
  async () => {

    await submitJobCard(
      jobCard.job_card_id     //,jobCard.requested_by_employee_id
    );

    message.success(
      "Submitted for verification"
    );

    loadData();
  };
  const handleVerify =
  async () => {

    await verifyJobCard(
      jobCard.job_card_id   //,jobCard.verified_by_employee_id
    );

    message.success(
      "Job Card verified"
    );

    loadData();
  };
const handleApprove =
  async () => {

    await approveJobCard(
      jobCard.job_card_id   //,jobCard.approved_by_employee_id
    );

    message.success(
      "Job Card approved"
    );

    loadData();
  };
   
const getApprovalStep =
  () => {

    switch (
      jobCard.job_status
    ) {

      case "REQUESTED":
        return 0;

      case "VERIFIED":
        return 1;

      case "APPROVED":
        return 2;

      default:
        return 0;
    }
  };  
  return (
    <Space
      direction="vertical"
      size="large"
      style={{
        width: "100%",
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
                          "/jobcards"
                        )
                      }
                    >
                      Back To Job Cards
                    </Button>
        {
          jobCard.requisition_id ? (
            <Button
              onClick={() => window.open(
                `/requisitions/${jobCard.requisition_id}`,
                "_blank"
              )
              }
            >
              View Requisition
            </Button>
          ) : (
            <Button
              type="primary"
              disabled={
                activeParts.length === 0
              }
              onClick={() =>
                handleGenerateRequisition(
                  jobCard.job_card_id
                )
              }
            >
              Generate Requisition
            </Button>
          )
        }
        <Button
          type="primary"
          onClick={() =>
            window.open(
              `${API_BASE_URL}/jobcards_print/${
                jobCard.job_card_id
              }/pdf`,
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
                marginBottom:
                  0,
              }}
            >
              Vehicle Job Card
            </Title>
          
            <div
              style={{
                textAlign:
                  "center",
                color: "#888",
                marginBottom: 20,
              }}
            >
              Job Card #
              {jobCard.job_card_id}
            </div>
        <Descriptions
          bordered
          column={2}
        >

          <Descriptions.Item
            label="Job Card No"
          >
            {
              jobCard.job_card_id
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Vehicle"
          >
            {
              vehicle?.rc_number
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Driver"
          >
            {
              driver?.driver_name
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Status"
          >
            <Tag
              color={
                getStatusColor(
                  jobCard.job_status
                )
              }
            >
              {jobCard.job_status}
            </Tag>
          </Descriptions.Item>

          <Descriptions.Item
            label="Date Time In"
          >
            {jobCard.date_time_in
              ? dayjs(
                  jobCard.date_time_in
                ).format(
                  "DD-MMM-YYYY HH:mm"
                )
              : "-"
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Date Time Out"
          >
            {jobCard.date_time_in
              ? dayjs(
                  jobCard.date_time_out
                ).format(
                  "DD-MMM-YYYY HH:mm"
                )
              : "-"
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Zone / Area"
          >
            {
              jobCard.zone_area
            }
          </Descriptions.Item>
          <Descriptions.Item
            label="Complaint ID"
          >
            {jobCard.complaint_id}
          </Descriptions.Item>
                  
          <Descriptions.Item
            label="Inspection ID"
          >
            {jobCard.inspection_id}
          </Descriptions.Item>
          <Descriptions.Item
            label="Mileage / Hours"
          >
            {
              jobCard.mileage_hours
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Maintenance Type"
          >
            {
              jobCard.maintenance_type
            }
          </Descriptions.Item>
          <Descriptions.Item
            label="Request Status"
          >
            {
              jobCard.requisition_id
                ? (
                  <Tag color="green"> GENERATED  </Tag>
                )
                : (
                  <Tag color="orange"> NOT GENERATED </Tag>
                )
            }
          </Descriptions.Item>
        </Descriptions>

      </Card>

      <Card>

        <Title level={4}>
          Technicians
        </Title>

        <Descriptions
          bordered
          column={2}
        >

          <Descriptions.Item
            label="Technician 1"
          >
            {
              technician1?.full_name
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Technician 2"
          >
            {
              technician2?.full_name
            }
          </Descriptions.Item>

        </Descriptions>

      </Card>

      <Card>

        <Title level={4}>
          Issue Details
        </Title>

        <Descriptions
          bordered
          column={1}
        >

          <Descriptions.Item
            label="Issue Reported"
          >
            {
              jobCard.issue_reported
            }
          </Descriptions.Item>

          <Descriptions.Item
            label="Problems Found & Action Taken"
          >
            {
              jobCard.problem_found_action_taken
            }
          </Descriptions.Item>

<Descriptions.Item
  label="Requisition Slip Number"
>
  {
    jobCard.requisition_id
      ? (
        <Button
          type="link"
          style={{
            padding: 0,
          }}
          onClick={() =>
            window.open(
              `/requisitions/${jobCard.requisition_id}`,
              "_blank"
            )
          }
        >
          {
            jobCard.requisition_slip_number
          }
        </Button>
      )
      : (
        "-"
      )
  }
</Descriptions.Item>
          <Descriptions.Item
            label="Part Count"
          >
            <Tag color="blue"> {partCount} 
            </Tag>
          </Descriptions.Item>
        </Descriptions>
      </Card>
      <Card>
          <Card
title={
  <>
    Parts Used
    <Tag
      color="blue"
      style={{
        marginLeft: 8,
      }}
    >
      {parts.length} Part(s)
    </Tag>
  </>
}            extra={
              <Space>
        <Button
          type="primary"
                  onClick={() => {
                    setEditingRecord(null);
                    form.resetFields();
                    form.setFieldsValue({
                      part_detail_id:
                        Number(partId),
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
                    rowKey="jobcardId"
                    columns={
                      partColumns
                    }
                    dataSource={
                      parts
                    }
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
        onValuesChange={(
          changed,
          values
        ) => {

          const quantity =
            Number(
              values.quantity || 0
            );

          const unitPrice =
            Number(
              values.unit_price || 0
            );
      <SearchableSelect
        options={
          partMaster.map(
            part => ({
              value: part.part_id,
              label: part.part_name,
            })
          )
        }
        onChange={partId => {

          const selectedPart =
            partMaster.find(
              p =>
                p.part_id === partId
            );

          if (selectedPart) {

            form.setFieldsValue({

              unit_price:
                selectedPart.standard_cost
                || 0,
            });
          }
        }}
      />

          setTotalAmount(
            quantity * unitPrice
          );
        }}
      >    <Form.Item
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
                partMaster.map(
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
            name="quantity"
            label="Quantity"
          >
            <InputNumber
              min={0}
              style={{
                width: "100%",
              }}
            />
          </Form.Item>

          <Form.Item
            name="unit_price"
            label="Unit Price"
          >
            <InputNumber
              min={0}
              style={{
                width: "100%",
              }}
            />
          </Form.Item>
      <Form.Item label="Total">

        <Input
          value={
            totalAmount.toFixed(2)
          }
          readOnly
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

      <Card>

        <Title level={4}>
          Cost Summary
        </Title>

        <Descriptions
          bordered
          column={1}
        >

          <Descriptions.Item
            label="Total Parts Cost"
          >
            ₹
            {totalPartsCost.toFixed(2)}
          </Descriptions.Item>

          <Descriptions.Item
            label="Labour Charges"
          >
            ₹
            {labourCharges.toFixed(2)}
          </Descriptions.Item>

          <Descriptions.Item
            label="Grand Total"
          >
            <strong>
              ₹
              {grandTotal.toFixed(2)}
            </strong>
          </Descriptions.Item>

        </Descriptions>

      </Card>
      <Card
        style={{
          borderTop:
            "4px solid #52c41a",
        }}
      >

<Row
          justify="space-between"
          style={{
          marginBottom: 1,}}
>
  
        <Title level={4}>
          Approval Information
        </Title>
  {
    jobCard.job_status ===
    "DRAFT" ||
    jobCard.job_status ===
    "OPEN"
      ? (
        <Button
          type="primary"
          onClick={
            handleSubmitSubmit
          }
        >
          Submit
        </Button>
      )
      : null
  }

  {
    jobCard.job_status ===
    "REQUESTED"
      ? (
        <Button
          type="primary"
          onClick={
            handleVerify
          }
        >
          Verify
        </Button>
      )
      : null
  }

  {
    jobCard.job_status ===
    "VERIFIED"
      ? (
        <Button
          type="primary"
          onClick={
            handleApprove
          }
        >
          Approve
        </Button>
      )
      : null
  }

</Row>

        <Descriptions
          bordered
          column={3}
        >

<Descriptions.Item
  label="Current Approval Status"
  span={3}
>
  <strong>
    <Tag
      color="green"
      style={{
        fontSize: 14,
        padding: "4px 12px",
      }}
    >
      {jobCard.job_status}
    </Tag>
  </strong>
</Descriptions.Item>
        </Descriptions>
<Steps
  current={getApprovalStep()}
  items={[
    {
      title: "Requested",
      description: (
        <>
          <div>
            {
              requestedBy?.full_name
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
              jobCard.requested_at
                ? dayjs(
                    jobCard.requested_at
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
      title: "Verified",
      description: (
        <>
          <div>
            {
              verifiedBy?.full_name
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
              jobCard.verified_at
                ? dayjs(
                    jobCard.verified_at
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
      title: "Approved",
      description: (
        <>
          <div>
            {
              approvedBy?.full_name
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
              jobCard.approved_at
                ? dayjs(
                    jobCard.approved_at
                  ).format(
                    "DD-MMM-YYYY HH:mm"
                  )
                : "-"
            }
          </div>
        </>
      ),
    },
  ]}
/>      </Card>
    </Space>
  );
};

export default JobCardDetail;
