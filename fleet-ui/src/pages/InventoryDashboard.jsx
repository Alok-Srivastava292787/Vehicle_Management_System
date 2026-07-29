import {
  useEffect,
  useState,
} from "react";

import {
  Card,
  Col,
  Row,
  Spin,
  Statistic,
  Table,
  Tag,
  Typography,
  message,
} from "antd";

import {
  DropboxOutlined,
  ArrowDownOutlined,
  ArrowUpOutlined,
  FundProjectionScreenOutlined,
} from "@ant-design/icons";

import {
  getInventorySummary,
  getLowStockParts,
} from "../services/dashboardService";

const { Title } =
  Typography;

const InventoryDashboard = () => {

  const [loading,
    setLoading] =
    useState(true);

  const [summary,
    setSummary] =
    useState({});

  const [lowStock,
    setLowStock] =
    useState([]);
  const [
    topConsumed,
    setTopConsumed,
    ] = useState([]);
  const [
    topReturned,
    setTopReturned,
    ] = useState([]);
  const [
    trendData,
    setTrendData,
    ] = useState([]);


  const loadData =
    async () => {
      try {
        setLoading(true);
        const [
          summaryData,
          lowStockData,
          consumedData,
          returnedData,
          trendData,
        ] =
          await Promise.all([
            getInventorySummary(),
            getLowStockParts(),
            getTopConsumedParts(),
            getTopReturnedParts(),
            getIssueReturnTrend(),
          ]);
        setSummary(
          summaryData
        );
        setLowStock(
          lowStockData
        );
        setTopConsumed(
          consumedData
        );
        setTopReturned(
          returnedData
        );
        setTrendData(
          trendData
        );
      } catch (
        error
      ) {
        console.error(          error        );
        message.error(          "Failed to load Inventory Dashboard"        );
      } finally {
        setLoading(          false        );
      }
    };
  useEffect(() => {
    loadData();
  }, []);

  const lowStockColumns = [
    {
      title:        "Part",
      dataIndex:        "part_name",
    },
    {
      title:        "Current Stock",
      dataIndex:        "balance",
    },
    {
      title:        "Minimum Stock",
      dataIndex:        "minimum_stock_qty",
    },
    {
      title:        "Status",
      render:
        () => (
          <Tag color="red">
            Low Stock
          </Tag>
        ),
    },
  ];
  const topConsumedColumns = [
        {
            title:        "Part",
            dataIndex:        "part_name",
        },
        {
            title:        "Quantity Consumed",
            dataIndex:        "quantity_consumed",
        },
    ];
 const topReturnedColumns = [
    {
        title:        "Part",
        dataIndex:        "part_name",
    },
    {
        title:        "Quantity Returned",
        dataIndex:        "quantity_returned",
    },
    ];
const trendColumns = [
  {
    title:      "Month",
    dataIndex:      "month",
  },
  {
    title:      "Issued",
    dataIndex:      "issue",
  },
  {
    title:      "Returned",
    dataIndex:      "return",
  },
];
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

  return (
    <>

      <Title level={3}>
        Inventory Dashboard
      </Title>

      <Row
        gutter={16}
      >

        <Col span={6}>

          <Card>

            <Statistic
              title=
                "Total Stock"

              value={
                summary.total_stock
                ?? 0
              }

              prefix={
                <DropboxOutlined />
              }
            />

          </Card>

        </Col>

        <Col span={6}>

          <Card>

            <Statistic
              title=
                "Total Issued"

              value={
                summary.total_issued
                ?? 0
              }

              prefix={
                <ArrowDownOutlined />
              }

              valueStyle={{
                color:
                  "#cf1322",
              }}
            />

          </Card>

        </Col>

        <Col span={6}>

          <Card>

            <Statistic
              title=
                "Total Returned"

              value={
                summary.total_returned
                ?? 0
              }

              prefix={
                <ArrowUpOutlined />
              }

              valueStyle={{
                color:
                  "#3f8600",
              }}
            />

          </Card>

        </Col>

        <Col span={6}>

          <Card>

            <Statistic
              title=
                "Transactions"

              value={
                summary.total_transactions
                ?? 0
              }

              prefix={
                <FundProjectionScreenOutlined />
              }
            />

          </Card>

        </Col>

      </Row>

      <Row
        gutter={16}
        style={{
          marginTop:
            24,
        }}
      >

        <Col span={24}>

          <Card
            title="Low Stock Parts"
          >

            <Table
              rowKey={
                row =>
                  row.part_id
              }
              columns={
                lowStockColumns
              }
              dataSource={
                lowStock
              }
              pagination={
                false
              }
            />

          </Card>

        </Col>

      </Row>
      <Row
        gutter={16}
        style={{
            marginTop: 24,
        }}
        >

        <Col span={24}>

            <Card
            title=
            "Top Consumed Parts"
            >

            <Table
                rowKey=
                "part_id"

                columns={
                topConsumedColumns
                }

                dataSource={
                topConsumed
                }

                pagination={
                false
                }
            />

            </Card>

        </Col>

        </Row>
        <Row
            gutter={16}
            style={{
                marginTop: 24,
            }}
            >

            <Col span={24}>

                <Card
                title=
                "Top Returned Parts"
                >

                <Table
                    rowKey=
                    "part_id"

                    columns={
                    topReturnedColumns
                    }

                    dataSource={
                    topReturned
                    }

                    pagination={
                    false
                    }
                />
                </Card>
            </Col>
        </Row>
        <Row
            gutter={16}
            style={{
                marginTop: 24,
            }}
            >

            <Col span={24}>

                <Card
                title=
                "Monthly Issue vs Return Trend"
                >

                <Table
                    rowKey="month"
                    columns={
                    trendColumns
                    }
                    dataSource={
                    trendData
                    }
                    pagination={
                    false
                    }
                />
                </Card>
            </Col>
            </Row>
    </>
  );
};

export default
  InventoryDashboard;