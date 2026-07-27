import apiClient
  from "../api/apiClient";

export const getPartReturnDetails =
  async () => {

    const response =
      await apiClient.get(
        "/part-return-details",
        {
          params: {
            _ts: Date.now(),
          },
        }
      );

    return response.data;
  };

export const createPartReturnDetail =
  async payload => {

    const response =
      await apiClient.post(
        "/part-return-details",
        payload
      );

    return response.data;
  };

export const updatePartReturnDetail =
  async (
    returnDetailId,
    payload
  ) => {

    const response =
      await apiClient.put(
        `/part-return-details/${returnDetailId}`,
        payload
      );

    return response.data;
  };

export const deactivatePartReturnDetail =
  async returnDetailId => {

    const response =
      await apiClient.delete(
        `/part-return-details/${returnDetailId}`
      );

    return response.data;
  };