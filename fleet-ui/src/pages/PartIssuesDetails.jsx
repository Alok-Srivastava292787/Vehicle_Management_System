
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
import {  getPartIssues,} from "../services/partIssueService";

import {  getPartIssueDetails,} from "../services/partIssueDetailService";

import {  getEmployees,} from "../services/employeeService";

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

          <Table
            rowKey="issue_detail_id"
            columns={columns}
            dataSource={details}
            pagination={false}
          />

        </Card>

      </Space>
    );
  };

export default PartIssueDetails;