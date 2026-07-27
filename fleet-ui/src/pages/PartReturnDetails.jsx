
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
} from "antd";

import {
  useNavigate,
  useParams,
} from "react-router-dom";

import {  API_BASE_URL,} from "../utils/config";
import {  getPartReturns,} from "../services/partReturnService";

import {  getPartReturnDetails,} from "../services/partReturnDetailService";

import {  getEmployees,} from "../services/employeeService";

import {  getParts,} from "../services/partService";

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

    const [parts,
      setParts] =
      useState([]);

    const loadData =
      async () => {

        try {

          const [
            returnData,
            detailData,
            employeeData,
            partData,
          ] =
            await Promise.all([
              getPartReturns(),
              getPartReturnDetails(),
              getEmployees(),
              getParts(),
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
              label="Requisition"
            >
              {
                returnPart.requisition_id
              }
            </Descriptions.Item>

          </Descriptions>

        </Card>

        <Card>

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

      </Space>
    );
  };

export default PartReturnDetails;