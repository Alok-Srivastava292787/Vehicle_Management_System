import apiClient
  from "../api/apiClient";

export const getPartReturns =
  async () => {

    const response =
      await apiClient.get(
        "/part-returns",
        {
          params: {
            _ts: Date.now(),
          },
        }
      );

    return response.data;
  };

export const createPartReturn =
  async payload => {

    const response =
      await apiClient.post(
        "/part-returns",
        payload
      );

    return response.data;
  };

export const updatePartReturn =
  async (
    returnId,
    payload
  ) => {

    const response =
      await apiClient.put(
        `/part-returns/${returnId}`,
        payload
      );

    return response.data;
  };

export const deactivatePartReturn =
  async returnId => {

    const response =
      await apiClient.delete(
        `/part-returns/${returnId}`
      );

    return response.data;
  };