import {
  useEffect,
  useState,
} from "react";

import {
  Button,
  Card,
  Form,
  Input,
  InputNumber,
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
  EditOutlined,
  DeleteOutlined,
} from "@ant-design/icons";

import SearchToolbar
  from "../components/SearchToolbar";

import tablePagination
  from "../utils/tablePagination";

import {
  getOpeningStock,
  createOpeningStock,
  updateOpeningStock,
  deactivateOpeningStock,
} from "../services/openingStockService";

import {
  getParts,
} from "../services/partService";
import {SearchableSelect } from "../components/SearchableSelect";
const { Title } =
  Typography;

const OpeningStock = () => {

  const [loading,
    setLoading] =
    useState(false);

  const [openingStock,
    setOpeningStock] =
    useState([]);

  const [parts,
    setParts] =
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

  const loadData =
    async () => {

      try {

        setLoading(true);

        const [
          openingData,
          partData,
        ] =
          await Promise.all([
            getOpeningStock(),
            getParts(),
          ]);

        setOpeningStock(
          openingData
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
          "Failed to load Opening Stock"
        );

      } finally {

        setLoading(
          false
        );
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
        active_flag:
          true,
      });

      setModalOpen(
        true
      );
    };

  const openEditModal =
    record => {

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
    };

  const handleSubmit =
    async () => {

      try {

        const values =
          await form.validateFields();

        if (
          editingRecord
        ) {

          await updateOpeningStock(
            editingRecord.opening_stock_id,
            values
          );

        } else {

          await createOpeningStock(
            values
          );
        }

        message.success(
          "Opening Stock saved successfully"
        );

        setModalOpen(
          false
        );

        await loadData();

      } catch (
        error
      ) {

        message.error(
          error?.response?.data?.detail
          ||
          "Operation failed"
        );
      }
    };

  const handleDeactivate =
    async (
      openingStockId
    ) => {

      try {

        await deactivateOpeningStock(
          openingStockId
        );

        message.success(
          "Opening Stock deactivated"
        );

        await loadData();

      } catch {

        message.error(
          "Operation failed"
        );
      }
    };

  const partMap =
    Object.fromEntries(
      parts.map(
        part => [
          part.part_id,
          part.part_name,
        ]
      )
    );

  const filteredData =
    openingStock.filter(
      item => {

        const partName =
          partMap[
            item.part_id
          ] ?? "";

        const matchesSearch =
          partName
            .toLowerCase()
            .includes(
              searchText.toLowerCase()
            );

        const matchesStatus =
          statusFilter ===
            "ALL"
          ||
          (
            statusFilter ===
              "ACTIVE"
            &&
            item.active_flag
          )
          ||
          (
            statusFilter ===
              "INACTIVE"
            &&
            !item.active_flag
          );

        return (
          matchesSearch
          &&
          matchesStatus
        );
      }
    );

  const columns = [

    {
      title:
        "ID",
      dataIndex:
        "opening_stock_id",
      width: 80,
    },

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
        "Opening Quantity",

      dataIndex:
        "opening_quantity",
    },

    {
      title:
        "Remarks",

      dataIndex:
        "remarks",
    },

    {
      title:
        "Status",

      render:
        (_, record) => (

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
              title="Deactivate Opening Stock?"
              onConfirm={() =>
                handleDeactivate(
                  record.opening_stock_id
                )
              }
            >

              <Button
                danger
                icon={
                  <DeleteOutlined />
                }
                disabled={
                  !record.active_flag
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
        Opening Stock
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
        searchPlaceholder=
          "Search Opening Stock"
        addLabel=
          "Add Opening Stock"
      />

      <Card>

        <Table
          rowKey=
            "opening_stock_id"
          loading={
            loading
          }
          columns={
            columns
          }
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
            ? "Edit Opening Stock"
            : "Add Opening Stock"
        }
        open={
          modalOpen
        }
        onOk={
          handleSubmit
        }
        onCancel={() =>
          setModalOpen(
            false
          )
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
            name="opening_quantity"
            label="Opening Quantity"
            rules={[
              {
                required: true,
              },
            ]}
          >

            <InputNumber
              min={0}
              style={{
                width:
                  "100%",
              }}
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

export default OpeningStock;