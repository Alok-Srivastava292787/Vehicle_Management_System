//src/services/stockLedgerService.js
import apiClient
  from "../api/apiClient";

export const getStockLedger =
  async () => {

    const response =
      await apiClient.get(
        "/stock-ledger"
      );

    return response.data;
  };

export const getPartBalance =
  async partId => {

    const response =
      await apiClient.get(
        `/stock-ledger/balance/${partId}`
      );

    return response.data;
  };
