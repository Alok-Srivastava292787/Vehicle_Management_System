import apiClient
  from "../api/apiClient";

export const getInventorySummary =
  async () => {

    const response =
      await apiClient.get(
        "/stock-ledger/dashboard/summary"
      );

    return response.data;
  };

export const getLowStockParts =
  async () => {

    const response =
      await apiClient.get(
        "/stock-ledger/dashboard/low-stock"
      );

    return response.data;
  };
export const getTopConsumedParts =
  async () => {

    const response =
      await apiClient.get(
        "/stock-ledger/dashboard/top-consumed"
      );

    return response.data;
  };
export const getTopReturnedParts =
  async () => {

    const response =
      await apiClient.get(
        "/stock-ledger/dashboard/top-returned"
      );

    return response.data;
  };
  export const getIssueReturnTrend =
  async () => {

    const response =
      await apiClient.get(
        "/stock-ledger/dashboard/trend"
      );

    return response.data;
  };