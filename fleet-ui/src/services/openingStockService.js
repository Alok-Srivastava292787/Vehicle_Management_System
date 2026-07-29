import apiClient
  from "../api/apiClient";

export const getOpeningStock =
  async () => {

    const response =
      await apiClient.get(
        "/opening-stock",
        {
          params: {
            _ts: Date.now(),
          },
        }
      );

    return response.data;
  };

export const createOpeningStock =
  async payload => {

    const response =
      await apiClient.post(
        "/opening-stock",
        payload
      );

    return response.data;
  };

export const updateOpeningStock =
  async (
    openingStockId,
    payload
  ) => {

    const response =
      await apiClient.put(
        `/opening-stock/${openingStockId}`,
        payload
      );

    return response.data;
  };

export const deactivateOpeningStock =
  async openingStockId => {

    const response =
      await apiClient.delete(
        `/opening-stock/${openingStockId}`
      );

    return response.data;
  };