import {
  useEffect,
  useState,
} from "react";

import {
  Card,
  Table,
  Tag,
  Typography,
  message,
} from "antd";

import SearchToolbar from
  "../components/SearchToolbar";

import tablePagination from
  "../utils/tablePagination";

import {
  getStockLedger,
} from "../services/stockLedgerService";

import {
  getParts,
} from "../services/partService";

const { Title } =
  Typography;

const StockLedger = () => {

  const [loading,
    setLoading] =
    useState(false);

  const [ledger,
    setLedger] =
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

  const loadData =
    async () => {

      try {

        setLoading(true);

        const [
          ledgerData,
          partData,
        ] =
          await Promise.all([
            getStockLedger(),
            getParts(),
          ]);

        setLedger(
          ledgerData
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
          "Failed to load Stock Ledger"
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
    ledger.filter(
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
        "Ledger ID",

      dataIndex:
        "ledger_id",

      width:
        100,
    },

    {
      title:
        "Date",

      dataIndex:
        "transaction_date",

      width:
        180,

      render:
        value =>
          value
            ? new Date(
                value
              ).toLocaleString()
            : "-",
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
        "Transaction",

      dataIndex:
        "transaction_type",

      render:
        value => {

          let color =
            "blue";

          if (
            value ===
            "ISSUE"
          ) {
            color =
              "red";
          }

          if (
            value ===
            "RETURN"
          ) {
            color =
              "green";
          }

          if (
            value ===
            "OPENING"
          ) {
            color =
              "gold";
          }

          if (
            value ===
            "ADJUSTMENT"
          ) {
            color =
              "purple";
          }

          return (
            <Tag
              color={
                color
              }
            >
              {value}
            </Tag>
          );
        },
    },

    {
      title:
        "Reference",

      dataIndex:
        "reference_id",

      width:
        120,
    },

    {
      title:
        "Qty In",

      dataIndex:
        "quantity_in",

      width:
        120,

      render:
        value => (
          <span
            style={{
              color:
                "green",
              fontWeight:
                600,
            }}
          >
            {value}
          </span>
        ),
    },

    {
      title:
        "Qty Out",

      dataIndex:
        "quantity_out",

      width:
        120,

      render:
        value => (
          <span
            style={{
              color:
                "red",
              fontWeight:
                600,
            }}
          >
            {value}
          </span>
        ),
    },

    {
      title:
        "Balance",

      dataIndex:
        "balance_quantity",

      width:
        120,

      render:
        value => (
          <span
            style={{
              fontWeight:
                700,
            }}
          >
            {value}
          </span>
        ),
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
  ];

  return (
    <>

      <Title level={3}>
        Stock Ledger
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
        hideAddButton
        searchPlaceholder=
          "Search Part"
      />

      <Card>

        <Table
          rowKey=
            "ledger_id"
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

    </>
  );
};

export default StockLedger;