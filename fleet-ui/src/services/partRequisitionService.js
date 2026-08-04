import apiClient from "../api/apiClient";

export const getPartRequisitions = async () => {
    const response = await apiClient.get("/requisitions",{params: { _ts: Date.now(),},});

    return response.data;
  };

export const createPartRequisition =  async (payload) => {
    const response = await apiClient.post("/requisitions", payload);

    return response.data;
  };

export const updatePartRequisition = async (requisitionId,payload) => {
    const response =await apiClient.put( `/requisitions/${requisitionId}`, payload);

    return response.data;
  };

export const deactivatePartRequisition =
  async (
    requisitionId
  ) => {

    const response =
      await apiClient.delete(
        `/requisitions/${requisitionId}`
      );

    return response.data;
  };
  export const submitRequest =
  async requestId => {

    const response =
      await apiClient.post(
        `/requisitions/${requestId}/submit`
      );

    return response.data;
  };
  export const approveRequest =
  async requestId => {

    const response =
      await apiClient.post(
        `/requisitions/${requestId}/approve`
      );

    return response.data;
  };